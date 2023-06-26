from tornado.websocket import websocket_connect
from tornado.testing import AsyncHTTPTestCase, gen_test
from src.handlers.feedback_handler import FeedbackHandler
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

    rel_path_source = "/ws/feedback"

    def get_app(self):
        self.close_future = Future()  # type: Future[None]
        return Application(
            [
                (self.rel_path_source, FeedbackHandler),
            ],
        )

    @gen_test
    async def test_simple_source_no_target(self):
        """Tests the scenario where one source websocket client
        sends a feedback message and sends an acknowledgement back

        Yields:
            _type_: _description_
        """
        ws = await self.ws_connect(self.rel_path_source)
        await ws.write_message("hello")
        response = await ws.read_message()
        if response is not None:
            try:
                js_response = json.loads(response)
                ws.close()
                print("json response ", js_response)
                self.assertEqual(js_response["outcome"], "success")
            except Exception as ex:
                print("Exception parsing the response", ex.args)
        print("FeedbackHandler - Test verify on-message is called")

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
        print("FeedbackHandler - Test - disabled compression")
        wapi_config.enable_compression()


feedback_string = (
    "{"
    + '"order_type": "啡快",'
    + '"order_number": "35974",'
    + '"captured_frame": "/9j/4AAQSkZJRgABAQAAAQABAA'
    + '"correlation_id": "ABCDEFG9802312",'
    + '"device_id": "DEV0101",'
    + '"store_id": "STORE0101"'
    + "}"
)

# if __name__ == "__main__":
#     unittest.main()
