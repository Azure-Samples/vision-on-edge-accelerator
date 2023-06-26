import sys
from src.common.app_logger import AppLogger
from os import getenv
import logging

"""Entry point to get a logger that is used
across the module

"""


# the component name to use in the logger
component_name = "webapp-api"

APP_LOGGER = AppLogger()
app_insights_key = getenv("APPINSIGHTS_CONNECTION_STRING", None)
device_id = getenv("IOTEDGE_DEVICEID", "")
module_id = getenv("IOTEDGE_MODULEID", component_name)
store_id = getenv("STORE_ID", "")
log_level_from_env = getenv("LOG_LEVEL", "INFO")

logger_levels = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]  %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def get_logger(component_name=component_name):
    """Returns the logger that can be used

    Returns:
        Logger: Logger
    """
    try:
        log_level = logger_levels[log_level_from_env.rstrip()]

        if app_insights_key is None:
            # logger = get_disabled_logger().get_logger(component_name)
            logger = logging.getLogger(name=component_name)
        else:
            app_key = app_insights_key.rstrip()
            if app_key == "":
                # logger = get_disabled_logger().get_logger(component_name)
                logger = logging.getLogger(name=component_name)
            else:
                logger = APP_LOGGER.get_logger(
                    component_name=component_name,
                    custom_dimensions={
                        "deviceid": device_id,
                        "moduleid": module_id,
                        "store_id": store_id,
                    },
                )

        logger.setLevel(log_level)
        return logger
    except Exception as ex:
        print(ex)
        raise Exception(f"ERROR - in initiate app logger - {ex}") from ex
