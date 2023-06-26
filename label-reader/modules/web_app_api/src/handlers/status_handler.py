from src.common.config_handler import ConfigHandler
from src.util import log_helper, message_sender
from src.util.message_sender import UseCaseScenarios
from src.webappapi.status import Status, StatusInternal
from tornado import websocket


class StatusInternalHandler(websocket.WebSocketHandler):
    """Handler for WebSocket connections from label reader component
    (for status Information)

    Args:
        websocket (_type_): WebSocketHandler for  connections from
        label reader

    Returns:
        _type_: NA
    """

    # Cross Origin requests is being allowed for now. Needs to be revisited in
    # subsequent sprints
    # overridden method from WebsocketHandler

    def check_origin(self, origin) -> bool:
        return True

    # overridden method from WebsocketHandler
    def open(self) -> None:

        # Set a no-wait indication when receiving messages
        # overridden method from WebsocketHandler
        self.set_nodelay(True)

        # overridden method from WebsocketHandler
        # add this connection to the in-memory list
        StatusInternal.addClient(self)

    # overridden method from WebsocketHandler
    def on_close(self) -> None:
        StatusInternal.removeClient(self)

    def get_compression_options(self):
        # Non-None enables compression with default options.
        if l_config.compression_is_enabled:
            status_internal_logger.debug(
                "Set default compression level for this connection"
            )
            # compression level 6 is the default compression level..
            return {"compression_level": 6, "mem_level": 5}
        else:
            status_internal_logger.debug("compression is disabled for this connection")
            return None

    # overridden method from WebsocketHandler
    def on_message(self, message: str) -> None:
        """Handler action when an incoming message is received

        Args:
            message (str): message to be relayed
        """
        # Get the UI Clients that are waiting to get the status info
        allClients = Status.getConnectedLabelReaders()

        # relay the message to the listening clients
        error_indicator = message_sender.send_message(
            allClients, UseCaseScenarios.StatusInformationToUi.value, message, False
        )
        if error_indicator.outcome is False:
            """This is sent as a separate message, back to
            the caller, and not as a response to the original msg
            """
            self.write_message(
                f" Error relaying the message to the client - {error_indicator.msg_out_error}"
            )


class StatusHandler(websocket.WebSocketHandler):
    """Handler for WebSocket connections from UI component
    (for status Information)

    Args:
        websocket (_type_): WebSocketHandler for connections from
        UI Component

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

        # overridden method from WebsocketHandler
        # Set a no-wait indication when receiving messages
        self.set_nodelay(True)

        # add this connection to the in-memory list
        Status.addClient(self)

    # overridden method from WebsocketHandler
    def on_close(self) -> None:
        Status.removeClient(self)

    def get_compression_options(self):
        # Non-None enables compression with default options.
        if l_config.compression_is_enabled:
            status_logger.debug("Set default compression level for this connection")
            # compression level 6 is the default compression level..
            return {"compression_level": 6, "mem_level": 5}
        else:
            status_logger.debug("compression is disabled for this connection")
            return None

    # overridden method from WebsocketHandler
    def on_message(self, message: str) -> None:
        """meant to relay messages, but not required in this use case

        Args:
            message (str): message to relay
        """
        status_logger.debug("Unexpected message received from UI client, ignoring")


# obtain a reference to the logger utility
status_logger = log_helper.get_logger(component_name=StatusHandler.__name__)
status_internal_logger = log_helper.get_logger(
    component_name=StatusInternalHandler.__name__
)
# Initialize the config settings for Webapp api
config_handler = ConfigHandler()
l_config = config_handler.get_webapp_api_config()
