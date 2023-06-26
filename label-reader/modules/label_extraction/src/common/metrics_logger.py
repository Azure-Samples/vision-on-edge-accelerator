from logging import Logger


class MetricsLogger:
    """
    This class is used to log metrics for latency & DS Model performance to App Insights.
    """

    def __init__(self, logger: Logger) -> None:
        """Constructor for the MetricsLogger class
        @param logger: Logger object to emit metrics to App Insights
        """
        self.l_metrics_logger = logger

    def log_latency_metrics(self, latency_metrics: dict) -> None:
        """
        This method is used to log latency metrics!
        @param
            latency_metrics{dict}: latency metrics to log

        @return: None

        """
        self.l_metrics_logger.info(
            "Latency Metric",
            extra=latency_metrics,
        )

    def log_ds_model_metrics(self, metrics_payload: dict):
        """
        This method is used to log ds model metrics
        @param metrics_payload: {dict} object to emit

        @return: None
        """
        self.l_metrics_logger.info(
            "Model Metric",
            extra=metrics_payload,
        )
