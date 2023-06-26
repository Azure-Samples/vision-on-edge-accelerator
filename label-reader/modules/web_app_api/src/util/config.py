"""Contains all the configuration settings used to tune
the behavior of the component. Presently, these configs
are hard set in code. These would be environment variable
driven in subsequent iterations

"""


class WebappApiConfig:

    """Contains all the configurations specific to Webapp API Services"""

    # The singleton instance of the current class
    __instance = None

    def __init__(
        self,
    ) -> None:
        """Initialize the singleton instance of the WebappApiConfig class"""
        self.compression_is_enabled = True

    def disable_compression(self):
        """_summary_: Disable compression for the Webapp API
        Note that this would take effect only for new
        web socket connections
        """

        self.compression_is_enabled = False

    def enable_compression(self):
        """summary_: Enable compression for the Webapp API
        Note that this would take effect only for new
        web socket connections
        """

        self.compression_is_enabled = True


class StorageConfig:

    """Contains all the configurations specific to Storage Helper"""

    # The singleton instance of the current class
    __instance = None

    def __init__(self, l_blob_storage_conn_string: str, l_container_name: str) -> None:
        """Initialize the singleton instance of the StorageConfig class"""
        self.blob_storage_conn_string = l_blob_storage_conn_string
        self.container_name = l_container_name
