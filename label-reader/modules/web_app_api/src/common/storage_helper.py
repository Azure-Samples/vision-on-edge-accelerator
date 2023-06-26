import base64
import datetime
import json
from typing import Union

import azure.core
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient
from src.entities.feedback_entity import FeedbackEntity, MetricsPayloadWrapper
from logging import Logger
from src.util.config import StorageConfig


class StorageServiceHelper(object):
    """A Helper class that provides methods to upload an image to Azure Blob Storage after
    extracting the image frame and feedback entity from the payload received.

    """

    def __init__(self, logger: Logger, storage_config: StorageConfig) -> None:
        """initializes the configuration settings required to access Blob
        Storage, and acquires a reference to the Logger utility
        @param logger: Logger utility
        @param storage_config: StorageConfig object containing the storage configuration settings
        @param basic_sampler: Basic Samplerobject containing the sampling logic before upload of image to blob storage

        @return: None
        """
        self.logger = logger
        self.config = storage_config
        self._initialize_storage_client()

    def _initialize_storage_client(self) -> None:
        # Instantiate a new BlobServiceClient using a connection string
        # set a retry policy of 3 times
        self.logger.info("Initializing Blob storage connections ...")
        try:
            blob_service_client = BlobServiceClient.from_connection_string(
                self.config.blob_storage_conn_string, retry_total=3
            )
        except Exception as e:
            self.logger.error(f"Error connecting to Azure Blob Storage {e}, {type(e)}")
            self.logger.exception(e)
            return None

        with blob_service_client:
            container_client = blob_service_client.get_container_client(
                self.config.container_name
            )

            # Instantiate a new ContainerClient
            try:
                # Create new Container in the service
                container_client.create_container()
                self.logger.info("created a blob storage container for first use...")
            except azure.core.exceptions.ResourceExistsError as ree:
                self.logger.info(
                    f"blob storage container {self.config.container_name} already exists ..."
                )
                self.logger.exception(ree)
            except Exception as ex:
                self.logger.error(
                    f"error creating blob storage container {self.config.container_name},\
                        {ex}, {type(ex)}"
                )
                self.logger.exception(ex)
                return None

    def verify_upload_frame(self, message: str) -> MetricsPayloadWrapper:
        """verifies the payload before uploading the image frame to Azure Blob Storage

        Args:
            message (str): the payload containing the user feedback along with the image frame
            initConfig (bool): a flag to indicate whether the required configuration settings
            to upload to blob storage are already initialized, through a call to _set_config_state
            method. If not intialized, this method will initialize the settings.

        Returns:
            MetricsPayloadWrapper: The Feedback Entity that was extracted from the payload in the
            incoming message
        """
        feedback_obj = None
        # parse the payload from UI and extract the content
        try:
            feedback_payload = json.loads(message)
            feedback_obj = FeedbackEntity(**feedback_payload)
            if (
                len(feedback_obj.correlation_id) == 0
                or len(feedback_obj.device_id) == 0
                or len(feedback_obj.store_id) == 0
                or len(feedback_obj.captured_frame) == 0
            ):
                self.logger.error(
                    "key attributes in feedback message payload from UI have empty values .. "
                    + f"correlation id length : {len(feedback_obj.correlation_id)}, "
                    + f"device id length : {len(feedback_obj.device_id)}, "
                    + f"store id length : {len(feedback_obj.store_id)}, "
                    + f"captured frame length : {len(feedback_obj.captured_frame)}"
                )
                return None

            # decode the string to extract the image content for uploading to blob storage
            l_image = base64.b64decode(feedback_obj.captured_frame)
        except Exception as e:
            self.logger.error("Error in parsing the incoming feedback message from UI")
            self.logger.exception(e)
            return None

        # upload the image to Azure Blob storage
        l_blob_name = self._upload_frame(
            l_image,
            feedback_obj.device_id,
            feedback_obj.store_id,
            feedback_obj.correlation_id,
        )

        # return the feedback entity object to the caller along with the blob url
        return MetricsPayloadWrapper(feedback_obj, l_blob_name)

    def _upload_frame(
        self, frame: bytes, device_id: str, store_id: str, correlation_id: str
    ) -> Union[str, None]:
        """internal method that uploads the image frame in the feedback message from UI
        to Azure Blob storage

        Args:
            frame (str): image frame to upload
            device_id (str): The device ID of the Jetson Nano
            store_id (str): The ID of the retail store where the device is located
            correlation_id (str): internal GUID used to track the request flow

        Returns:
            str: The blob name of the uploaded image frame

        Raises:
            ResourceExistsError: when a blob with the same name already exists
            Exception: all other errors, network errors, momentary failures, etc.
        """

        # Instantiate a new BlobClient and set the path to upload the image frame
        blob_name = (
            store_id
            + "/"
            + device_id
            + "/"
            + "userfeedback"
            + "/"
            + datetime.datetime.now().strftime("%Y-%m-%d")
            + "/"
            + correlation_id
            + ".jpg"
            # datetime.datetime.now().strftime('%H-%M-%S') + ".jpg"
        )

        try:
            blob_client = BlobClient.from_connection_string(
                conn_str=self.config.blob_storage_conn_string,
                container_name=self.config.container_name,
                blob_name=blob_name,
            )

            # Upload the image frame to the blob storage
            blob_client.upload_blob(frame, blob_type="BlockBlob")

            self.logger.info(
                f"uploaded image frame to blob storage, {blob_client.blob_name}"
            )

            # return the URL of the uploaded image to the caller
            return blob_client.blob_name
        except Exception as ex:
            self.logger.error(
                f"Error uploading image frame to blob storage : , {ex}, {type(ex)}"
            )
            self.logger.exception(ex)
            return None
