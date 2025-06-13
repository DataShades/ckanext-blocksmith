from flask import render_template_string
from markupsafe import Markup

import ckan.plugins.toolkit as tk

import ckanext.blocksmith.model as model


def blocksmith_get_default_content() -> str:
    return tk.render("blocksmith/page/default_content.html")


def bs_render_snippet(name, **kwargs) -> str | None:
    """Render a snippet.

    Args:
        name: The name of the snippet
        **kwargs: The keyword arguments to pass to the snippet

    Returns:
        The rendered snippet
    """
    snippet = model.SnippetModel.get_by_name(name)

    if not snippet:
        return None

    return Markup(render_template_string(snippet.html.strip(), **kwargs))
