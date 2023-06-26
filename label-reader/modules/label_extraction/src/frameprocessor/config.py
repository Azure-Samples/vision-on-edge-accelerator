"""This module is used to provide the configurations for label extraction process."""


from typing import List


class LabelExtractionConfig:
    """
    Class for label extraction process configurations.
    """

    def __init__(
        self,
        frame_size_ocr: List,
        status_internal_url: str,
        order_info_internal_url: str,
        device_id: str,
        store_id: str,
    ) -> None:
        """
        Initialize the configuration.

        @param
            frame_size_ocr (List): frame size for OCR as [height, width]
            status_internal_url (str): internal url for status WebAppApi
            order_info_internal_url (str): internal url for order info WebAppApi
            device_id (str): device id
            store_id (str): store id
        """
        self.frame_size_ocr = frame_size_ocr
        self.status_internal_url = status_internal_url
        self.order_info_internal_url = order_info_internal_url
        self.device_id = device_id
        self.store_id = store_id


class StorageConfig:

    """Contains all the configurations specific to Storage Helper"""

    def __init__(self, l_blob_storage_conn_string: str, l_container_name: str) -> None:
        """Initialize the instance of the StorageConfig class
        @param l_blob_storage_conn_string: (str) connection string for blob storage
        @param l_container_name: (str) container name for blob storage
        """

        self.blob_storage_conn_string = l_blob_storage_conn_string
        self.container_name = l_container_name


class SamplerConfig:

    """Contains all the configurations specific to Storage Helper"""

    def __init__(self, max_num_images_per_hour: int) -> None:
        """Initialize the instance of the StorageConfig class
        @param max_images_per_window per hour: (int) max images that will be captured during a window span

        """
        self.max_num_images_per_hour = max_num_images_per_hour


class DuplicateOrderCacheConfig:
    """
    Class for duplicate order cache configurations.
    """

    def __init__(self, max_len: int, max_age_in_seconds: int) -> None:
        """
        Initialize the configuration.

        @param
            max_len (int): max length of cache
            max_age_in_seconds (int): max age in seconds
        """
        self.max_len = max_len
        self.max_age_in_seconds = max_age_in_seconds
