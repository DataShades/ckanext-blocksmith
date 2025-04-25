import ckan.plugins.toolkit as tk
from ckan.types import AuthResult, Context, DataDict

import ckanext.blocksmith.model as model


def blocksmith_create_page(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


@tk.auth_allow_anonymous_access
def blocksmith_get_page(context: Context, data_dict: DataDict) -> AuthResult:
    page_name = tk.get_or_bust(data_dict, "name")

    page = model.PageModel.get(page_name)

    if (not page) or (
        not page.published
        and tk.current_user.is_anonymous
        or not tk.current_user.sysadmin
    ):
        return {"success": False}

    return {"success": True}


def blocksmith_edit_page(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


def blocksmith_update_page(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}
