"""This module is used to provide frame processor process."""
import os
import signal
from src.frameprocessor.label_extraction import LabelExtractionProcess
from src.pcm.queue import ProcessQueue
from src.common.log_helper import get_logger


class FrameProcessorProcess:
    """
    Process for frame processor.
    """

    def __init__(self) -> None:
        """
        Initialize the frame processor process.
        """
        pass

    def run(self, queue: ProcessQueue) -> None:
        """
        Run the frame processor process.

        @param
            queue: ProcessQueue object to communicate with frame processor
        """
        self.logger = get_logger(
            component_name=FrameProcessorProcess.__name__,
        )
        self.logger.info("Starting frame processor process...")
        self._process(queue)

    def _process(self, queue: ProcessQueue) -> None:
        """
        Process for frame processor.

        @param
            queue: ProcessQueue object to communicate with frame processor
        """
        try:
            label_extraction = LabelExtractionProcess(queue)
            label_extraction.run()
        except Exception as e:
            self.logger.critical("Failed to start frame processor process {}".format(e))
            self.logger.exception(e)
            self.logger.critical(f"Killing main process... pid = {os.getppid()}")
            os.kill(os.getppid(), signal.SIGTERM)
