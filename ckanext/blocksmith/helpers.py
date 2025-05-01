import ckan.plugins.toolkit as tk


def blocksmith_get_default_content() -> str:
    return tk.render("blocksmith/page/default_content.html")
