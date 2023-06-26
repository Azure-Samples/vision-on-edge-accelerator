from unittest.mock import patch, MagicMock
import unittest
from src.util import message_sender
from src.entities.response_msg import MessageOutResponse
import asyncio
from tornado import websocket


class EchoWebSocket(websocket.WebSocketHandler):
    """Utility Handler class that is used to unit test Message sender

    Args:
        websocket (_type_): _description_
    """

    def open(self):
        print("WebSocket opened")


class TestMessageSender(unittest.TestCase):

    @patch('tornado.websocket.WebSocketHandler.write_message')
    def test_MessageSenderIoCancelledError(self, mocka):
        mocka.side_effect = asyncio.CancelledError()
        conn_obj = EchoWebSocket(MagicMock(), MagicMock())
        conn_obj.open()
        dummylist = []
        dummylist.append(conn_obj)
        mock_response = message_sender.send_message(dummylist, MagicMock(), MagicMock(), MagicMock())
        # print('*******************',mock_response.msg_out_error)
        self.assertEquals(mock_response.msg_out_error.name, 'ioCancelledError')
        self.assertEquals(mock_response.outcome, False)
        conn_obj.close()
        print("MessageSender -Test trigger IO cancelled error")

    @patch('tornado.websocket.WebSocketHandler.write_message')
    def test_MessageSenderWebsocketClosedError(self, mocka):
        mocka.side_effect = websocket.WebSocketClosedError()
        conn_obj = EchoWebSocket(MagicMock(), MagicMock())
        conn_obj.open()
        dummylist = []
        dummylist.append(conn_obj)
        mock_response = message_sender.send_message(dummylist, MagicMock(), MagicMock(), MagicMock())
        # print('*******************',mock_response.msg_out_error)
        self.assertEquals(mock_response.msg_out_error.name, 'WebSocketClosedError')
        self.assertEquals(mock_response.outcome, False)
        conn_obj.close()
        print("MessageSender -Test trigger websocket error")

    @patch('tornado.websocket.WebSocketHandler.write_message')
    def test_MessageSenderNoClientsConnectedError(self, mocka):
        mock_response = message_sender.send_message(MagicMock(), 'test use case', 'test message', True)
        self.assertEquals(mock_response.msg_out_error.name, 'NoClientsConnected')
        self.assertEquals(mock_response.outcome, False)
        print("MessageSender -Test trigger no clients connected error")

    @patch('tornado.websocket.WebSocketHandler.write_message')
    def test_MessageSenderSuccessPath(self, mocka):
        conn_obj = EchoWebSocket(MagicMock(), MagicMock())
        conn_obj.open()
        dummylist = []
        dummylist.append(conn_obj)
        mocka.return_value = MessageOutResponse(True, None)
        mock_response = message_sender.send_message(dummylist, 'test use case', 'test message', True)
        self.assertEquals(mock_response.outcome, True)
        conn_obj.close()
        print("MessageSender -Test send message success path")
