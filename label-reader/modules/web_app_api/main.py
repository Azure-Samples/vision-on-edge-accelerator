from tornado import ioloop, web

from src.handlers import (
    admin_handler,
    feedback_handler,
    order_info_handler,
    status_handler,
    vid_stream_handler,
)
from src.util import log_helper

""" Design considerations that apply to this module
- Maintains connection state from different clients (i.e. UI and Label
    Reader components) using WebSockets
    - There is no limit on the number of clients that can connect to this
        component, though the current implementation requires
        one client connection each, from UI and Label Reader, respectively
- Relays messages between the Label Reader Component and UI Component
- Does not parse or validate incoming messages for well formedness, or
    schema adherence, etc. Validation of the messages
    would be handled by the UI and Label Reader components themselves
- About handling Client connections that drop & how reconnections are handled:
    - The Tornado framework raises events automatically when any client
        connection breaks, and the 'OnClose' method called
        that clears up the connection state. This was verified by manually
        terminating the client applications
    - Any other form of Client connection drops has not been tested/
        envisaged yet. Will be taken up when there are more details
        on how they can be simulated # TODO: simulate any additional scenarios
        for websocket connection failure?
- Handling compression of messages - no considerations implemented
    currently. # TODO: to be revisited in the subsequent iterations
- Handling CORS - presently the code permits cross origin requests -
    # TODO: to be revisited in the subsequent iterations
- No user authentication of clients trying to connect
- When there is an error relaying messages to a client over the socket
 connection, the error would be logged, but it is not required to return
 the error details to the call, except when the client is the UI Component
- All logged messages and text in the responses would be in English
"""

# identifier used for logging
component_name = "webapp_api"


class IndexHandler(web.RequestHandler):
    """Handler for the root endpoint for the application running on
    Tornado Web Server. Not used to handle requests

    Args:
        web (_type_): Request handler
    """

    def get(self):
        self.write("root endpoint")


app = web.Application(
    [
        (r"/", IndexHandler),
        (r"/ws/order_info_internal", order_info_handler.OrderInfoInternalHandler),
        (r"/ws/order_info", order_info_handler.OrderInfoHandler),
        (r"/ws/vid_stream_internal", vid_stream_handler.VideoStreamInternalHandler),
        (r"/ws/vid_stream", vid_stream_handler.VideoStreamHandler),
        (r"/ws/status", status_handler.StatusHandler),
        (r"/ws/status_internal", status_handler.StatusInternalHandler),
        (r"/ws/feedback", feedback_handler.FeedbackHandler),
        (r"/ws/admin_internal", admin_handler.AdminInternalHandler),
        (r"/ws/admin", admin_handler.AdminHandler),
    ]
)


if __name__ == "__main__":
    app.listen(7001)
    log_helper.get_logger(component_name=component_name).info(
        "Webapp api service starting ..."
    )
    ioloop.IOLoop.instance().start()
