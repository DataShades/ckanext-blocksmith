from __future__ import annotations

from typing import Any, Dict

from ckan.logic.schema import validator_args

Schema = Dict[str, Any]


@validator_args
def blocksmith_save_page(
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
        "editor_data": [not_empty, convert_to_json_if_string],
        "published": [default(False), boolean_validator],
        "order_index": [default(0), int_validator],
        "fullscreen": [default(False), boolean_validator],
        "__extras": [ignore],
    }


@validator_args
def blocksmith_get_page(not_empty, unicode_safe, blocksmith_page_exists) -> Schema:
    return {"name": [not_empty, unicode_safe, blocksmith_page_exists]}
