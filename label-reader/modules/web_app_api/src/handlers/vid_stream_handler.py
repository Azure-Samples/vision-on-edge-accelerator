from src.common.config_handler import ConfigHandler
from src.util import log_helper, message_sender
from src.util.message_sender import UseCaseScenarios
from src.webappapi.vid_stream import VideoStream, VideoStreamInternal
from tornado import websocket


class VideoStreamInternalHandler(websocket.WebSocketHandler):
    """Handler for WebSocket connections from label reader
    (for video stream)

    Args:
        websocket (_type_): WebSocketHandler for  connections from
        label reader

    Returns:
        _type_: NA
    """

    # Cross Origin requests is being allowed for now. Needs to be revisited
    # in subsequent iterations
    def check_origin(self, origin) -> bool:
        return True

    def open(self) -> None:

        # Set a no-wait indication when receiving messages
        # overridden method from WebsocketHandler
        self.set_nodelay(True)

        # add this connection to the in-memory list
        # overridden method from WebsocketHandler
        VideoStreamInternal.addClient(self)

    def on_close(self) -> None:
        # overridden method from WebsocketHandler
        VideoStreamInternal.removeClient(self)

    def get_compression_options(self):
        # Non-None enables compression with default options.
        if l_config.compression_is_enabled:
            vid_stream_internal_logger.debug(
                "Set default compression level for this connection"
            )
            # compression level 6 is the default compression level..
            return {"compression_level": 6, "mem_level": 5}
        else:
            vid_stream_internal_logger.debug(
                "compression is disabled for this connection"
            )
            return None

    # overridden method from WebsocketHandler
    def on_message(self, message: str) -> None:
        """Handler action when an incoming message is received

        Args:
            message (str): the message to relay
        """
        # Get the UI Clients that are waiting to get the Video frames
        allClients = VideoStream.getConnectedLabelReaders()

        # Relay the message
        error_indicator = message_sender.send_message(
            allClients, UseCaseScenarios.VideoStreamToUi.value, message, True
        )
        if error_indicator.outcome is False:
            """This is sent as a separate message, back to
            the caller, and not as a response to the original msg
            """
            self.write_message(
                f" Error relaying the message to the client - {error_indicator.msg_out_error}"
            )


"""Handler for WebSocket connections from Label Reader, to receive
    live video stream that is sent to the UI component
"""


class VideoStreamHandler(websocket.WebSocketHandler):
    """Handler for WebSocket connections from UI Component
    (for video stream)

    Args:
        websocket (_type_): WebSocketHandler for  connections from
        UI Component

    Returns:
        _type_: NA
    """

    # Cross Origin requests is being allowed for now. Needs to be revisited in
    #  subsequent sprints
    def check_origin(self, origin) -> bool:
        return True

    # overridden method from WebsocketHandler
    def open(self) -> None:

        # overridden method from WebsocketHandler
        # Set a no-wait indication when receiving messages
        self.set_nodelay(True)

        # overridden method from WebsocketHandler
        # add this connection to the in-memory list
        VideoStream.addClient(self)

    # overridden method from WebsocketHandler
    def on_close(self) -> None:
        VideoStream.removeClient(self)

    def get_compression_options(self):
        # Non-None enables compression with default options.
        if l_config.compression_is_enabled:
            vid_stream_logger.debug("Set default compression level for this connection")
            # compression level 6 is the default compression level..
            return {"compression_level": 6, "mem_level": 5}
        else:
            vid_stream_logger.debug("compression is disabled for this connection")
            return None

    # overridden method from WebsocketHandler
    def on_message(self, message: str) -> None:
        """Handler action when an incoming message is received

        Args:
            message (str): no action, only placeholder method
        """
        vid_stream_logger.debug("Ignoring message received from UI client.. ")


# obtain a reference to the logger utility
vid_stream_logger = log_helper.get_logger(component_name=VideoStreamHandler.__name__)
vid_stream_internal_logger = log_helper.get_logger(
    component_name=VideoStreamInternalHandler.__name__
)
# Initialize the config settings for Webapp api
config_handler = ConfigHandler()
l_config = config_handler.get_webapp_api_config()
