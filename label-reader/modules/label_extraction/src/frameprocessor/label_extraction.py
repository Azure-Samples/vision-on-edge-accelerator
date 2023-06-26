"""This module is used to provide the label extraction process."""
import time


from src.common.config_handler import ConfigHandler
from src.common.expiring_cache import ExpiringCache
from src.common.log_helper import APP_LOGGER, get_logger
from src.common.metrics_logger import MetricsLogger
from src.common.sampler import BasicSampler
from src.common.socket_client import SocketClient
from src.common.status import ErrorCode
from src.common.utils import convert_to_jpeg, encode_audio, encode_image
from src.edgeinferencing.edge_model import TextDetection
from src.edgeinferencing.request import TextDetectionRequest
from src.frameprocessor.order_notifier import OrderNotification, OrderNotifier
from src.frameprocessor.status_notifier import StatusNotifier
from src.frameprovider.label_extraction_request import LabelExtractionRequest
from src.metrics.latency_metrics import LatencyMetrics, OutcomeType
from src.frameprocessor.labelprocessor.label_processing import LabelProcessing
from src.frameprocessor.labelprocessor.default_label_processor import LabelProcessor
from src.frameprocessor.labelprocessor.model import (
    LabelProcessingRequest,
    LabelProcessingResponse,
)
from src.metrics.ocr_model_metrics import (
    OcrModelProcessingMetrics,
    set_ocr_model_metrics
)
from src.frameprocessor.labelprocessor.afr_runner import AFRRunner
from src.pcm.queue import ProcessQueue
from src.storage.storage_helper import StorageServiceHelper
from src.storage.storage_request import StorageUploadRequest
from src.tts.tts import TTS


