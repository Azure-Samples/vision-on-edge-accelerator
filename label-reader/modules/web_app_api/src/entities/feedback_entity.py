

class FeedbackEntity(object):
    """Feedback Entity object that is passed by the UI Client as a string
    in the messge payload.

    """

    def __init__(
        self,
        order_type: str,
        order_number: str,
        captured_frame: str,
        correlation_id: str,
        device_id: str,
        store_id: str
    ) -> None:
        self.order_type = order_type
        self.store_id = store_id
        self.device_id = device_id
        self.correlation_id = correlation_id
        self.captured_frame = captured_frame
        self.order_number = order_number


class MetricsPayloadWrapper:
    """A wrapper object that wraps the Feedback object received
    from the UI Client, along with the url to the image uploaded
    to Blob Storage
    """

    def __init__(
        self,
        feedback_obj: FeedbackEntity,
        blob_name: str
    ) -> None:
        self.feedback_obj = feedback_obj
        self.blob_name = blob_name
