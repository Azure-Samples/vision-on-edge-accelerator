"""This module is used to provide the socket client for WebAppApi."""
import socket
import threading
import time
from typing import Any, Callable
import websocket
from src.common.log_helper import get_logger
import rel


class SocketClient:
    """
    Socket client to interact with WebAppApi.
    """

    def on_message(self, ws, message):
        """
        Callback for websocket on message.

        @param
            ws (websocket): websocket object
            message (Any): message received from websocket
        """
        if self.on_message_received is not None:
            self.on_message_received(message)

    def on_error(self, ws, error):
        """
        Callback for websocket on error, that recconects the websocket.

        @param
            ws (websocket): websocket object
            error (Any): error received from websocket
        """
        self.logger.warning(
            f"Websocket connection ERROR for url: {self.url} error:{error}"
        )
        self.logger.exception(error)
        self.reconnect()

    def on_close(self, ws, close_status_code, close_msg):
        """
        Callback for websocket on close, that reconnects the websocket.

        @param
            ws (websocket): websocket object
            close_status_code (int): close status code
            close_msg (bytes): close message
        """
        self.logger.warning(
            f"Websocket connection CLOSED for url: {self.url} close_status_code:{close_status_code} close_msg:{close_msg}"
        )
        self.reconnect()

    def on_open(self, ws):
        """
        Callback for websocket on open.

        @param
            ws (websocket): websocket object
        """
        self.logger.info(f"Websocket connection OPENED for url: {self.url}")

    def __init__(
        self,
        url: str,
        enable_tracing=False,
        reconnection_interval: int = 3,
        ping_interval: int = 0,
        ping_timeout: int = None,
        on_message: Callable[[Any], None] = None,
    ):
        """
        Initialize the socket client.

        @param
            url (str): url to connect to
            enable_tracing (bool): enable tracing
            reconnection_interval (int): reconnection interval
            ping_interval (int): ping interval
            ping_timeout (int): ping timeout
            on_message (Callable[[Any], None]): callback for on message
        """
        self.url = url
        self.on_message_received = on_message
        self.logger = get_logger(component_name=SocketClient.__name__)
        self.reconnection_interval = reconnection_interval
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        websocket.enableTrace(enable_tracing)
        self.ws = None
        self._lock_reconnect = threading.Lock()
        self.dispatcher_thread = None

    def connect(self) -> websocket.WebSocketApp:
        """
        Connect to the websocket.

        @return
            websocket.WebSocketApp: websocket app object
        """
        self._lock_reconnect.acquire(blocking=True, timeout=3)
        if not self.ws or not self.ws.sock or not self.ws.sock.connected:
            # TODO: Add socks options like compresion, etc.
            self.ws = websocket.WebSocketApp(
                self.url,
                on_open=self.on_open,
                on_error=self.on_error,
                on_close=self.on_close,
                on_message=self.on_message,
            )
            return self.ws.run_forever(
                sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),),
                dispatcher=rel,
                skip_utf8_validation=True,
                ping_interval=self.ping_interval,
                ping_timeout=self.ping_timeout,
            )
        self._lock_reconnect.release()

    def reconnect(self) -> None:
        """
        Reconnect the websocket.
        """
        self.logger.warning(f"Websocket connection RECONNECTING for url: {self.url}")

        try:
            if self.ws.sock and self.ws.sock.connected:
                self.ws.sock.close(
                    status=websocket.STATUS_GOING_AWAY,
                    reason=b"reconnecting",
                    timeout=3,
                )
        except Exception as e:
            self.logger.warning(
                f"Websocket RECONNECTING for url: {self.url}. Underlying socket close exception:{e}"
            )
            self.logger.exception(e)

        time.sleep(self.reconnection_interval)
        self.connect()

    def send(self, message: Any, opcode: int = websocket.ABNF.OPCODE_TEXT) -> bool:
        """
        Send message to the websocket.

        @param
            message (Any): message to send
            opcode (int): opcode to send
        """
        if not self.ws.sock or not self.ws.sock.connected:
            self.logger.warn(f"Websocket connection NOT CONNECTED for url: {self.url}")
            self.reconnect()
        try:
            self.ws.send(message, opcode)
            return True
        except Exception as e:
            self.logger.warning(
                f"FAILED sending message in websocket for url: {self.url}, Exception: {e}"
            )
            self.logger.exception(e)
            self.reconnect()
            return False

    def start_dispatcher(self) -> None:
        """
        Start the websocket dispatcher, need to called once.

        If called more than once, only for first call dispatcher will be running
            and for rest reconnecting will not happen.
        """
        rel.safe_read()
        self.dispatcher_thread = threading.Thread(
            target=lambda: self._dispatch(self.reconnect)
        )
        self.dispatcher_thread.daemon = True
        self.dispatcher_thread.start()

    def _dispatch(self, reconnect: Callable) -> None:
        """
        Wrapper for rel dispather.

        @param
            reconnect (Callable): reconnect function
        """
        _alive = True
        while _alive:
            _alive = False
            try:
                self.logger.warning(
                    f"Websocket dispatcher STARTING for url: {self.url}"
                )
                rel.dispatch()
                self.logger.warning(f"Websocket dispatcher STOPPED for url: {self.url}")
            except Exception as e:
                self.logger.error(
                    f"Websocket dispatcher EXCEPTION for url: {self.url} exception: {e}"
                )
                self.logger.exception(e)
                self.logger.warning(
                    f"Websocket dispatcher RESTARTING for url: {self.url}"
                )
                """
                Currently this will only reconnect the socket that is owned by this class.
                If there are other websockets in same python process, those will not reconnect.

                To handle this, main a map of url, websocket objects and reconnect all of them.
                """
                reconnect()
                rel.rel.running = False
                _alive = True


# if __name__ == "__main__":
#     ws = SocketClient("wss://api.gemini.com/v1/marketdata/BTCUSD", enable_tracing=False)
#     ws.connect()
#     threading.Timer(interval=5, function=ws.ws.close).start()
#     # rel.dispatch()
#     SocketClient.start_dispatcher()
#     # t.join()
#     while True:
#         time.sleep(1)
