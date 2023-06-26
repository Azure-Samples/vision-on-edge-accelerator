import unittest
from src.frameprocessor.labelprocessor.label_processing import LabelProcessing
from unittest.mock import MagicMock
from src.validators.ocr_validator import OcrValidationResult


class TestLabelProcessing(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.afr_runner_mock = MagicMock(name="AFR Runner")
        cls.label_processor_mock = MagicMock(name="Label Processor")
        cls.logger_mock = MagicMock(name="Logger")
        cls.processing_request = MagicMock(name="Request")
        cls.label_processing = LabelProcessing(
            cls.afr_runner_mock, cls.label_processor_mock, cls.logger_mock
        )

    def _failed_validation(self):
        return OcrValidationResult(is_valid=False, error_code=None)

    def test_exit_the_run_and_raise_exception_if_afr_result_is_none(self):
        # setup
        self.afr_runner_mock.run.return_value = None

        # run
        self.assertRaises(Exception, self.label_processing.run, self.processing_request)

        # assert
        self.afr_runner_mock.run.assert_called_once()
        self.label_processor_mock.extract_fields.assert_not_called()

    def test_for_invalid_results(self):
        # setup
        failed_validation = self._failed_validation()
        self.label_processor_mock.validate_fields.return_value = failed_validation

        # run
        response = self.label_processing.run(self.processing_request)

        # assert
        self.label_processor_mock.extract_fields.assert_called_once()
        self.label_processor_mock.validate_fields.assert_called_once()
        self.label_processor_mock.transform_fields.assert_not_called()

        self.assertEqual(response.validation_result, failed_validation)
        self.assertIsNone(response.content_for_ui)
        self.assertIsNone(response.content_for_narration)
        self.assertIsNone(response.transformed_result)
        self.assertIsNone(response.hash_identity)

    def test_for_successful_flow(self):
        # run
        response = self.label_processing.run(self.processing_request)

        # assert
        self.label_processor_mock.extract_fields.assert_called_once()
        self.label_processor_mock.validate_fields.assert_called_once()
        self.label_processor_mock.transform_fields.assert_called_once()

        self.assertIsNotNone(response.content_for_ui)
        self.assertIsNotNone(response.content_for_narration)
        self.assertIsNotNone(response.transformed_result)
        self.assertIsNotNone(response.hash_identity)
