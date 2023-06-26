
import unittest
from src.entities.feedback_entity import FeedbackEntity


class TestFeedbackEntity(unittest.TestCase):

    def test_feedback_entity_success(self):
        l_feedback_entity = FeedbackEntity('ordertype', 'order_number', 'captured frame',
                                           'correlation_id', 'device001', 'store01')
        self.assertEqual(l_feedback_entity.order_type, 'ordertype')
        self.assertEqual(l_feedback_entity.captured_frame, 'captured frame')
        self.assertEqual(l_feedback_entity.order_number, 'order_number')
        self.assertEqual(l_feedback_entity.correlation_id, 'correlation_id')
        self.assertEqual(l_feedback_entity.device_id, 'device001')
        self.assertEqual(l_feedback_entity.store_id, 'store01')
        print("Entity - Test feedback entity")
