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


@validator_args
def blocksmith_create_menu(
    not_empty,
    unicode_safe,
    name_validator,
    ignore_empty,
    ignore,
    blocksmith_name_is_unique,
) -> Schema:
    return {
        "name": [not_empty, unicode_safe, name_validator, blocksmith_name_is_unique],
        "__extras": [ignore_empty, ignore],
    }


@validator_args
def blocksmith_create_menu_item(
    not_empty,
    unicode_safe,
    default,
    int_validator,
    ignore_empty,
    ignore,
    blocksmith_parent_menu_item_exists,
    blocksmith_menu_exists,
) -> Schema:
    return {
        "title": [not_empty, unicode_safe],
        "url": [not_empty, unicode_safe],
        "order": [default(0), int_validator],
        "parent_id": [ignore_empty, unicode_safe, blocksmith_parent_menu_item_exists],
        "classes": [ignore_empty, unicode_safe],
        "menu_id": [not_empty, unicode_safe, blocksmith_menu_exists],
        "__extras": [ignore],
    }


@validator_args
def blocksmith_update_menu(
    not_empty,
    unicode_safe,
    name_validator,
    ignore_empty,
    ignore,
    blocksmith_menu_exists,
    blocksmith_name_is_unique,
) -> Schema:
    return {
        "id": [not_empty, unicode_safe, blocksmith_menu_exists],
        "name": [ignore_empty, unicode_safe, name_validator, blocksmith_name_is_unique],
        "__extras": [ignore_empty, ignore],
    }


@validator_args
def blocksmith_delete_menu(not_empty, blocksmith_menu_exists) -> Schema:
    return {"id": [not_empty, blocksmith_menu_exists]}
