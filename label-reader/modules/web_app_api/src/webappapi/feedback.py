from src.util import log_helper
from tornado import websocket


class Feedback:
    """Handles life cycle events for WebSocket Connections for
    every UI client

    Returns:
        _type_: NA
    """

    # Maintains reference to open WebSocket Client connections
    ui_connections = []

    l_logger = log_helper.get_logger()

    def addClient(client_conn: websocket.WebSocketHandler) -> None:
        """adds this new Client connection to the in memory list

        Args:
            client_conn (websocket.WebSocketHandler):  WebSocketHandler
        """
        msg = 'ui client for user feedback messages {id} connected..'\
            .format(id=str(id(client_conn)))
        if client_conn not in Feedback.ui_connections:
            Feedback.ui_connections.append(client_conn)
            Feedback.l_logger.debug(msg)

    def removeClient(client_conn: websocket.WebSocketHandler) -> None:
        """Removes closed client connections

        Args:
            client_conn (websocket.WebSocketHandler): WebSocketHandler
        """
        msg = 'ui client for user feedback messages {id} removed..'\
            .format(id=str(id(client_conn)))
        if client_conn in Feedback.ui_connections:
            Feedback.ui_connections.remove(client_conn)
            Feedback.l_logger.debug(msg)

    def getConnectedLabelReaders() -> list:
        """Returns the list of active WebSocket Client connections

        Returns:
            list: client connections list
        """
        return Feedback.ui_connections
