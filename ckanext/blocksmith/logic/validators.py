from __future__ import annotations

from typing import Any

import ckan.types as types
import ckan.plugins.toolkit as tk

import ckanext.blocksmith.model as model


def blocksmith_page_exists(name_or_id: str, context: types.Context) -> Any:
    """Ensures that the page with a given id exists"""

    result = model.PageModel.get(name_or_id)

    if not result:
        raise tk.Invalid(f"The page {name_or_id} doesn't exist.")

    return name_or_id
