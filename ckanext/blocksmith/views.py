from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk
from ckan.types import Context

import ckanext.blocksmith.model as model

blocksmith_blueprint = Blueprint("blocksmith", __name__, url_prefix="/blocksmith")


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


class EditorView(MethodView):
    def get(self):
        try:
            tk.check_access("blocksmith_create_page", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        return tk.render("blocksmith/create.html")


class ReadView(MethodView):
    def get(self, page_id: str):
        page = model.PageModel.get_by_id(page_id)

        if not page:
            return tk.abort(404, "Page not found")

        try:
            tk.check_access("blocksmith_get_page", make_context(), {"id": page_id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        template = (
            "blocksmith/read.html"
            if not page.fullscreen  # type: ignore
            else "blocksmith/read_fullscreen.html"
        )

        return tk.render(template, extra_vars={"page": page})


class EditView(MethodView):
    def get(self, page_id: str):
        page = model.PageModel.get_by_id(page_id)

        try:
            tk.check_access("blocksmith_edit_page", make_context(), {"id": page_id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not page:
            return tk.abort(404, "Page not found")

        return tk.render("blocksmith/edit.html", extra_vars={"page": page.dictize({})})


class ListView(MethodView):
    def get(self):
        try:
            tk.check_access("blocksmith_list_pages", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        pages = [page.dictize({}) for page in model.PageModel.get_all()]

        return tk.render("blocksmith/list.html", extra_vars={"pages": pages})


blocksmith_blueprint.add_url_rule("/create", view_func=EditorView.as_view("create"))
blocksmith_blueprint.add_url_rule("/edit/<page_id>", view_func=EditView.as_view("edit"))
blocksmith_blueprint.add_url_rule("/read/<page_id>", view_func=ReadView.as_view("read"))
blocksmith_blueprint.add_url_rule("/list", view_func=ListView.as_view("list"))
