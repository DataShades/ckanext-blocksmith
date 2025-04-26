from __future__ import annotations

from typing import Any, Dict

from ckan.logic.schema import validator_args

Schema = Dict[str, Any]


@validator_args
def blocksmith_create_page(
    not_empty,
    boolean_validator,
    blocksmith_url_is_unique,
    unicode_safe,
    ignore,
    default,
) -> Schema:

    return {
        "url": [not_empty, unicode_safe, blocksmith_url_is_unique],
        "title": [not_empty, unicode_safe],
        "html": [not_empty, unicode_safe],
        "data": [not_empty, unicode_safe],
        "published": [default(False), boolean_validator],
        "fullscreen": [default(False), boolean_validator],
        "__extras": [ignore],
    }


@validator_args
def blocksmith_get_page(not_empty, unicode_safe, blocksmith_page_exists) -> Schema:
    return {"id": [not_empty, unicode_safe, blocksmith_page_exists]}


@validator_args
def blocksmith_update_page(
    not_empty,
    unicode_safe,
    blocksmith_url_is_unique,
    blocksmith_page_exists,
    boolean_validator,
    ignore,
    ignore_empty,
) -> Schema:
    return {
        "id": [not_empty, unicode_safe, blocksmith_page_exists],
        "title": [ignore_empty, unicode_safe],
        "url": [ignore_empty, unicode_safe, blocksmith_url_is_unique],
        "html": [ignore_empty, unicode_safe],
        "data": [ignore_empty, unicode_safe],
        "published": [ignore_empty, boolean_validator],
        "fullscreen": [ignore_empty, boolean_validator],
        "__extras": [ignore],
    }


@validator_args
def blocksmith_delete_page(not_empty, blocksmith_page_exists) -> Schema:
    return {"id": [not_empty, blocksmith_page_exists]}
