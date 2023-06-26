"""This modules creates an expiring dict for order number cache"""
from expiringdict import ExpiringDict
from logging import Logger


class ExpiringCache:
    """
    ExpiringCache class.
    This class is used to create an expiring cache.
    """

    def __init__(self, max_len: int, max_age_in_seconds: int, logger: Logger) -> None:
        """
        Initialize the ExpiringCache class.
        @param
            max_len (int): max length of the dict
            max_age_in_seconds (int): max age in seconds
            logger (logging.Logger): logger
        """
        self.max_age_in_seconds = max_age_in_seconds
        self.max_len = max_len
        self.logger = logger
        self.cache = None

    def initialize(self) -> None:
        """
        Initialize the ExpiringCache class.
        @param
            None
        @return
            None
        """
        self.logger.info("Initializing ExpiringCache for order number")
        try:
            self.cache = ExpiringDict(
                max_len=self.max_len, max_age_seconds=self.max_age_in_seconds
            )
        except Exception as e:
            self.logger.exception(e)
            self.logger.error(f"Error, in creating expiring cache: {e}")
            raise e

    def validate_cache(self) -> bool:
        """
        Validate the cache.
        @param
            None
        @return
            None
        """
        if self.cache is None:
            self.logger.error("ExpiringCache for order number not initialized")
            return False
        return True

    def contains(self, key: str) -> bool:
        """
        Check if the key is present in the dict.
        @param
            key (str): key
        @return
            bool: True if key is present else False
        """
        if key is not None and self.validate_cache():
            return self.cache.__contains__(key)
        return False

    def add_item(self, key: str, value: object) -> None:
        """
        Set the value of the key.
        @param
            key (str): key
            value (object): value
        @return
            None
        """
        if key is not None and value is not None and self.validate_cache():
            self.logger.debug(f"Adding key: {key} and value: {value} to cache")
            self.cache.__setitem__(key, value)

    def get_value(self, key: str) -> object:
        """
        Get the value of the key.
        @param
            key (str): key
        @return
            object: value of the key
        """
        if key is not None and self.validate_cache():
            if self.cache.__contains__(key):
                return self.cache.__getitem__(key)
        return None

    def remove(self, key: str) -> None:
        """
        Delete the key.
        @param
            key (str): key
        @return
            None
        """
        if key is not None and self.validate_cache():
            self.logger.debug(f"Removing key: {key} from cache")
            if self.cache.__contains__(key):
                self.cache.__delitem__(key)

    def clear(self) -> None:
        """
        Clear the dict.
        @param
            None
        @return
            None
        """
        if self.validate_cache():
            self.logger.debug("Clearing the cache")
            self.cache.clear()

    def get_len(self) -> int:
        """
        Get the length of the dict.
        @param
            None
        @return
            int: length of the dict
        """
        len = 0
        if self.validate_cache():
            len = self.cache.__len__()
            self.logger.debug(f"Length of cache {len}")
        return len
