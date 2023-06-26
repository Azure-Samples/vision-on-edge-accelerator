from src.frameprocessor.labelprocessor.default_label_processor import LabelProcessor


class LabelSpecificImplementation(LabelProcessor):

    CUSTOMER_NAME = "customer_name"

    def hash_identity(self, transformed_fields: dict[str, str]) -> str:
        """
        using customer_name to dedup

        @param
            transformed_fields (dict[str, str]): Dictionary of field names and their transformed values
        @return
            str: Hashed identity of the label
        """

        return transformed_fields[self.CUSTOMER_NAME]
