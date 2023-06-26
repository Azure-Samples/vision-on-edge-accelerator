"""This module is used to get all configuration and create config objects."""

import os

from src.util.config import StorageConfig, WebappApiConfig


class ConfigHandler:
    """
    Get all configuration and create config objects.
    """

    def __init__(self, config_source: str = "environment") -> None:
        """
        Initialize ConfigHandler.

        @param:
            config_source (str): source of all configurations
        """
        self.config_source = config_source

    def get_webapp_api_config(self) -> WebappApiConfig:
        """
        Get WebappApiConfig instance

        @return:
            WebappApiConfig (object): WebappApiConfig class
        """
        return WebappApiConfig()

    def get_storage_config(self) -> StorageConfig:
        """
        Get StorageConfig instance

        @return:
            StorageConfig (object): StorageConfig class
        """
        return StorageConfig(
            self.get_config("BLOB_STORAGE_CONN_STRING"),
            self.get_config("AZURE_BLOB_STORAGE_CONTAINER_NAME"),
        )

    def get_config(self, config_name: str) -> str:
        """
        Get value of a specific configuration parameter.

        @return:
        value (str): Parameter value
        """
        if self.config_source == "environment":
            return self._read_env_variable(config_name)
        else:
            raise ValueError(f"Unknown config source: {self.config_source}")

    def _read_env_variable(self, config_name) -> str:
        """
        Read environment variable.

        @param:
            config_name (str): Name of the configuration parameter
        @return:
            value (str): Parameter value
        """
        value = os.environ.get(config_name)
        if value is None:
            raise ValueError(f"Config environment variable {config_name} is not set.")
        return value
