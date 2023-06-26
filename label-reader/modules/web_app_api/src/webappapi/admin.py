from src.util import log_helper
from tornado import websocket

l_logger = log_helper.get_logger()


class AdminInternal:
    """Handles life cycle events for WebSocket Connections for
    every label reader client

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
        if client_conn not in AdminInternal.label_reader_connections:
            AdminInternal.label_reader_connections.append(client_conn)
            msg = (
                f"label reader client for admin command messages {str(id(client_conn))} connected .. "
                + "len of connections: {len(AdminInternal.label_reader_connections)}"
            )
            l_logger.debug(msg)

    def removeClient(client_conn: websocket.WebSocketHandler) -> None:
        """Removes closed client connections

        Args:
            client_conn (websocket.WebSocketHandler): WebSocketHandler
        """
        msg = "label reader client for admin command messages {id} removed ..".format(
            id=str(id(client_conn))
        )
        if client_conn in AdminInternal.label_reader_connections:
            AdminInternal.label_reader_connections.remove(client_conn)
            l_logger.debug(msg)

    def getConnectedLabelReaders() -> list:
        """Returns the list of active WebSocket Client connections

        Returns:
            list: client connections list
        """
        return AdminInternal.label_reader_connections


class Admin:
    """Handles life cycle events for WebSocket Connections for
    every UI client

    Returns:
        _type_: NA
    """

    # Maintains reference to open WebSocket Client connections
    ui_connections = []

    def addClient(client_conn: websocket.WebSocketHandler) -> None:
        """adds this new Client connection to the in memory list

        Args:
            client_conn (websocket.WebSocketHandler):  WebSocketHandler
        """
        msg = "ui client for admin command messages - {id} - connected ..".format(
            id=str(id(client_conn))
        )
        if client_conn not in Admin.ui_connections:
            Admin.ui_connections.append(client_conn)
            l_logger.debug(msg)

    def removeClient(client_conn: websocket.WebSocketHandler) -> None:
        """Removes closed client connections

        Args:
            client_conn (websocket.WebSocketHandler):
                WebSocketHandler
        """
        msg = "ui client for admin command messages - {id} - removed ..".format(
            id=str(id(client_conn))
        )
        if client_conn in Admin.ui_connections:
            Admin.ui_connections.remove(client_conn)
            l_logger.debug(msg)

    def getConnectedUiClients() -> list:
        """Returns the list of active WebSocket Client connections

        Returns:
            list: client connections list
        """
        return Admin.ui_connections
