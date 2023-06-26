from src.common.config_handler import ConfigHandler
from src.common.metrics_logger import MetricsLogger
from src.common.storage_helper import StorageServiceHelper
from src.entities.response_msg import acknowledgement
from src.util import log_helper
from src.webappapi.feedback import Feedback
from tornado import websocket
from src.util.log_helper import get_logger


class FeedbackHandler(websocket.WebSocketHandler):
    """WebSocket Request Handler for the use case related to capturing User Feedback
    from the UI Component. This handler is meant for the UI Component,
    which is the sender of the User Feedback messages

    Args:
        websocket (_type_): WebSocketHandler for connections from UI Component

    Returns:
        _type_: NA
    """

    # Cross Origin requests is being allowed for now. Needs to be revisited
    # in subsequent sprints

    # overridden method from WebsocketHandler
    def check_origin(self, origin) -> bool:
        return True

    # overridden method from WebsocketHandler
    def open(self) -> None:

        # Set a no-wait indication when receiving messages
        self.set_nodelay(True)
        self.storage_helper = None
        # add this connection to the in-memory list
        Feedback.addClient(self)

    def get_compression_options(self):
        # Non-None enables compression with default options.
        if webapp_api_config.compression_is_enabled:
            logger.debug("Set default compression level for this connection")
            # compression level 6 is the default compression level..
            return {"compression_level": 6, "mem_level": 5}
        else:
            logger.debug("compression is disabled for this connection")
            return None

    # overridden method from WebsocketHandler
    def on_close(self) -> None:
        Feedback.removeClient(self)

    # overridden method from WebsocketHandler
    def on_message(self, message: str) -> None:
        """Handler action when an incoming message is received

        message (str): incoming message from the UI Component containing
        the feedback. The base64 string from within it will be uploaded
        to Azure Blob storage
        """
        # send an acknowledgement to the UI that the feedback was received
        self.write_message(acknowledgement())

        # initialize and upload the frame in the feedback message to Blob Storage
        self._initialize_storage_helper()
        wrapper_obj = self.storage_helper.verify_upload_frame(message)

        if wrapper_obj is None or wrapper_obj.blob_name is None:
            logger.error(
                "Image from User feedback could not be uploaded to Blob Storage, no data sent to Metrics Service"
            )
            return
        # send the metrics to App Insights
        metrics_logger.log_metrics_for_user_feedback(
            wrapper_obj.feedback_obj, wrapper_obj.blob_name
        )

    def _initialize_storage_helper(self):
        if self.storage_helper is None:
            storage_config = config_handler.get_storage_config()
            self.storage_helper = StorageServiceHelper(
                get_logger(component_name=StorageServiceHelper.__name__), storage_config
            )


logger = log_helper.get_logger(component_name=FeedbackHandler.__name__)

# Initialize the config settings for Webapp api
config_handler = ConfigHandler()
webapp_api_config = config_handler.get_webapp_api_config()
metrics_logger = MetricsLogger()