class LabelExtractionProcess:
    """
    LabelExtractionProcess class.
    """

    def __init__(self, queue: ProcessQueue) -> None:
        """
        Initialize the LabelExtractionProcess class.

        @param
            queue (ProcessQueue): queue
        """
        self.logger = get_logger(component_name=LabelExtractionProcess.__name__)
        self.queue = queue
        config_handler = ConfigHandler()

        text_detection_config = config_handler.get_db_postprocess_config()
        model_config = config_handler.get_edge_model_config()
        text_detection_validation_config = (
            config_handler.get_text_detection_validation_config()
        )
        self.text_detection = TextDetection(
            text_detection_config,
            model_config,
            text_detection_validation_config,
            get_logger(component_name=TextDetection.__name__),
        )

        self.config = config_handler.get_label_extraction_config()
        status_ws = self._connect_to_socket(self.config.status_internal_url)
        self.status_notifier = StatusNotifier(status_ws)

        order_ws = self._connect_to_socket(self.config.order_info_internal_url)
        self.order_notifier = OrderNotifier(order_ws)

        ocr_validation_config = config_handler.get_ocr_validation_config()
        label_processor = LabelProcessor(
            ocr_validation_config.confidence_threshold,
            get_logger(LabelProcessor.__name__),
        )

        form_recog_config = config_handler.get_az_cogs_formrecog_config()
        frame_size = config_handler.get_label_extraction_config().frame_size_ocr

        afr_runner = AFRRunner(frame_size, form_recog_config)
        self.label_processing = LabelProcessing(
            afr_runner, label_processor, get_logger(LabelProcessing.__name__)
        )

        tts_azure_config = config_handler.get_az_cogs_tts_config()
        tts_config = config_handler.get_tts_config()
        self.tts = TTS(
            tts_config, tts_azure_config, get_logger(component_name=TTS.__name__)
        )
        sampler_config = config_handler.get_sampler_config()
        sampler = BasicSampler(
            get_logger(component_name=BasicSampler.__name__), sampler_config
        )

        storage_config = config_handler.get_storage_config()
        self.storage_helper = StorageServiceHelper(
            get_logger(component_name=StorageServiceHelper.__name__),
            storage_config,
            sampler,
        )

        self.metrics_logger = MetricsLogger(
            get_logger(component_name=MetricsLogger.__name__)
        )

        duplicate_order_cache_config = config_handler.get_duplicate_order_cache_config()
        self.duplicate_order_cache = ExpiringCache(
            duplicate_order_cache_config.max_len,
            duplicate_order_cache_config.max_age_in_seconds,
            self.logger,
        )

    def run(self) -> None:
        """
        Run the label extraction process.
        """
        self.logger.info("Starting label extraction process...")
        try:
            self.text_detection.initialize()
            self.duplicate_order_cache.initialize()
        except Exception as e:
            self.logger.exception(e)
            self.logger.error(f"Label extraction process initialization failed. {e}")
            raise e
        while True:
            if not self.queue.is_empty():
                item = self.queue.get_item()
                if item is None:
                    time.sleep(0.01)
                    continue
                # initialize the latency metrics & ds metrics objects
                ds_model_metrics = OcrModelProcessingMetrics(
                    item.correlation_id,
                )
                latency_metrics = LatencyMetrics(item.correlation_id)
                self._process(item, ds_model_metrics, latency_metrics)

                # Log the latency metrics and DS Model inference metrics to App Insights
                if latency_metrics.is_candidate_for_logging:
                    latency_metrics.set_total_metrics(item.t_start_frame)
                    self.metrics_logger.log_latency_metrics(
                        latency_metrics.getExtraProperties()
                    )

                if ds_model_metrics.is_candidate_for_logging:
                    self.metrics_logger.log_ds_model_metrics(
                        ds_model_metrics.getExtraProperties()
                    )
            else:
                time.sleep(0.1)

    def _process(
        self,
        item: LabelExtractionRequest,
        ds_model_metrics: OcrModelProcessingMetrics,
        latency_metrics: LatencyMetrics,
    ) -> None:
        """
        Process the label extraction request.

        @param
            item (LabelExtractionRequest): label extraction request
            ds_model_metrics (OcrModelProcessingMetrics): ocr model processing metrics object
            latency_metrics (LatencyMetrics): latency metrics object
        """
        text_detection_result = None
        APP_LOGGER.add_correlation_id(item.correlation_id)
        text_detect_start_time = time.time()
        try:
            text_detection_result = self.text_detection.run(
                TextDetectionRequest(item.frame)
            )
            self.logger.debug(
                f"Text validation result: {text_detection_result.validation_result}"
            )
            self.status_notifier.notify(text_detection_result, item.correlation_id)
            if not text_detection_result.validation_result.is_valid:
                return
        except Exception as e:
            self.logger.exception(e)
            self.status_notifier.notify_system(
                ErrorCode.EDGE_MODEL_ERROR, item.correlation_id
            )
            return
        finally:
            if text_detection_result is None or (
                not text_detection_result.validation_result.is_valid
                and text_detection_result.validation_result.error_code
                == ErrorCode.NO_CUP
            ):
                latency_metrics.set_exclude_from_logging()
                ds_model_metrics.set_exclude_from_logging()
                return
            # set the latency metric for local inference
            latency_metrics.set_edge_inference_metrics(text_detect_start_time)

            if (
                text_detection_result.validation_result.error_code
                == ErrorCode.SKIP_FRAME
            ):
                latency_metrics.set_outcome_type(OutcomeType.skipped.name)
                ds_model_metrics.set_outcome_type(OutcomeType.skipped.name)
                ds_model_metrics.failure_cause = OutcomeType.skipped.name

            # set the model metrics for local reference
            if text_detection_result.boxes is not None:
                ds_model_metrics.set_edge_inference_metrics(
                    len(text_detection_result.boxes)
                )

        label_processing_result = None
        ocr_start_time = time.time()
        try:
            label_processing_result: LabelProcessingResponse = (
                self.label_processing.run(LabelProcessingRequest(item.frame))
            )
            self.logger.debug(
                f"Label processing result: {label_processing_result.validation_result}"
            )
            self.status_notifier.notify(label_processing_result, item.correlation_id)
            if not label_processing_result.validation_result.is_valid:
                return
        except Exception as e:
            self.logger.exception(e)
            self.status_notifier.notify_system(
                ErrorCode.LABEL_PROCESSING_ERROR, item.correlation_id
            )
            return
        finally:
            # update the latency metrics for ocr
            latency_metrics.set_ocr_metrics(ocr_start_time)

            if label_processing_result is not None:
                if label_processing_result.validation_result is not None:
                    if label_processing_result.validation_result.is_valid:
                        latency_metrics.set_meta_data(
                            label_processing_result.transformed_result
                        )
            # prepare the Request object to upload to Blob Storage
            # & upload frame to Blob Storage when the ocr inference fails
            if (
                label_processing_result is None
                or not label_processing_result.validation_result.is_valid
            ):
                blob_name = self.storage_helper.verify_upload_frame(
                    StorageUploadRequest(
                        image=convert_to_jpeg(item.frame),
                        correlation_id=item.correlation_id,
                        device_id=self.config.device_id,
                        store_id=self.config.store_id,
                    )
                )
                # update the ds model metrics object with blob name
                if blob_name is not None:
                    ds_model_metrics.set_blob_name(blob_name)

            set_ocr_model_metrics(label_processing_result, ds_model_metrics)

        if label_processing_result.validation_result.is_valid:
            if self.duplicate_order_cache.contains(
                label_processing_result.hash_identity
            ):
                self.logger.info(
                    f"Duplicate extracted info: {label_processing_result.transformed_result}"
                )
                latency_metrics.set_outcome_type(OutcomeType.duplicate.name)
                ds_model_metrics.set_outcome_type(OutcomeType.duplicate.name)
                return
        tts_start_time = time.time()
        tts_result = None
        try:
            tts_result = self.tts.run(label_processing_result.content_for_narration)
            tts_result.audio_content
            self.order_notifier.notify_order(
                OrderNotification(
                    encode_audio(tts_result.audio_content),
                    encode_image(item.frame),
                    item.correlation_id,
                    self.config.store_id,
                    self.config.device_id,
                    label_processing_result.content_for_ui,
                )
            )
            if label_processing_result.validation_result.is_valid:
                self.duplicate_order_cache.add_item(
                    label_processing_result.hash_identity,
                    label_processing_result.hash_identity,
                )
                self.logger.info(
                    f"Adding hash identity: {label_processing_result.hash_identity} to cache"
                )
        except Exception as e:
            self.logger.exception(e)
            self.status_notifier.notify_system(ErrorCode.TTS_ERROR, item.correlation_id)
            return
        finally:
            # update the latency metric for the inference
            latency_metrics.set_tts_metrics(tts_start_time)
            if tts_result is not None and tts_result.audio_content is not None:
                latency_metrics.set_outcome_type(OutcomeType.success.name)

    def _connect_to_socket(self, url: str) -> SocketClient:
        """
        Connect to socket.

        @param
            url (str): websocket url
        @return
            SocketClient: socket client
        """
        ws = SocketClient(url)
        ws.connect()
        ws.start_dispatcher()
        return ws
