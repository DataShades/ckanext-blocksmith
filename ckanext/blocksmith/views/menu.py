from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk
from ckan.types import Context

import ckanext.blocksmith.model as model

bs_menu_blueprint = Blueprint("bs_menu", __name__, url_prefix="/blocksmith/menu")


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


class MenuListView(MethodView):
    def get(self):
        try:
            tk.check_access("blocksmith_manage_menu", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "You are not authorized to visit this page")

        menus = [menu.dictize({}) for menu in model.MenuModel.get_all()]

        return tk.render("blocksmith/menu/menu_list.html", extra_vars={"menus": menus})

    def post(self):
        return tk.render("blocksmith/menu/menu_list.html")


bs_menu_blueprint.add_url_rule("/list", view_func=MenuListView.as_view("list"))
