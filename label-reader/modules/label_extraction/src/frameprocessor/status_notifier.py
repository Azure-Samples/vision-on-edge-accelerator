"""This module is used to provide the status notifier."""
import json
from typing import Any, Union
from src.frameprocessor.labelprocessor.model import LabelProcessingResponse
from src.common.status import ErrorCode, Status, StatusCode
from src.edgeinferencing.result import TextDetectionResult
from src.common.socket_client import SocketClient


class StatusNotifier:
    """
    Status notifier class
    """

    def __init__(self, ws: SocketClient) -> None:
        """
        Initialize StatusNotifier.

        @param:
            ws (SocketClient): socket client
        """
        self.ws = ws

    def notify(
        self, result: Union[TextDetectionResult, Any], correlation_id: str
    ) -> bool:
        """
        Notify status to the server if it's eligible to be sent.

        @param:
            result (Union[TextDetectionResult, Any]): result to be sent
        @return:
            bool: True if the status is elibible to send and is sent successfully, False otherwise
        """
        if type(result) is TextDetectionResult:
            if not result.validation_result.is_valid:
                if result.validation_result.error_code == ErrorCode.LOW_BB:
                    return self._send_status(
                        Status(
                            error_sub_type=ErrorCode.LOW_BB,
                            error_code=StatusCode.LABEL_EXTRACTION,
                            correlation_id=correlation_id,
                            is_error=True,
                        ),
                    )
        elif type(result) is LabelProcessingResponse:
            if not result.validation_result.is_valid:
                return self._send_status(
                    Status(
                        error_sub_type=result.validation_result.error_code,
                        error_code=StatusCode.LABEL_EXTRACTION,
                        correlation_id=correlation_id,
                        is_error=True,
                    ),
                )
        return False

    def notify_system(self, error_code: ErrorCode, correlation_id: str) -> bool:
        return self._send_status(
            Status(
                error_sub_type=error_code,
                error_code=StatusCode.SYSTEM,
                correlation_id=correlation_id,
                is_error=True,
            ),
        )

    def _send_status(self, status: Status) -> bool:
        """
        Send status to the server.

        @param:
            status (Status): status to be sent
        @return:
            bool: True if the status is sent successfully, False otherwise
        """
        return self.ws.send(json.dumps(status, default=lambda o: o.__dict__))
