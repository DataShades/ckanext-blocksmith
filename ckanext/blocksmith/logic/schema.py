from __future__ import annotations

from typing import Any, Dict

from ckan.logic.schema import validator_args

Schema = Dict[str, Any]


@validator_args
def blocksmith_create_page(
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


@validator_args
def blocksmith_update_page(
    not_empty,
    unicode_safe,
    name_validator,
    blocksmith_page_exists,
    boolean_validator,
    int_validator,
    ignore,
    convert_to_json_if_string,
    ignore_empty,
) -> Schema:
    return {
        "id": [not_empty, unicode_safe, blocksmith_page_exists],
        "title": [ignore_empty, unicode_safe],
        "name": [ignore_empty, unicode_safe, name_validator],
        "html": [ignore_empty, unicode_safe],
        "editor_data": [ignore_empty, convert_to_json_if_string],
        "published": [ignore_empty, boolean_validator],
        "order_index": [ignore_empty, int_validator],
        "fullscreen": [ignore_empty, boolean_validator],
        "__extras": [ignore],
    }
