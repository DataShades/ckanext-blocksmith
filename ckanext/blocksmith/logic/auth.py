from ckan.types import AuthResult, Context, DataDict


def blocksmith_save_page(context: Context, data_dict: DataDict) -> AuthResult:
    # sysadmin only
    return {"success": False}
