from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk

blocksmith_blueprint = Blueprint("blocksmith", __name__, url_prefix="/blocksmith")


class EditorView(MethodView):
    def get(self):
        return tk.render("blocksmith/editor.html")


blocksmith_blueprint.add_url_rule("/editor", view_func=EditorView.as_view("editor"))
