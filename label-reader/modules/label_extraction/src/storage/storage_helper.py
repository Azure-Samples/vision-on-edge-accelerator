import datetime
from logging import Logger
from typing import Union

import azure.core

from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient
from src.common.sampler import BasicSampler
from src.frameprocessor.config import StorageConfig
from src.storage.storage_request import StorageUploadRequest
from src.common.log_time import log_time


class StorageServiceHelper(object):
    """A Helper class that provides methods to upload an image to Azure Blob Storage when an
    OCR call on the image frame results in an error. This image would be used by back end Teams (e.g. Data scientists)
    to help them understand the cause for the OCR error.
    """

    def __init__(
        self,
        logger: Logger,
        storage_config: StorageConfig,
        basic_sampler: BasicSampler,
    ) -> None:
        """initializes the configuration settings required to access Blob
        Storage, and acquires a reference to the Logger utility
        @param logger: Logger utility
        @param storage_config: StorageConfig object containing the storage configuration settings
        @param basic_sampler: Basic Samplerobject containing the sampling logic before upload of image to blob storage

        @return: None
        """
        self.logger = logger
        self.config = storage_config
        self.sampler = basic_sampler
        self.blob_service_client = None
        self._initialize_storage_client()

    def _initialize_storage_client(self) -> None:
        # Instantiate a new BlobServiceClient using a connection string
        # set a retry policy of 3 times
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                self.config.blob_storage_conn_string, retry_total=3
            )
        except Exception as e:
            self.logger.error(f"Error connecting to Azure Blob Storage {e}, {type(e)}")
            self.logger.exception(e)
            return None

        with self.blob_service_client:
            container_client = self.blob_service_client.get_container_client(
                self.config.container_name
            )

            # Instantiate a new ContainerClient
            try:
                # Create new Container in the service
                container_client.create_container()
                self.logger.info("created a blob storage container for first use...")
            except azure.core.exceptions.ResourceExistsError:
                self.logger.info(
                    f"blob storage container {self.config.container_name} already exists ..."
                )
            except Exception as ex:
                self.logger.error(
                    f"error creating blob storage container {self.config.container_name},\
                        {ex}, {type(ex)}"
                )
                self.logger.exception(ex)
                return None

    def verify_upload_frame(
        self, storage_request: StorageUploadRequest
    ) -> Union[str, None]:
        """verifies the payload before Uploading the image frame to Azure Blob storage
        @param storage_request: StorageRequest object containing the request properties

        @return: (Union[str,None]) Blob name of the uploaded image frame
        """

        """Upload only the max numbers of frames allowed to Azure Blob Storage
        verify if the threshold has been hit for the current time window
        """
        if self.sampler.is_threshold_reached():
            return None

        if (
            storage_request.correlation_id is None
            or len(storage_request.correlation_id) == 0
            or storage_request.device_id is None
            or len(storage_request.device_id) == 0
            or storage_request.store_id is None
            or len(storage_request.store_id) == 0
        ):
            self.logger.error(
                "invalid or empty correlation id, device id, or store id; cannot upload image frame to blob storage"
            )
            return None

        # upload the image to Azure Blob storage
        return self._upload_frame(storage_request, storage_request.image)

    @log_time
    def _upload_frame(
        self, storage_request: StorageUploadRequest, frame: bytes
    ) -> Union[str, None]:
        """internal method that uploads the image frame to Azure Blob Storage
        # TODO - Blob Service Client cannot presently be reused across calls - to explore if there is a workaround
        to prevent instantiating it for every call
        Args:
            storage_request: (StorageUploadRequest) object containing the request details
            frame (bytes): image frame to upload

        Returns:
            Union[str,None]: The blob name of the uploaded image frame

        """

        blob_name = (
            storage_request.store_id
            + "/"
            + storage_request.device_id
            + "/"
            + "ocrerrors"
            + "/"
            + datetime.datetime.now().strftime("%Y-%m-%d")
            + "/"
            + storage_request.correlation_id
            + ".jpg"
        )
        blob_client = BlobClient.from_connection_string(
            conn_str=self.config.blob_storage_conn_string,
            container_name=self.config.container_name,
            blob_name=blob_name,
        )

        try:
            # Upload the image frame to the blob storage
            blob_client.upload_blob(frame, blob_type="BlockBlob")

            self.logger.info(
                f"uploaded image frame to blob storage, {blob_client.blob_name}"
            )

            # return the URL of the uploaded image to the caller
            return blob_client.blob_name
        except Exception as ex:
            self.logger.error(
                f"Error uploading image frame to blob storage : , {ex}, {type(ex)}"
            )
            self.logger.exception(ex)
            return None
