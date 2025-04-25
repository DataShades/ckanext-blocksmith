import ckan.plugins.toolkit as tk
from ckan.types import AuthResult, Context, DataDict

import ckanext.blocksmith.model as model


def blocksmith_save_page(context: Context, data_dict: DataDict) -> AuthResult:
    # sysadmin only
    return {"success": False}


@tk.auth_allow_anonymous_access
def blocksmith_get_page(context: Context, data_dict: DataDict) -> AuthResult:
    page_name = tk.get_or_bust(data_dict, "name")

    page = model.PageModel.get(page_name)

    if not page or not tk.current_user.sysadmin:
        return {"success": False}

    return {"success": True}
