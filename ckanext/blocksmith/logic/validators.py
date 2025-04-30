from __future__ import annotations

from typing import Any

import ckan.plugins.toolkit as tk
import ckan.types as types

import ckanext.blocksmith.model as model


def blocksmith_page_exists(page_id: str, context: types.Context) -> Any:
    """Ensures that the page with a given id exists"""

    result = model.PageModel.get_by_id(page_id)

    if not result:
        raise tk.Invalid(f"The page {page_id} doesn't exist.")

    return page_id


def blocksmith_url_is_unique(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Ensures that the page with a given url doesn't exist"""


    result = model.PageModel.get_by_url(data[key])

    if not result:
        return

    current_page = model.PageModel.get_by_id(data.get(("id",), ""))

    if current_page and current_page.url == data[key]:
        return

    raise tk.Invalid(f"The page {data[key]} already exists.")
