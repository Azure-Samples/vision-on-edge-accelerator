"""This module provides all models for azure ocr post processing."""


class OrderLabelFieldInfo:
    """
    This class is used to provide model for an order label field
    """

    def __init__(
        self,
        field_name: str,
        field_value: str,
        field_confidence: float,
    ) -> None:
        """
        Initialize the class

        @param
            field_name (str): Name of the field in the order label
            field_value (str): Value of the field in the order label
            field_confidence (float): Analysis confidence for the field in the order label
        """
        self.field_name = field_name
        self.field_value = field_value
        self.field_confidence = field_confidence


class OrderLabelInfo:
    """
    This class provides order label info model
    """

    def __init__(
        self,
        customer_name: OrderLabelFieldInfo,
        item_name: OrderLabelFieldInfo,
        order_type: OrderLabelFieldInfo,
    ) -> None:
        """
        Initialize the class

        @param
            customer_name (OrderLabelFieldInfo): customer name
            item_name (OrderLabelFieldInfo]): item name
            order_type (OrderLabelFieldInfo): order type
        """
        self.customer_name = customer_name
        self.item_name = item_name
        self.order_type = order_type
