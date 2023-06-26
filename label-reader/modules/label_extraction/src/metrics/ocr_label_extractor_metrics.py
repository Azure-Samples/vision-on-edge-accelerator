"""This module is used get properties for OCR Label Extractor metrics which can be used in logging."""


from typing import Dict, Union


def get_ocr_label_extrcator_metrics(
    order_type: str = None,
    order_number: str = None,
    candidate_lines: int = None,
    line_index_after_qty: int = None,
    item_name_cn: str = None,
    pickup_phrase: str = None,
) -> Dict[str, Union[str, int, None]]:
    """ "
    This function takes certain input params
    and returns properties object which can be used in logging.

    @param
        order_type(str):  Order type
        order_number(str): Order Number
        candidate_lines(int): Total candidates
        line_index_after_qty(int): Line index after qty line
        item_name_cn(str): item name cn as extracted from OCR
        pickup_phrase(str): pickup phrase
        correlation_id(str): correlation id
    @return
        properties(Dict[str, Union[str, int, None]]): properties object which can be used in logging.
    """
    properties = {
        "custom_dimensions": {
            "order_number": order_number,
            "order_type": order_type,
            "candidate_lines": candidate_lines,
            "line_index_after_qty": line_index_after_qty,
            "item_name_cn": item_name_cn,
            "pickup_phrase": pickup_phrase,
        }
    }
    return properties
