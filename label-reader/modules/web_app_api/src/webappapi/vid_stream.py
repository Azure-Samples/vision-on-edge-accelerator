from src.util import log_helper
from tornado import websocket


class VideoStream:
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
        msg = "ui client for video frame messages - {id} - connected ..".format(
            id=str(id(client_conn))
        )
        if client_conn not in VideoStream.ui_connections:
            VideoStream.ui_connections.append(client_conn)
            VideoStream.l_logger.debug(msg)

    def removeClient(client_conn: websocket.WebSocketHandler) -> None:
        """Removes closed client connections

        Args:
            client_conn (websocket.WebSocketHandler):
                WebSocketHandler
        """
        msg = "ui client for video frame messages - {id} - removed ..".format(
            id=str(id(client_conn))
        )
        if client_conn in VideoStream.ui_connections:
            VideoStream.ui_connections.remove(client_conn)
            VideoStream.l_logger.debug(msg)

    def getConnectedLabelReaders() -> list:
        """Returns the list of active WebSocket Client connections

        Returns:
            list: client connections list
        """
        return VideoStream.ui_connections


class VideoStreamInternal:
    """Handles life cycle events for WebSocket Connections for
    every Label Reader Client

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
        if client_conn not in VideoStreamInternal.label_reader_connections:
            VideoStreamInternal.label_reader_connections.append(client_conn)
            msg = (
                f"label reader client for video frame messages {str(id(client_conn))} connected .. "
                + "len of connections: {len(VideoStreamInternal.label_reader_connections)}"
            )
            VideoStream.l_logger.debug(msg)

    def removeClient(client_conn: websocket.WebSocketHandler) -> None:
        """Removes closed client connections

        Args:
            client_conn (websocket.WebSocketHandler):
                WebSocketHandler
        """
        msg = "label reader client for video frame messages {id} removed ..".format(
            id=str(id(client_conn))
        )
        if client_conn in VideoStreamInternal.label_reader_connections:
            VideoStreamInternal.label_reader_connections.remove(client_conn)
            VideoStream.l_logger.debug(msg)

    def getConnectedLabelReaders() -> list:
        """Returns the list of active WebSocket Client connections

        Returns:
            list: client connections list
        """
        return VideoStreamInternal.label_reader_connections
