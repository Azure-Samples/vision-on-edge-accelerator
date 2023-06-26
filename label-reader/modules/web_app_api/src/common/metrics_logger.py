from src.entities.feedback_entity import FeedbackEntity
from src.util import log_helper


class MetricsLogger:
    """
    This class is used to log metrics for user feedback to App Insights
    """

    def __init__(self):
        pass

    @staticmethod
    def log_metrics_for_user_feedback(
        metrics_dict: FeedbackEntity, blob_name: str
    ) -> None:
        """
        This method is used to log custom metrics for the web app api
        :param metrics_dict: Metrics Entity object for User Feedback
        :param blob_name: Blob id/name of the uploaded image
        :return: None
        """

        # the device id is excluded here, since the logger init already includes this property in custom dimensions
        l_metrics_logger.info(
            "User Feedback captured from UI",
            extra={
                "custom_dimensions": {
                    "store_id": metrics_dict.store_id,
                    "correlation_id": metrics_dict.correlation_id,
                    "order_type": metrics_dict.order_type,
                    "order_number": metrics_dict.order_number,
                    "evaluation_type": "user",
                    "frame_blob_id": blob_name,
                }
            },
        )


# Acquire a reference to the Logger for metrics
l_metrics_logger = log_helper.get_logger(component_name=MetricsLogger.__name__)
