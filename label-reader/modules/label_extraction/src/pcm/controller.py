"""This module is used to provide process controller."""
import json
from multiprocessing.context import DefaultContext
from multiprocessing import Process
from src.common.config_handler import ConfigHandler
from src.common.socket_client import SocketClient
from src.pcm.processor_process import FrameProcessorProcess
from src.pcm.provider_process import FrameProviderProcess
from src.common.log_helper import get_logger
from src.pcm.queue import ProcessQueue


class AdminResponse:
    def __init__(self, command: str, status: str):
        """
        Initialize the admin response.

        @param:
            command (str): Command
            status (str): Status
        """
        self.command = command
        self.status = status
        self.type = "response"


class ProcessController:
    """
    Process controller for start stop restarting the processes.
    """

    def __init__(self, multiprocessing_context: DefaultContext) -> None:
        """
        Initialize the process controller.

        @param:
            multiprocessing_context (DefaultContext): Multiprocessing context
        """
        self.multiprocessing_context = multiprocessing_context
        self.queue = ProcessQueue()
        self.frame_provider_process = None
        self.frame_processor_process = None
        self.logger = get_logger(
            component_name=ProcessController.__name__,
        )
        config_handler = ConfigHandler()
        self.config = config_handler.get_process_conroller_config()
        self.ws = SocketClient(
            self.config.admin_internal_url,
            on_message=self.on_message,
        )

    def initialize(self) -> None:
        """
        Initialize the process controller.
        """
        self.logger.info("Initializing process controller...")
        self.ws.connect()
        self.ws.start_dispatcher()
        self.logger.info("Initialized process controller...")

    def on_message(self, message: str) -> None:
        """
        On message callback.

        @param:
            message (str): Message
        """
        self.logger.info(f"Admin Control Received message: {message}")
        message_dict = json.loads(message)
        message_type = message_dict["type"]
        message_command = message_dict["command"]
        response = AdminResponse(message_command, "success")
        if message_type == "request":
            try:
                if message_command == "start":
                    self.start()
                elif message_command == "stop":
                    self.stop()
                elif message_command == "restart":
                    self.restart()
                else:
                    self.logger.error(f"Unknown message: {message}")
                    response.status = "error"
            except Exception as e:
                self.logger.error(f"Error: {e}")
                self.logger.exception(e)
                response.status = "error"
            self.ws.send(json.dumps(response, default=lambda o: o.__dict__))

    def start(self) -> bool:
        """
        Start the processes.

        @return:
            success (bool): True if the processes are started successfully, False otherwise
        """
        self.logger.info("Starting all processes...")
        if (
            self.frame_provider_process is not None
            and self.frame_provider_process.is_alive()
        ):
            self.logger.info("frame_provider_process is already running...")
            return False
        if (
            self.frame_processor_process is not None
            and self.frame_processor_process.is_alive()
        ):
            self.logger.info("frame_processor_process is already running...")
            return False

        self.queue = ProcessQueue()
        self.frame_provider_process = self.multiprocessing_context.Process(
            target=FrameProviderProcess().run,
            args=((self.queue),),
            name="frame_provider_process",
        )
        self.frame_provider_process.daemon = True
        self.frame_provider_process.start()
        self.frame_processor_process = self.multiprocessing_context.Process(
            target=FrameProcessorProcess().run,
            args=((self.queue),),
            name="frame_processor_process",
        )
        self.frame_processor_process.daemon = True
        self.frame_processor_process.start()
        self.logger.info("Started all processes...")
        return True

    def stop(self) -> bool:
        """
        Stop the processes.

        @return:
            success (bool): True if the processes are stopped successfully, False otherwise
        """
        self.logger.info("Stopping all processes...")
        if (
            self.frame_provider_process is not None
            and self.frame_provider_process.is_alive()
        ):
            self._terminate_process(self.frame_provider_process)
            self.frame_provider_process = None
            self.logger.info("frame_provider_process is stopped...")
        if (
            self.frame_processor_process is not None
            and self.frame_processor_process.is_alive()
        ):
            self._terminate_process(self.frame_processor_process)
            self.frame_processor_process = None
            self.logger.info("frame_processor_process is stopped...")

        self.queue.work_queue.close()
        self.logger.info("Queue is cleared...")
        self.logger.info("Stopped all processes...")
        return True

    def restart(self) -> bool:
        """
        Restart the processes.

        @return:
            success (bool): True if the processes are restarted successfully, False otherwise
        """
        self.logger.info("Restarting all processes...")
        self.stop()
        result = self.start()
        self.logger.info("Restarted all processes...")
        return result

    def _terminate_process(self, process: Process, retry_count: int = 0) -> None:
        """
        Terminate the process with retry (internal).

        @param:
            process (Process): Process object
            retry_count (int): Retry count
        """
        self.logger.info(f"Terminating process {process.name}...")
        if retry_count < 3:
            try:
                process.terminate()
            except Exception as e:
                self.logger.exception(e)
                self.logger.error(e)
                self._terminate_process(process, retry_count + 1)
        else:
            self.logger.error(f"Could not terminate process {process.name}...")
            raise Exception(f"Could not terminate process {process.name}...")
