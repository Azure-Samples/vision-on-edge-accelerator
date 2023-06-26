import unittest

from src.common import metrics_logger
from src.common.metrics_logger import MetricsLogger
from src.entities.feedback_entity import FeedbackEntity, MetricsPayloadWrapper


class TestMetricsWrapperEntity(unittest.TestCase):

    def test_wrapper_entity_success(self):

        l_feedback_entity = FeedbackEntity('ordertype', 'order_number', 'captured frame',
                                           'correlation_id', 'device001', 'store01')

        l_wrapper_entity = MetricsPayloadWrapper(l_feedback_entity, 'dummy_name')
        self.assertEqual(l_wrapper_entity.blob_name, 'dummy_name')
        self.assertEqual(l_wrapper_entity.feedback_obj.captured_frame, 'captured frame')
        self.assertEqual(l_wrapper_entity.feedback_obj.order_number, 'order_number')
        self.assertEqual(l_wrapper_entity.feedback_obj.correlation_id, 'correlation_id')
        self.assertEqual(l_wrapper_entity.feedback_obj.device_id, 'device001')
        self.assertEqual(l_wrapper_entity.feedback_obj.store_id, 'store01')
        print("MetricsWrapper - Test - verify init Entity")

    def test_verify_metric_logger(self):
        self.assertIsNot(metrics_logger.l_metrics_logger, None)
        print("MetricsLogger - Test - verify metric logger")

    def test_verify_metric_logger_success(self):
        l_feedback_entity = FeedbackEntity('ordertype', 'order_number', 'captured frame',
                                           'correlation_id', 'device001', 'store01')
        l_wrapper_entity = MetricsPayloadWrapper(l_feedback_entity, 'dummy_url')
        resp = MetricsLogger().log_metrics_for_user_feedback(l_wrapper_entity.feedback_obj, l_wrapper_entity.blob_name)
        self.assertIs(resp, None)
        print("MetricsLogger - Test - verify metric logger success")
