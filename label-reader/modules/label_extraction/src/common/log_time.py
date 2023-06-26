"""Creates a timer decorator function
"""

import functools
from time import time
from src.common.log_helper import get_logger

logger = get_logger("Timer")


def log_time(func):
    """Logs time taken by function
    @param
        func: function object
    @return
        This function returns the wrapper function which logs the time taken by function
    @usage
        For any function for which we need time to be logged we can annotate the function using @log_time
        eg
            @log_time
            def func1():
                print("func1")
    """

    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        """Wrapper function to log the time
        @param
            *args: Non keyword arguments
            **kwards: Keyword arguments
        @return
            Returns the result of execution of function 'func'
        """
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        time_taken = end_time - start_time
        extra_properties = _create_properties(func, time_taken)
        logger.debug(
            f"Time taken by function {func.__code__.co_filename}.{func.__name__} is {time_taken}",
            extra=extra_properties,
        )
        return result

    return _wrapper


def _create_properties(func, time_taken):
    """Function to create properties object for logging dimensions for log_time
    @param
        func: Function object for which @log_time is added
        time_taken: Time taken by execution of function
    @return
        Returns the properties object
    """
    properties = {
        "custom_dimensions": {
            "func_name": func.__name__,
            "time_taken": time_taken,
            "file_name": func.__code__.co_filename,
        }
    }
    return properties
