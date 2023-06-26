from tornado.websocket import websocket_connect
from tornado.testing import AsyncHTTPTestCase, gen_test
from src.handlers.order_info_handler import OrderInfoHandler, OrderInfoInternalHandler
from tornado.concurrent import Future
from tornado.web import Application
import json
from src.util.config import WebappApiConfig

"""tornado testing framework runs the HTTP Server to execute the test cases on
It plumbs all requests to the respective handler code

Returns:
    _type_: _description_
"""


class WebSocketBaseTestCase(AsyncHTTPTestCase):
    async def ws_connect(self, path, **kwargs):
        ws = await websocket_connect(
            "ws://127.0.0.1:%d%s" % (self.get_http_port(), path), **kwargs
        )
        return ws


class WebSocketTest(WebSocketBaseTestCase):

    rel_path_target = "/ws/order_info"
    rel_path_source = "/ws/order_info_internal"

    def get_app(self):
        self.close_future = Future()  # type: Future[None]
        return Application(
            [
                (self.rel_path_target, OrderInfoHandler),
                (self.rel_path_source, OrderInfoInternalHandler),
            ],
        )

    @gen_test
    async def test_simple_source_to_target(self):
        """Tests the simple scenario where one source websocket client
        sends a simple message to a single target websocket client

        Yields:
            _type_: _description_
        """
        msg_1 = "hello test message"
        ws_source = await self.ws_connect(self.rel_path_source)
        ws_target = await self.ws_connect(self.rel_path_target)

        await ws_source.write_message(msg_1)
        response = await ws_target.read_message()
        ws_source.close()
        ws_target.close()
        self.assertEqual(response, msg_1)
        print("OrderInfoHandler - Test - source with single target")

    @gen_test
    async def test_empty_msg_source_to_target(self):
        """Tests the simple scenario where one source websocket client
        sends a empty string message to a single target websocket client

        Yields:
            _type_: _description_
        """
        msg_1 = ""
        ws_source = await self.ws_connect(self.rel_path_source)
        ws_target = await self.ws_connect(self.rel_path_target)

        await ws_source.write_message(msg_1)
        response = await ws_target.read_message()
        ws_source.close()
        ws_target.close()
        self.assertEqual(response, msg_1)
        print(
            "OrderInfoHandler - Test - source with single target - empty string message"
        )

    @gen_test
    async def test_fullmsg_source_to_target(self):
        """Tests the scenario where one source websocket client
        sends a complete message to a single target websocket client

        Yields:
            _type_: _description_
        """
        msg_1 = order_info_string
        ws_source = await self.ws_connect(self.rel_path_source)
        ws_target = await self.ws_connect(self.rel_path_target)

        await ws_source.write_message(msg_1)
        response = await ws_target.read_message()
        ws_source.close()
        ws_target.close()
        self.assertEqual(response, msg_1)
        print("OrderInfoHandler - Test - full msg - source with single target")

    @gen_test
    async def test_simple_source_no_targets(self):
        """Tests the simple scenario where one source websocket client
        sends a message and there are no target websocket clients connected

        Yields:
            _type_: _description_
        """
        ws_source = await self.ws_connect(self.rel_path_source)
        await ws_source.write_message("hello")
        response = await ws_source.read_message()
        if response is not None:
            try:
                js_response = json.loads(response)
                print("json response ", js_response)
                ws_source.close()
                self.assertEqual(js_response["is_error"], "true")
            except Exception as ex:
                print("Exception parsing the response", ex.args)
        print("OrderInfoHandler - Test - source with no targets")

    @gen_test
    async def test_simple_source_multiple_targets(self):

        """Tests the simple scenario where one source websocket client
        sends a message and there are multiple target websocket clients connected

        Yields:
            _type_: _description_
        """

        msg_1 = "one source multiple targets propagate"
        ws_source = await self.ws_connect(self.rel_path_source)
        num_targets = 3
        all_target_connections = []
        for i in range(0, num_targets):
            ws_target = await self.ws_connect(self.rel_path_target)
            all_target_connections.append(ws_target)

        await ws_source.write_message(msg_1)
        ws_source.close()
        for ws_target in all_target_connections:
            response = await ws_target.read_message()
            ws_target.close()
            self.assertEqual(response, msg_1)
        print("OrderInfoHandler - Test - source with multiple targets")

    @gen_test
    async def test_simple_source_verify_uncompressed(self):
        """Tests the simple scenario where one source websocket client
        sends a message but there are no target websocket clients connected
        and the message is uncompressed
        Yields:
            _type_: _description_
        """
        wapi_config = WebappApiConfig()
        wapi_config.disable_compression()
        print("disabled compression on the singleton")
        ws = await self.ws_connect(self.rel_path_source)
        await ws.write_message("hello")
        response = await ws.read_message()
        if response is not None:
            try:
                js_response = json.loads(response)
                ws.close()
                print("json response ", js_response)
                self.assertEqual(js_response["is_error"], "true")
            except Exception as ex:
                print("Exception parsing the response", ex.args)
        print("OrderInfoHandler - Test - disabled compression")
        wapi_config.enable_compression()

    @gen_test
    async def test_simple_target_verify_uncompressed(self):
        """Tests the simple scenario where one source websocket client
        sends a message but there are no target websocket clients connected
        and the message is uncompressed
        Yields:
            _type_: _description_
        """
        wapi_config = WebappApiConfig()
        wapi_config.disable_compression()
        print("disabled compression on the singleton")
        ws = await self.ws_connect(self.rel_path_target)
        resp = await ws.write_message("hello")
        self.assertEqual(resp, None)
        print("OrderInfoHandler - Test - disabled compression on target")


order_info_string = (
    "{"
    + '"order_type": "啡快",'
    + '"order_number": "35974",'
    + '"pickup_phrase": "啡快,online order for pick up at store",'
    + '"item_name": "大/热榛果拿铁",'
    + '"captured_frame": "/9j/4AAQSkZJ,'
    + '"audio_byte": "jhjkhjhjhjkhkj",'
    + '"correlation_id": "ABCDEFG9802312",'
    + '"device_id": "DEV0101",'
    + '"store_id": "STORE0101"'
    + "}"
)


# if __name__ == "__main__":
#     unittest.main()
