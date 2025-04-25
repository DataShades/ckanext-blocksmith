import json

from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk
from ckan.types import Context

import ckanext.blocksmith.model as model

blocksmith_blueprint = Blueprint("blocksmith", __name__)


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


class EditorView(MethodView):
    def get(self):
        return tk.render("blocksmith/create.html")


class ReadView(MethodView):
    def get(self, page_name: str):
        page = model.PageModel.get(page_name)

        try:
            tk.check_access("blocksmith_get_page", make_context(), {"name": page_name})
        except (tk.NotAuthorized, tk.ObjectNotFound):
            return tk.abort(404, "Page not found")

        template = (
            "blocksmith/read.html"
            if not page.fullscreen  # type: ignore
            else "blocksmith/read_fullscreen.html"
        )

        return tk.render(template, extra_vars={"page": page})


class EditView(MethodView):
    def get(self, page_name: str):
        page = model.PageModel.get(page_name)

        try:
            tk.check_access("blocksmith_edit_page", make_context(), {"name": page_name})
        except (tk.NotAuthorized, tk.ObjectNotFound):
            return tk.abort(404, "Page not found")

        page_dict = page.dictize({})  # type: ignore
        page_dict["editor_data"] = json.dumps(page_dict["editor_data"])

        return tk.render("blocksmith/edit.html", extra_vars={"page": page_dict})


blocksmith_blueprint.add_url_rule(
    "/blocksmith/create", view_func=EditorView.as_view("create")
)
blocksmith_blueprint.add_url_rule(
    "/blocksmith/edit/<page_name>", view_func=EditView.as_view("edit")
)
blocksmith_blueprint.add_url_rule(
    "/page/<page_name>", view_func=ReadView.as_view("read")
)
