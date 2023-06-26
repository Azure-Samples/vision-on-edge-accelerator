"""This module is used to log traces into Azure Application Insights."""
import logging
import uuid
from os import getenv

from opencensus.ext.azure.common import utils
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace import config_integration
from opencensus.trace.samplers import AlwaysOffSampler, AlwaysOnSampler
from opencensus.trace.tracer import Tracer


class CustomDimensionsFilter(logging.Filter):
    """Add custom-dimensions in each log by using filters."""

    def __init__(self, custom_dimensions=None):
        """Initialize CustomDimensionsFilter."""
        self.custom_dimensions = custom_dimensions or {}

    def filter(self, record):
        """Add the default custom_dimensions into the current log record."""
        dim = {**self.custom_dimensions, **getattr(record, "custom_dimensions", {})}
        record.custom_dimensions = dim
        return True

    def add_custom_dimension(self, key: str, value: str):
        """Add custom dimension into the filter."""
        self.custom_dimensions[key] = value


class AppLogger:
    """Logger wrapper that attach the handler to Application Insights."""

    HANDLER_NAME = "Azure Application Insights Handler"

    def __init__(self, config=None):
        """Create an instance of the Logger class.
        Args:
            config:([dict], optional):
                Contains the setting for logger {"log_level": "DEBUG","logging_enabled":"true"",
                                    "app_insights_key":"<app insights key>"}
        """
        config_integration.trace_integrations(["logging"])
        config_integration.trace_integrations(["requests"])
        self.config = {"log_level": logging.INFO, "logging_enabled": "true"}
        self.APPINSIGHTS_CONNECTION_STRING = "APPINSIGHTS_CONNECTION_STRING"
        self.custom_dimension_filters = []
        self.update_config(config)

    def _initialize_azure_log_handler(self, component_name, custom_dimensions):
        """Initialize azure log handler."""
        # Adding logging to trace_integrations
        # This will help in adding trace and span ids to logs
        # https://github.com/census-instrumentation/opencensus-python/tree/master/contrib/opencensus-ext-logging

        logging.basicConfig(
            format="%(asctime)s name=%(name)s level=%(levelname)s "
            "traceId=%(traceId)s spanId=%(spanId)s %(message)s"
        )
        app_insights_cs = self._get_app_insights_key()
        log_handler = AzureLogHandler(
            connection_string=app_insights_cs, enable_local_storage=False
        )
        log_handler.add_telemetry_processor(self._get_callback(component_name))
        log_handler.name = self.HANDLER_NAME
        custom_dimension_filter = CustomDimensionsFilter(custom_dimensions)
        self.custom_dimension_filters.append(custom_dimension_filter)
        log_handler.addFilter(custom_dimension_filter)
        return log_handler

    def _initialize_logger(self, log_handler, component_name):
        """Initialize Logger."""
        logger = logging.getLogger(component_name)
        logger.setLevel(self.log_level)
        if self.config.get("logging_enabled") == "true":
            if not any(x for x in logger.handlers if x.name == self.HANDLER_NAME):
                logger.addHandler(log_handler)
        return logger

    def add_correlation_id(self, correlation_id: str):
        """Add correlation id to the logger."""
        for filter in self.custom_dimension_filters:
            filter.add_custom_dimension("correlation_id", correlation_id)

    def get_logger(self, component_name="AppLogger", custom_dimensions={}):
        """Get Logger Object.
        Args:
            component_name (str, optional): Name of logger. Defaults to "AppLogger".
            custom_dimensions (dict, optional): {"key":"value"} to capture with every log.
                Defaults to {}.
        Returns:
            Logger: A logger.
        """
        self.update_config(self.config)
        handler = self._initialize_azure_log_handler(component_name, custom_dimensions)
        return self._initialize_logger(handler, component_name)

    def get_tracer(self, component_name="AppLogger", parent_tracer=None):
        """Get Tracer Object.
        Args:
            component_name (str, optional): Name of logger. Defaults to "AppLogger".
            parent_tracer([opencensus.trace.tracer], optional):
                Contains parent tracer required for setting coorelation.
        Returns:
            opencensus.trace.tracer: A Tracer.
        """
        self.update_config(self.config)
        sampler = AlwaysOnSampler()
        exporter = self.get_log_exporter(component_name)
        if self.config.get("logging_enabled") != "true":
            sampler = AlwaysOffSampler()
        if parent_tracer is None:
            tracer = Tracer(exporter=exporter, sampler=sampler)
        else:
            tracer = Tracer(
                span_context=parent_tracer.span_context,
                exporter=exporter,
                sampler=sampler,
            )
        return tracer

    def _get_app_insights_key(self):
        """Get Application Insights Key."""
        try:
            if self.app_insights_key is None:
                self.app_insights_key = getenv(self.APPINSIGHTS_CONNECTION_STRING, None)
            if self.logging_enabled != "false":
                if self.app_insights_key is not None:
                    instrumentation_key = self.app_insights_key[
                        self.app_insights_key.index("=")
                        + 1 : self.app_insights_key.index(";")  # noqa E203
                    ]
                    utils.validate_instrumentation_key(instrumentation_key)
                    return self.app_insights_key
                else:
                    raise Exception("ApplicationInsights Key is not set")
            return self.app_insights_key
        except Exception as exp:
            raise Exception(f"Exception is getting app insights key-> {exp}")

    def _get_callback(self, component_name):
        """Adding cloud role name. This is required to give the name of component in application map.
        https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-map?tabs=net#understanding-cloud-role-name-within-the-context-of-the-application-map
        Args:
            component_name ([str]): [The name of the component or applicaiton]
        """

        def _callback_add_role_name(envelope):
            """Add role name for logger."""
            envelope.tags["ai.cloud.role"] = component_name
            envelope.tags["ai.cloud.roleInstance"] = component_name

        return _callback_add_role_name

    def update_config(self, config=None):
        """Update logger configuration."""
        if config is not None:
            self.config.update(config)
        self.app_insights_key = self.config.get("app_insights_key")
        self.log_level = self.config.get("log_level")
        self.logging_enabled = self.config.get("logging_enabled")

    def get_log_exporter(self, component_name="AppLogger"):
        """[Get log exporter]

        Returns:
            [AzureExporter]: [Azure Log Exporter]
        """
        app_insights_cs = self._get_app_insights_key()
        log_exporter = AzureExporter(
            connection_string=app_insights_cs, enable_local_storage=False
        )
        log_exporter.add_telemetry_processor(self._get_callback(component_name))
        return log_exporter


def get_disabled_logger():
    """Get a disabled AppLogger.
    Returns:
        AppLogger: A disabled AppLogger
    """
    return AppLogger(
        config={
            "logging_enabled": "false",
            "app_insights_key": "InstrumentationKey=" + str(uuid.uuid1()),
        }
    )
