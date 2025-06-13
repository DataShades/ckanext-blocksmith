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


def blocksmith_menu_exists(menu_id: str, context: types.Context) -> Any:
    """Ensures that the menu with a given id exists"""

    if not model.MenuModel.get_by_id(menu_id):
        raise tk.Invalid(f"The menu {menu_id} doesn't exist.")

    return menu_id


def blocksmith_parent_menu_item_exists(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Ensures that the menu item with a given id exists in the same menu"""

    menu_id = data.get(("menu_id",))
    parent_menu_item_id = data.get(("parent_id",))

    if not menu_id or not parent_menu_item_id:
        return

    current_menu = model.MenuModel.get_by_id(menu_id)
    parent_menu_item = model.MenuItemModel.get_by_id(parent_menu_item_id)

    if not parent_menu_item:
        raise tk.Invalid(f"The menu item {parent_menu_item_id} doesn't exist.")

    if not current_menu:
        return

    if parent_menu_item.menu_id != current_menu.id:
        raise tk.Invalid(
            f"The menu item {parent_menu_item_id} doesn't exist in the same menu."
        )


def blocksmith_name_is_unique(name: str, context: types.Context) -> Any:
    """Ensures that the name with a given name doesn't exist"""

    if model.MenuModel.get_by_name(name):
        raise tk.Invalid(f"The name {name} already exists.")

    return name


def blocksmith_snippet_name_is_unique(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Ensures that the snippet with a given name doesn't exist"""

    result = model.SnippetModel.get_by_name(data[key])

    if not result:
        return

    current_snippet = model.SnippetModel.get_by_id(data.get(("id",), ""))

    if current_snippet and current_snippet.name == data[key]:
        return

    raise tk.Invalid(f"The snippet {data[key]} already exists.")


def blocksmith_snippet_exists(snippet_id: str, context: types.Context) -> Any:
    """Ensures that the snippet with a given id exists"""

    result = model.SnippetModel.get_by_id(snippet_id)

    if not result:
        raise tk.Invalid(f"The snippet {snippet_id} doesn't exist.")

    return snippet_id
