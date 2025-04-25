import ckan.plugins.toolkit as tk
from ckan import types
from ckan.logic import validate

import ckanext.blocksmith.logic.schema as schema
import ckanext.blocksmith.model as blocksmith_model


@validate(schema.blocksmith_page_save)
def blocksmith_page_save(
    context: types.Context, data_dict: types.DataDict
) -> types.ActionResult.AnyDict:
    import ipdb

    ipdb.set_trace()

    tk.check_access("blocksmith_save_page", context, data_dict)

    blocksmith_model.PageModel.create(data_dict)

    return {"success": True, "message": "Page saved successfully"}
