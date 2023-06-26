import unittest
from unittest.mock import Mock
from src.frameprocessor.order_notifier import OrderNotification, OrderNotifier


class TestOrderNotifier(unittest.TestCase):
    def test_notify_order_called_once(self):
        order_ws = Mock()
        order_notifier = OrderNotifier(order_ws)
        transformed_fields = {
            "customer_name": "customer_name",
            "item_name": "item_name",
            "order_type": "order_type",
        }
        order_notification = OrderNotification(
            audio_byte="audio_byte",
            captured_frame="captured_frame",
            correlation_id="correlation_id",
            store_id="store_id",
            device_id="device_id",
            transformed_fields=transformed_fields,
        )
        order_notifier.notify_order(order_notification)
        order_ws.send.assert_called_once()
