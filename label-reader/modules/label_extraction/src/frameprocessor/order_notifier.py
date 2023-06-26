"""This module is used to provide the order notifier class."""
import json

from src.common.socket_client import SocketClient


class OrderNotification:
    """
    Class for order notification model
    """

    def __init__(
        self,
        audio_byte: str,
        captured_frame: str,
        correlation_id: str,
        store_id: str,
        device_id: str,
        transformed_fields: dict[str, str],
    ) -> None:
        """
        Initialize the class

        @param
            audio_byte (str): encoded audio byte
            captured_frame (str): encoded captured frame
            correlation_id (str): correlation id
            store_id (str): store id
            device_id (str): device id
            transformed_result(dict(str,str)) : custom labels
        """
        self.audio_byte = audio_byte
        self.captured_frame = captured_frame
        self.correlation_id = correlation_id
        self.store_id = store_id
        self.device_id = device_id
        self.transformed_fields = transformed_fields


class OrderNotifier:
    """
    Class for sending order notification
    """

    def __init__(self, order_ws: SocketClient) -> None:
        """
        Initialize the class

        @param
            order_ws (SocketClient): order websocket client
        """
        self._order_ws = order_ws

    def notify_order(self, order_notification: OrderNotification) -> bool:
        """
        Send order notification

        @param
            order_notification (OrderNotification): order notification
        @return
            bool: True if order notification is sent successfully, False otherwise
        """
        return self._order_ws.send(
            json.dumps(order_notification, default=lambda o: o.__dict__)
        )
