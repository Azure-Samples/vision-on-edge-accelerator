import time
import unittest
from unittest.mock import patch
from src.common.socket_client import SocketClient

SOCKET_TEST_URL = "wss://ws.postman-echo.com/raw"


class TestSocketClient(unittest.TestCase):
    def test_send_should_return_False_if_connection_is_broken(self):
        socket_client = SocketClient(SOCKET_TEST_URL)
        socket_client.connect()
        socket_client.start_dispatcher()
        time.sleep(0.1)
        self.assertTrue(socket_client.send("test"))
        socket_client.ws.sock.abort()
        self.assertFalse(socket_client.send("test"))

    def test_reconnect_should_start_new_socket_connection(self):
        socket_client = SocketClient(SOCKET_TEST_URL, reconnection_interval=0.1)
        socket_client.connect()
        socket_client.start_dispatcher()
        time.sleep(0.1)
        self.assertTrue(socket_client.send("test"))

        old_ws = socket_client.ws
        socket_client.reconnect()
        new_ws = socket_client.ws

        self.assertTrue(socket_client.send("test"))
        self.assertFalse(old_ws is new_ws)

    def test_reconnect_should_log_exception_and_reconnect_if_error_happens(self):
        socket_client = SocketClient(SOCKET_TEST_URL, reconnection_interval=0.1)
        socket_client.connect()
        socket_client.start_dispatcher()
        time.sleep(0.1)
        self.assertTrue(socket_client.send("test"))

        old_ws = socket_client.ws
        with patch.object(socket_client.ws, "sock") as mock_socket:
            mock_socket.close.side_effect = Exception("test")
            mock_socket.connected = False
            socket_client.reconnect()
            new_ws = socket_client.ws
            # failing sometime due to network issues
            # time.sleep(0.3)
            # socket_client.ws.sock.connected = True
            # self.assertTrue(socket_client.send("test"))
            self.assertFalse(old_ws is new_ws)

    @patch("src.common.socket_client.websocket.WebSocketApp.send")
    def test_send_reconnect_if_socket_is_not_connected(self, ws_send_mock):
        socket_client = SocketClient(SOCKET_TEST_URL, reconnection_interval=0.1)
        socket_client.connect()
        socket_client.start_dispatcher()
        time.sleep(0.1)
        socket_client.ws.sock.close()
        time.sleep(0.1)
        socket_client.send("")
        ws_send_mock.assert_called_once()
