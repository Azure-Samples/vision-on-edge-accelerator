"""This module is used to provide frame provider process."""
import os
import signal
from src.pcm.queue import ProcessQueue
from src.frameprovider.camera_integration import CameraIntegration
from src.common.log_helper import get_logger


class FrameProviderProcess:
    """
    Process for frame provider.
    """

    def __init__(self) -> None:
        """
        Initialize the frame provider process.
        """
        pass

    def run(self, queue: ProcessQueue) -> None:
        """
        Run the frame provider process.

        @param
            queue (ProcessQueue): Object to communicate with frame processor
        """
        self.logger = get_logger(
            component_name=FrameProviderProcess.__name__,
        )
        self.logger.info("Starting frame provider process...")
        self._process(queue)
        self.logger.info("Started frame provider process...")

    def _process(self, queue: ProcessQueue) -> None:
        """
        Process for frame provider.

        @param
            queue (ProcessQueue): Object to communicate with frame processor
        """
        try:
            camera_integration = CameraIntegration(queue)
            camera_integration.start_camera()
        except Exception as e:
            self.logger.critical(
                "Failed to start camera integration process: {}".format(e)
            )
            self.logger.exception(e)
            self.logger.critical("Killing main process...")
            self.logger.critical(f"Killing main process... pid = {os.getppid()}")
            os.kill(os.getppid(), signal.SIGTERM)
