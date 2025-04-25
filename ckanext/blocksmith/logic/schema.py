from __future__ import annotations

from typing import Any, Dict

from ckan.logic.schema import validator_args

Schema = Dict[str, Any]


@validator_args
def blocksmith_page_save(
    not_empty,
    name_validator,
    convert_to_json_if_string,
    boolean_validator,
    if_empty_same_as,
    unicode_safe,
    int_validator,
    ignore,
    default,
) -> Schema:

    return {
        "name": [not_empty, unicode_safe, name_validator],
        "title": [if_empty_same_as("name"), unicode_safe],
        "html": [not_empty, unicode_safe],
        "css": [not_empty, unicode_safe],
        "editor_data": [not_empty, convert_to_json_if_string],
        "published": [default(False), boolean_validator],
        "order_index": [default(0), int_validator],
        "__extras": [ignore],
    }
