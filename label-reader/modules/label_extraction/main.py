"""This is the main module."""
from multiprocessing.context import DefaultContext
import multiprocessing
import signal
import sys
import time
from src.pcm.controller import ProcessController

from src.common.log_helper import get_logger


def main(multiprocessing_context: DefaultContext):
    logger = get_logger(
        component_name="MainProcess",
    )
    logger.info("Initiating all configurations...")
    logger.info("Calling process controller start...")
    process_controller = ProcessController(multiprocessing_context)
    try:
        process_controller.initialize()
        process_controller.start()
    except Exception as exp:
        logger.exception(exp)
        logger.error(f"Exception while starting process controller: {exp}")
        sys.exit(1)
    logger.info("Starting the main process...")
    while True:
        time.sleep(100000000)


def exit_gracefully(*args):
    logger = get_logger(
        component_name="MainProcess",
    )
    logger.warning("Received SIGINT/SIGTERM signal. Exiting gracefully...")
    sys.exit(1)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    multiprocessing_context = multiprocessing.get_context()
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    main(multiprocessing_context)
