class StorageUploadRequest:
    """
    Storage Upload Request class.
    """

    def __init__(
        self, image: bytes, correlation_id: str, device_id: str, store_id: str
    ) -> None:
        """
        Initialize the StorageUploadRequest class.

        @param
            image (bytes): image from cup label scan
            correlation_id (str): correlation id of the image frame
            device_id (str): id of the device that captured the image
            store_id (str): store id where the device is running

        @return
            None
        """
        self.image = image
        self.correlation_id = correlation_id
        self.device_id = device_id
        self.store_id = store_id
