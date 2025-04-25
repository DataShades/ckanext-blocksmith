from typing import cast

import ckan.plugins.toolkit as tk
from ckan import types
from ckan.logic import validate

import ckanext.blocksmith.logic.schema as schema
import ckanext.blocksmith.model as model


@validate(schema.blocksmith_save_page)
def blocksmith_save_page(
    context: types.Context, data_dict: types.DataDict
) -> types.ActionResult.AnyDict:
    tk.check_access("blocksmith_save_page", context, data_dict)

    page = model.PageModel.create(data_dict)

    return page.dictize(context)


@tk.side_effect_free
@validate(schema.blocksmith_get_page)
def blocksmith_get_page(
    context: types.Context, data_dict: types.DataDict
) -> types.ActionResult.AnyDict:
    tk.check_access("blocksmith_get_page", context, data_dict)

    page = cast(model.PageModel, model.PageModel.get(data_dict["name"]))

    return page.dictize(context)
