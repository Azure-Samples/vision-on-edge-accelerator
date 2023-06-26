from src.util import log_helper
from tornado import websocket


class OrderInfo:
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
        msg = "ui client for order info messages - {id} - connected ..".format(
            id=str(id(client_conn))
        )
        if client_conn not in OrderInfo.ui_connections:
            OrderInfo.ui_connections.append(client_conn)
            OrderInfo.l_logger.debug(msg)

    def removeClient(client_conn: websocket.WebSocketHandler) -> None:
        """Removes closed client connections

        Args:
            client_conn (websocket.WebSocketHandler):
                WebSocketHandler
        """
        msg = "ui client for order info messages - {id} - removed ..".format(
            id=str(id(client_conn))
        )
        if client_conn in OrderInfo.ui_connections:
            OrderInfo.ui_connections.remove(client_conn)
            OrderInfo.l_logger.debug(msg)

    def getConnectedLabelReaders() -> list:
        """Returns the list of active WebSocket Client connections

        Returns:
            list: client connections list
        """
        return OrderInfo.ui_connections


class OrderInfoInternal:
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
        if client_conn not in OrderInfoInternal.label_reader_connections:
            OrderInfoInternal.label_reader_connections.append(client_conn)
            msg = (
                f"label reader client for order info messages {str(id(client_conn))} connected .. "
                + "len of connections: {len(OrderInfoInternal.label_reader_connections)}"
            )
            OrderInfo.l_logger.debug(msg)

    def removeClient(client_conn: websocket.WebSocketHandler) -> None:
        """Removes closed client connections

        Args:
            client_conn (websocket.WebSocketHandler): WebSocketHandler
        """
        msg = "label reader client for order info messages {id} removed ..".format(
            id=str(id(client_conn))
        )
        if client_conn in OrderInfoInternal.label_reader_connections:
            OrderInfoInternal.label_reader_connections.remove(client_conn)
            OrderInfo.l_logger.debug(msg)

    def getConnectedLabelReaders() -> list:
        """Returns the list of active WebSocket Client connections

        Returns:
            list: client connections list
        """
        return OrderInfoInternal.label_reader_connections
