from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk
from ckan.types import Context

import ckanext.blocksmith.model as model
from ckanext.blocksmith.tags import process_tags


bs_page_blueprint = Blueprint("bs_page", __name__, url_prefix="/blocksmith/page")


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

        return tk.render("blocksmith/page/create.html")


class ReadView(MethodView):
    def get(self, page_id: str):
        page = model.PageModel.get_by_id(page_id)

        if not page:
            return tk.abort(404, "Page not found")

        page.html = process_tags(page.html)  # type: ignore

        try:
            tk.check_access("blocksmith_get_page", make_context(), {"id": page_id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        template = (
            "blocksmith/page/read.html"
            if not page.fullscreen  # type: ignore
            else "blocksmith/page/read_fullscreen.html"
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

        return tk.render(
            "blocksmith/page/edit.html", extra_vars={"page": page.dictize({})}
        )


class ListView(MethodView):
    def get(self):
        try:
            tk.check_access("blocksmith_list_pages", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        pages = [page.dictize({}) for page in model.PageModel.get_all()]

        return tk.render("blocksmith/page/list.html", extra_vars={"pages": pages})


bs_page_blueprint.add_url_rule("/create", view_func=EditorView.as_view("create"))
bs_page_blueprint.add_url_rule("/edit/<page_id>", view_func=EditView.as_view("edit"))
bs_page_blueprint.add_url_rule("/read/<page_id>", view_func=ReadView.as_view("read"))
bs_page_blueprint.add_url_rule("/list", view_func=ListView.as_view("list"))
