import unittest
from azure.ai.formrecognizer import AnalyzeResult, AnalyzedDocument, DocumentField

from src.ocr.model import OrderLabelFieldInfo
from src.validators.ocr_validator import OcrValidationResult
from src.common.status import ErrorCode
from src.frameprocessor.labelprocessor.default_label_processor import LabelProcessor


class TestLabelProcessor(unittest.TestCase):
    def test_extract_fields(self):
        ocr_document = AnalyzedDocument(
            fields={
                "customer_name": DocumentField(
                    value_type="string", value="John", confidence=0.896
                ),
                "item_name": DocumentField(
                    value_type="string",
                    value="Gr Icd Latte",
                    content="Gr Icd Latte",
                    confidence=0.874,
                ),
                "order_type": DocumentField(
                    value_type="string", value="CAFE", confidence=0.86
                ),
            }
        )
        ocr_result = AnalyzeResult(documents=[ocr_document])
        label_processor = LabelProcessor(0.5, None)
        extracted_fields = label_processor.extract_fields(ocr_result)
        self.assertIsInstance(extracted_fields["customer_name"], OrderLabelFieldInfo)
        self.assertEqual(extracted_fields["customer_name"].field_value, "John")
        self.assertEqual(extracted_fields["item_name"].field_value, "Gr Icd Latte")
        self.assertEqual(extracted_fields["order_type"].field_value, "CAFE")

    def test_validate_empty_document(self):
        extracted_fields = {}
        label_processor = LabelProcessor(0.5, None)
        validation_result = label_processor.validate_fields(extracted_fields)
        self.assertIsInstance(validation_result, OcrValidationResult)
        self.assertEqual(validation_result.is_valid, False)
        self.assertEqual(validation_result.error_code, ErrorCode.FIELD_MISSING)

    def test_validate_empty_fields(self):
        extracted_fields = {
            "customer_name": OrderLabelFieldInfo("customer_name", None, 0.43),
            "item_name": OrderLabelFieldInfo("item_name", "Gr Icd Latte", 0.874),
            "order_type": OrderLabelFieldInfo("order_type", "CAFE", 0.86),
        }
        label_processor = LabelProcessor(0.5, None)
        validation_result = label_processor.validate_fields(extracted_fields)
        self.assertIsInstance(validation_result, OcrValidationResult)
        self.assertEqual(validation_result.is_valid, False)
        self.assertEqual(validation_result.error_code, ErrorCode.FIELD_MISSING)

    def test_validate_fields_confidence_greater_than_threshold(self):
        extracted_fields = {
            "customer_name": OrderLabelFieldInfo("customer_name", "John", 0.896),
            "item_name": OrderLabelFieldInfo("item_name", "Gr Icd Latte", 0.874),
            "order_type": OrderLabelFieldInfo("order_type", "CAFE", 0.86),
        }
        label_processor = LabelProcessor(0.5, None)
        validation_result = label_processor.validate_fields(extracted_fields)
        self.assertIsInstance(validation_result, OcrValidationResult)
        self.assertEqual(validation_result.is_valid, True)
        self.assertEqual(validation_result.error_code, None)

    def test_validate_fields_with_low_confidence(self):
        extracted_fields = {
            "customer_name": OrderLabelFieldInfo("customer_name", "John", 0.43),
            "item_name": OrderLabelFieldInfo("item_name", "Gr Icd Latte", 0.874),
            "order_type": OrderLabelFieldInfo("order_type", "CAFE", 0.86),
        }
        label_processor = LabelProcessor(0.5, None)
        validation_result = label_processor.validate_fields(extracted_fields)
        self.assertIsInstance(validation_result, OcrValidationResult)
        self.assertEqual(validation_result.is_valid, False)
        self.assertEqual(validation_result.error_code, ErrorCode.LOW_FIELD_CONFIDENCE)

    def test_transform_fields(self):
        extracted_fields = {
            "customer_name": OrderLabelFieldInfo("customer_name", "*John*", 0.896),
            "item_name": OrderLabelFieldInfo("item_name", " Gr Icd Latte", 0.874),
            "order_type": OrderLabelFieldInfo("order_type", ">CAFE<", 0.86),
        }
        label_processor = LabelProcessor(0.5, None)
        transformed_fields = label_processor.transform_fields(extracted_fields)
        self.assertEqual(transformed_fields["customer_name"], "JOHN")
        self.assertEqual(transformed_fields["item_name"], "GR ICD LATTE")
        self.assertEqual(transformed_fields["order_type"], "CAFE")
