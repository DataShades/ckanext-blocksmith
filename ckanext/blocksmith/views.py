import json

from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk

import ckanext.blocksmith.model as model

blocksmith_blueprint = Blueprint("blocksmith", __name__)


class EditorView(MethodView):
    def get(self):
        return tk.render("blocksmith/create.html")


class ReadView(MethodView):
    def get(self, page_name: str):
        page = model.PageModel.get(page_name)

        if not page or (not page.published and not tk.current_user.sysadmin):
            tk.abort(404, "Page not found")

        template = (
            "blocksmith/read.html"
            if not page.fullscreen
            else "blocksmith/read_fullscreen.html"
        )

        return tk.render(template, extra_vars={"page": page})


class EditView(MethodView):
    def get(self, page_name: str):
        page = model.PageModel.get(page_name)

        if not page or not tk.current_user.sysadmin:
            tk.abort(404, "Page not found")

        page_dict = page.dictize({})
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
