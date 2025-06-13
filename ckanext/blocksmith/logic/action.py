from typing import cast

import ckan.plugins.toolkit as tk
from ckan import types
from ckan.logic import validate

import ckanext.blocksmith.logic.schema as schema
import ckanext.blocksmith.model as model
import ckanext.blocksmith.types as blocksmith_types


@validate(schema.blocksmith_create_page)
def blocksmith_create_page(
    context: types.Context, data_dict: types.DataDict
) -> blocksmith_types.Page:
    tk.check_access("blocksmith_create_page", context, data_dict)

    page = model.PageModel.create(data_dict)

    return page.dictize(context)


@tk.side_effect_free
@validate(schema.blocksmith_get_page)
def blocksmith_get_page(
    context: types.Context, data_dict: types.DataDict
) -> blocksmith_types.Page:
    tk.check_access("blocksmith_get_page", context, data_dict)

    page = cast(model.PageModel, model.PageModel.get_by_id(data_dict["id"]))

    return page.dictize(context)


@validate(schema.blocksmith_update_page)
def blocksmith_update_page(
    context: types.Context, data_dict: types.DataDict
) -> blocksmith_types.Page:
    tk.check_access("blocksmith_update_page", context, data_dict)

    page = model.PageModel.get_by_id(data_dict["id"])

    if not page:
        raise tk.ObjectNotFound("Page not found")

    page.update(data_dict)

    return page.dictize(context)


@tk.side_effect_free
def blocksmith_list_pages(
    context: types.Context, data_dict: types.DataDict
) -> list[blocksmith_types.Page]:
    tk.check_access("blocksmith_list_pages", context, data_dict)

    return [page.dictize(context) for page in model.PageModel.get_all()]


@validate(schema.blocksmith_delete_page)
def blocksmith_delete_page(
    context: types.Context, data_dict: types.DataDict
) -> types.ActionResult.AnyDict:
    tk.check_access("blocksmith_delete_page", context, data_dict)

    page = cast(model.PageModel, model.PageModel.get_by_id(data_dict["id"]))

    page.delete()

    return {"success": True}


@validate(schema.blocksmith_create_menu)
def blocksmith_create_menu(
    context: types.Context, data_dict: types.DataDict
) -> blocksmith_types.Menu:
    tk.check_access("blocksmith_manage_menu", context, data_dict)

    menu = model.MenuModel.create(data_dict)

    return menu.dictize(context)


@validate(schema.blocksmith_create_menu_item)
def blocksmith_create_menu_item(
    context: types.Context, data_dict: types.DataDict
) -> blocksmith_types.MenuItem:
    tk.check_access("blocksmith_manage_menu", context, data_dict)

    menu_item = model.MenuItemModel.create(data_dict)

    return menu_item.dictize(context)


@tk.side_effect_free
def blocksmith_list_menus(
    context: types.Context, data_dict: types.DataDict
) -> list[blocksmith_types.Menu]:
    tk.check_access("blocksmith_manage_menu", context, data_dict)

    return [menu.dictize(context) for menu in model.MenuModel.get_all()]


@validate(schema.blocksmith_update_menu)
def blocksmith_update_menu(
    context: types.Context, data_dict: types.DataDict
) -> blocksmith_types.Menu:
    tk.check_access("blocksmith_manage_menu", context, data_dict)

    menu = model.MenuModel.get_by_id(data_dict["id"])

    if not menu:
        raise tk.ObjectNotFound("Menu not found")

    menu.update(data_dict)

    return menu.dictize(context)


@validate(schema.blocksmith_delete_menu)
def blocksmith_delete_menu(
    context: types.Context, data_dict: types.DataDict
) -> types.ActionResult.AnyDict:
    tk.check_access("blocksmith_manage_menu", context, data_dict)

    menu = cast(model.MenuModel, model.MenuModel.get_by_id(data_dict["id"]))

    menu.delete()

    return {"success": True}


@validate(schema.blocksmith_create_snippet)
def blocksmith_create_snippet(
    context: types.Context, data_dict: types.DataDict
) -> blocksmith_types.Snippet:
    tk.check_access("blocksmith_create_snippet", context, data_dict)

    snippet = model.SnippetModel.create(data_dict)

    return snippet.dictize(context)


@validate(schema.blocksmith_update_snippet)
def blocksmith_update_snippet(
    context: types.Context, data_dict: types.DataDict
) -> blocksmith_types.Snippet:
    tk.check_access("blocksmith_edit_snippet", context, data_dict)

    snippet = model.SnippetModel.get_by_id(data_dict["id"])

    if not snippet:
        raise tk.ObjectNotFound("Snippet not found")

    snippet.update(data_dict)

    return snippet.dictize(context)


@validate(schema.blocksmith_delete_snippet)
def blocksmith_delete_snippet(
    context: types.Context, data_dict: types.DataDict
) -> types.ActionResult.AnyDict:
    tk.check_access("blocksmith_delete_snippet", context, data_dict)

    snippet = cast(model.SnippetModel, model.SnippetModel.get_by_id(data_dict["id"]))

    snippet.delete()

    return {"success": True}


@tk.side_effect_free
@validate(schema.blocksmith_get_snippet)
def blocksmith_get_snippet(
    context: types.Context, data_dict: types.DataDict
) -> blocksmith_types.Snippet:
    tk.check_access("blocksmith_get_snippet", context, data_dict)

    snippet = cast(model.SnippetModel, model.SnippetModel.get_by_id(data_dict["id"]))

    return snippet.dictize(context)


@tk.side_effect_free
def blocksmith_list_snippets(
    context: types.Context, data_dict: types.DataDict
) -> list[blocksmith_types.Snippet]:
    tk.check_access("blocksmith_list_snippets", context, data_dict)

    return [snippet.dictize(context) for snippet in model.SnippetModel.get_all()]
