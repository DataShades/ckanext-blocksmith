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
