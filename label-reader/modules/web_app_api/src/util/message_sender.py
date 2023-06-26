import asyncio
from enum import Enum

from src.entities.response_msg import MessageOutErrors, MessageOutResponse
from src.util import log_helper
from tornado import websocket

l_logger = log_helper.get_logger()

""" Generic method used by all handlers to send messages to open,
    WebSocket client connections after performing some basic validation
    steps
"""


def send_message(
    allRecipientConnection: list,
    usecase: str,
    message: str,
    binary: bool,
) -> MessageOutResponse:
    """Generic method used by all handlers to send messages to open,
    WebSocket client connections after performing some basic validation
    steps.
    Args:
        allRecipientConnection (list): target active Websocket Clients
        message (string): The message to send WebSocket Clients
        usecase (string): The use case scenario to which this message applies
        binary (bool): If False message will be sent as utf-8 otherwise any byte string is allowed.
    Returns:
        MessageOutResponse: Flag to indicate to the 'sender' of the original
        message, a success/failure status, and details of errors on failure
    """
    if len(allRecipientConnection) == 0:
        # l_logger.warning("No connected clients found for " + usecase)
        return MessageOutResponse(False, MessageOutErrors.NoClientsConnected)

    # Get list of listening Client WebSocket Connections
    for l_handler in allRecipientConnection:
        try:
            l_handler.write_message(message, binary=binary)
            # Empty string to indicate there is no error
        except asyncio.CancelledError as ioCancelledError:
            l_logger.error(f"Error relaying - {usecase}, {ioCancelledError}")
            # print("io Error sending message- use case " + repr(ioCancelledError))
            # generate an error message
            return MessageOutResponse(False, MessageOutErrors.ioCancelledError)
        except websocket.WebSocketClosedError as wsockError:
            l_logger.error(f"Error relaying - {usecase}, {wsockError}")
            # print("Socket closed Error sending message- use case " + repr(wsockError))
            # generate an error message
            return MessageOutResponse(False, MessageOutErrors.WebSocketClosedError)
    return MessageOutResponse(True, None)


class UseCaseScenarios(Enum):
    """Use case scenario names that the Webapp api caters to; used for purpose of logging

    Args:
        Enum (_type_): usecase value
    """

    AdminCommandsFromUi = "Admin Command From UI"
    AdminCommandResponsesToUi = "Admin Command responses to UI"
    OrderInformationToUi = "order information to UI"
    StatusInformationToUi = "status information to UI"
    VideoStreamToUi = "video stream to UI"
