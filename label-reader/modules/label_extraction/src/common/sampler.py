import time
from logging import Logger
from src.frameprocessor.config import SamplerConfig

""" Implements a simple sampling mechanism that will allow a certain number of
images to be uploaded to Azure Blob Storage within a time window
Once the time window is crossed, the sampling threshold is reset
There are no considerations for thread safety implemented, since the capped number is not
sacrosanct, and it is acceptable to have a few more images than the configured limit

"""


class BasicSampler:
    def __init__(self, logger: Logger, sampler_config: SamplerConfig):
        self.config = sampler_config

        self.image_count = 0
        self.logger = logger

        # this is the gap between 2 consecutive uploads
        self.upload_frequency = 3600 / self.config.max_num_images_per_hour
        self.rollover_time = time.time()
        self.logger.info(
            f"Sampler configuration initialized.. Frames will be uploaded every {self.upload_frequency} seconds"
        )

    def is_threshold_reached(self) -> bool:
        """
        checks the sampling rule and determines whether the current image should be uploaded to storage or not
        @return: (bool) True if the sampling threshold has been reached, False otherwise
        """
        if time.time() >= self.rollover_time:
            # reset the time window afresh
            self.rollover_time = time.time() + self.upload_frequency
            self.logger.debug("Sampling threshold has been reset now ..")
            return False
        else:
            return True
