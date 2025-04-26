from flask import Response

import ckan.plugins.toolkit as tk
import ckan.types as types

from ckanext.blocksmith.model import PageModel
from ckanext.blocksmith.views import ReadView, make_context


def render_page_if_exists(response: types.Response) -> types.Response:
    """Check if the page exists at the given url.

    This allows us to show the page without registering the blueprint.
    We do it only if the original response is a 404, and it means,
    that there's no blueprint at the given url.
    """
    if response.status_code != 404:
        return response

    path = tk.request.path.lstrip("/")

    if page := PageModel.get_by_url(path):
        # delete to reinitialize webassets
        delattr(tk.g, "_webassets")

        try:
            tk.check_access("blocksmith_get_page", make_context(), {"id": page.id})
        except tk.NotAuthorized:
            return response

        return Response(ReadView().get(str(page.id)), status=200, mimetype="text/html")

    return response
