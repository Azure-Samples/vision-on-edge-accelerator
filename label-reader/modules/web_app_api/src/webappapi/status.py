from src.util import log_helper
from tornado import websocket


class Status:
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
        msg = "ui client for status messages - {id} - connected ..".format(
            id=str(id(client_conn))
        )
        if client_conn not in Status.ui_connections:
            Status.ui_connections.append(client_conn)
            Status.l_logger.debug(msg)

    def removeClient(client_conn: websocket.WebSocketHandler) -> None:
        """Removes closed client connections

        Args:
            client_conn (websocket.WebSocketHandler):
                WebSocketHandler
        """
        msg = "ui client for status messages - {id} - removed ..".format(
            id=str(id(client_conn))
        )
        if client_conn in Status.ui_connections:
            Status.ui_connections.remove(client_conn)
            Status.l_logger.debug(msg)

    def getConnectedLabelReaders() -> list:
        """Returns the list of active WebSocket Client connections

        Returns:
            list: client connections list
        """
        return Status.ui_connections


class StatusInternal:
    """Handles life cycle events for WebSocket Connections for
    every Label reader client

    Returns:
        _type_: NA
    """

    # Maintains reference to open WebSocket Client connections
    label_reader_connections = []

    def addClient(client_conn: websocket.WebSocketHandler) -> None:
        """adds this new Client connection to the in memory list

        Args:
            client_conn (websocket.WebSocketHandler):  WebSocketHandler
        """
        if client_conn not in StatusInternal.label_reader_connections:
            StatusInternal.label_reader_connections.append(client_conn)
            msg = (
                f"label client for status messages {str(id(client_conn))} connected .. "
                + "len of connections: {len(StatusInternal.label_reader_connections)}"
            )
            Status.l_logger.debug(msg)

    def removeClient(client_conn: websocket.WebSocketHandler) -> None:
        """Removes closed client connections

        Args:
            client_conn (websocket.WebSocketHandler):
                WebSocketHandler
        """
        msg = "label client for status messages {id} removed ..".format(
            id=str(id(client_conn))
        )
        if client_conn in StatusInternal.label_reader_connections:
            StatusInternal.label_reader_connections.remove(client_conn)
            Status.l_logger.debug(msg)

    def getConnectedLabelReaders() -> list:
        """Returns the list of active WebSocket Client connections

        Returns:
            list: client connections list
        """
        return StatusInternal.label_reader_connections
