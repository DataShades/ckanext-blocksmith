from flask import render_template_string
from markupsafe import Markup

import ckan.plugins.toolkit as tk

import ckanext.blocksmith.utils as bs_utils


def blocksmith_get_default_content() -> str:
    return tk.render("blocksmith/page/default_content.html")


def bs_render_snippet(name, **kwargs):
    snippet = bs_utils.load_snippet(name)
    
    if not snippet:
        return None

    return Markup(render_template_string(snippet.html.strip(), **kwargs))
