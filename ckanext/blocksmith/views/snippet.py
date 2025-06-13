from flask import Blueprint
from flask.views import MethodView

import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
import ckan.plugins.toolkit as tk
from ckan.types import Context

import ckanext.blocksmith.model as model
import ckanext.blocksmith.utils as bs_utils

bs_snippet_blueprint = Blueprint(
    "bs_snippet", __name__, url_prefix="/blocksmith/snippet"
)


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


class EditorView(MethodView):
    def get(self):
        try:
            tk.check_access("blocksmith_create_snippet", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        return tk.render("blocksmith/snippet/create.html", extra_vars={"data": {}})

    def post(self):
        try:
            tk.check_access("blocksmith_create_snippet", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        try:
            data_dict = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, _("Integrity Error"))

        data_dict["extras"] = {}
        data_dict["extras"]["arguments"] = bs_utils.prepare_snippet_arguments(data_dict)

        try:
            tk.get_action("blocksmith_create_snippet")(make_context(), data_dict)
        except tk.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "blocksmith/snippet/create.html", extra_vars={"data": data_dict}
            )

        return tk.redirect_to("bs_snippet.list")


class ReadView(MethodView):
    def get(self, snippet_id: str):
        snippet = model.SnippetModel.get_by_id(snippet_id)

        if not snippet:
            return tk.abort(404, "Page not found")

        try:
            tk.check_access(
                "blocksmith_edit_snippet", make_context(), {"id": snippet_id}
            )
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        return tk.render(
            "blocksmith/snippet/read.html", extra_vars={"snippet": snippet}
        )

    def post(self, snippet_id: str):
        try:
            tk.check_access("blocksmith_edit_snippet", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        try:
            data_dict = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, _("Integrity Error"))

        extra_vars = {"data": data_dict, "name": data_dict.pop("name")}
        try:
            return tk.render(
                "blocksmith/snippet/snippets/snippet_preview.html",
                extra_vars=extra_vars,
            )
        except Exception as e:
            return str(e)


class EditView(MethodView):
    def get(self, snippet_id: str):
        snippet = model.SnippetModel.get_by_id(snippet_id)

        try:
            tk.check_access(
                "blocksmith_edit_snippet", make_context(), {"id": snippet_id}
            )
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not snippet:
            return tk.abort(404, "Page not found")

        return tk.render(
            "blocksmith/snippet/edit.html",
            extra_vars={"snippet_id": snippet_id, "data": snippet.dictize({})},
        )

    def post(self, snippet_id):
        try:
            tk.check_access("blocksmith_edit_snippet", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        try:
            data_dict = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, _("Integrity Error"))

        data_dict["extras"] = {}
        data_dict["extras"]["arguments"] = bs_utils.prepare_snippet_arguments(data_dict)
        data_dict["id"] = snippet_id

        try:
            tk.get_action("blocksmith_update_snippet")(make_context(), data_dict)
        except tk.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "blocksmith/snippet/edit.html",
                extra_vars={"snippet_id": snippet_id, "data": data_dict},
            )

        return tk.redirect_to("bs_snippet.read", snippet_id=snippet_id)


@bs_snippet_blueprint.route("/delete/<snippet_id>")
def delete(snippet_id):
    try:
        tk.check_access("blocksmith_delete_snippet", make_context(), {})
    except tk.NotAuthorized:
        return tk.abort(404, "Page not found")

    data_dict = {"id": snippet_id}

    tk.get_action("blocksmith_delete_snippet")(make_context(), data_dict)

    return tk.redirect_to("bs_snippet.list")


class ListView(MethodView):
    def get(self):
        try:
            tk.check_access("blocksmith_list_snippets", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        snippets = [snippet.dictize({}) for snippet in model.SnippetModel.get_all()]

        return tk.render(
            "blocksmith/snippet/list.html", extra_vars={"snippets": snippets}
        )


@bs_snippet_blueprint.route("/add-argument-snippet", methods=["POST"])
def add_argument() -> str:
    return tk.render(
        "/blocksmith/snippet/snippets/snippet_kwarg_fieldset.html",
        extra_vars={},
    )


bs_snippet_blueprint.add_url_rule("/create", view_func=EditorView.as_view("create"))
bs_snippet_blueprint.add_url_rule(
    "/edit/<snippet_id>", view_func=EditView.as_view("edit")
)
bs_snippet_blueprint.add_url_rule(
    "/read/<snippet_id>", view_func=ReadView.as_view("read")
)
bs_snippet_blueprint.add_url_rule("/list", view_func=ListView.as_view("list"))
