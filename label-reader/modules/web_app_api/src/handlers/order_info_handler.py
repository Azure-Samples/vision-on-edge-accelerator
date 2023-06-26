from src.common.config_handler import ConfigHandler
from src.util import log_helper, message_sender
from src.util.message_sender import UseCaseScenarios
from src.webappapi.order_info import OrderInfo, OrderInfoInternal
from tornado import websocket


class OrderInfoHandler(websocket.WebSocketHandler):
    """Handler for WebSocket connections from UI Client
    (for Order Information)

    Args:
        websocket (_type_): WebSocketHandler for connections from
        UI Component

    Returns:
        _type_: NA
    """

    # Cross Origin requests is being allowed for now. Needs to be
    # revisited in subsequent iterations
    # overridden method from WebsocketHandler
    def check_origin(self, origin) -> bool:
        return True

    # overridden method from WebsocketHandler
    def open(self) -> None:

        # Set a no-wait indication when receiving messages
        # overridden method from WebsocketHandler
        self.set_nodelay(True)

        # add this connection to the in-memory list
        OrderInfo.addClient(self)

    # overridden method from WebsocketHandler
    def on_close(self) -> None:
        OrderInfo.removeClient(self)

    def get_compression_options(self):
        # Non-None enables compression with default options.
        if l_config.compression_is_enabled:
            order_info_logger.debug("Set default compression level for this connection")
            # compression level 6 is the default compression level..
            return {"compression_level": 6, "mem_level": 5}
        else:
            order_info_logger.debug("compression is disabled for this connection")
            return None

    # overridden method from WebsocketHandler
    def on_message(self, message: str) -> None:
        """Handler action when an incoming message is received

        Args:
            message (str): incoming message - there is no requirement
            to receive a message here, and it's merely a placeholder
        """
        order_info_logger.debug("Unexpected message received from UI client, ignoring")


"""Handler for WebSocket connections from Label Reader, to receive Order
    Information that is sent to the UI component
"""


class OrderInfoInternalHandler(websocket.WebSocketHandler):
    """Handler for WebSocket connections from label reader component
    (for Order Information)

    Args:
        websocket (_type_): WebSocketHandler for connections from
        label reader

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

        # add this connection to the in-memory list
        OrderInfoInternal.addClient(self)

    # overridden method from WebsocketHandler
    def on_close(self) -> None:
        OrderInfoInternal.removeClient(self)

    def get_compression_options(self):
        # Non-None enables compression with default options.
        if l_config.compression_is_enabled:
            order_info__internal_logger.debug(
                "Set default compression level for this connection"
            )
            # compression level 6 is the default compression level..
            return {"compression_level": 6, "mem_level": 5}
        else:
            order_info__internal_logger.debug(
                "compression is disabled for this connection"
            )
            return None

    # overridden method from WebsocketHandler

    def on_message(self, message: str) -> None:
        """Handler action when an incoming message is received

        message (str): incoming message from the UI Component
        """
        # Get the UI Clients that are waiting to get the Order info
        allClients = OrderInfo.getConnectedLabelReaders()

        # relay the incoming message to the UI Component
        acknowledgement = message_sender.send_message(
            allClients, UseCaseScenarios.OrderInformationToUi.value, message, False
        )
        if acknowledgement.outcome is False:
            """This is sent as a separate message, back to
            the caller, and not as a response to the original msg
            """
            self.write_message(
                f" Error relaying the message to the client - {acknowledgement.msg_out_error}"
            )


# Obtain a reference to the Logger utility
order_info_logger = log_helper.get_logger(component_name=OrderInfoHandler.__name__)
order_info__internal_logger = log_helper.get_logger(
    component_name=OrderInfoInternalHandler.__name__
)
# Initialize the config settings for Webapp api
config_handler = ConfigHandler()
l_config = config_handler.get_webapp_api_config()
