from enum import Enum
import json


class MessageOutResponse:
    """The response to Message send action to a Websocket client. It wraps a flag
    that indicates the success/failure status, and the details of any error that occured
    """

    def __init__(self,
                 outcome: bool,
                 msg_out_error:  Enum
                 ):
        """initializes a response object to return to the caller of Message Send
        action

        Args:
            outcome (bool): success(True) or failure(False) indicator
            msg_out_error (Enum): Error code depending on the nature of the
            Exception
        """
        self.outcome = outcome
        self.msg_out_error = msg_out_error


class MessageOutErrors(Enum):
    """Error codes when sending a message to Websocket Client

    Args:
        Enum (_type_): Error code - name and value to return
    """
    ioCancelledError = 2
    WebSocketClosedError = 1
    NoClientsConnected = 3


def acknowledgement():
    """The response to Message send action to a Websocket client. It wraps a flag
    that indicates the success/failure status, and the details of any error that occured

    Returns:
        json string: the acknowledgement message to be sent to the web socket client
    """
    l_ack_msg = {}
    l_ack_msg["outcome"] = "success"
    l_ack_msg["detail"] = "feedback received"
    return json.dumps(l_ack_msg)
