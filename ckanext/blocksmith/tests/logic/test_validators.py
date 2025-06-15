from typing import Any, Callable

import pytest

import ckan.plugins.toolkit as tk

import ckanext.blocksmith.types as bs_types
from ckanext.blocksmith.logic import validators


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestBlocksmithPageExists:
    def test_page_exists(self, page):
        assert validators.blocksmith_page_exists(page["id"], {}) == page["id"]

    def test_page_does_not_exist(self):
        with pytest.raises(tk.Invalid, match="The page non-existent doesn't exist."):
            validators.blocksmith_page_exists("non-existent", {})


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestBlocksmithUrlIsUnique:
    def test_url_is_unique(self, page):
        errors = {}
        validators.blocksmith_url_is_unique(
            ("url",), {("url",): "new-unique-url"}, errors, {}
        )
        assert not errors

    def test_url_already_exists(self, page):
        errors = {}
        with pytest.raises(tk.Invalid, match=f"The page {page['url']} already exists."):
            validators.blocksmith_url_is_unique(
                ("url",), {("url",): page["url"]}, errors, {}
            )

    def test_url_same_as_current_page(self, page):
        errors = {}
        validators.blocksmith_url_is_unique(
            ("url",), {("url",): page["url"], ("id",): page["id"]}, errors, {}
        )
        assert not errors


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestBlocksmithMenuExists:
    def test_menu_exists(self, menu: bs_types.Menu):
        result = validators.blocksmith_menu_exists(menu["id"], {})
        assert result == menu["id"]

    def test_menu_does_not_exist(self):
        with pytest.raises(tk.Invalid, match="The menu non-existent doesn't exist."):
            validators.blocksmith_menu_exists("non-existent", {})


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestBlocksmithParentMenuItemExists:
    def test_parent_menu_item_exists(
        self, menu: bs_types.Menu, menu_item_factory: Callable[..., bs_types.MenuItem]
    ):
        errors = {}

        parent_menu_item = menu_item_factory(menu_id=menu["id"])
        child_menu_item = menu_item_factory(
            menu_id=menu["id"], parent_id=parent_menu_item["id"]
        )

        validators.blocksmith_parent_menu_item_exists(
            ("parent_id",),
            {
                ("menu_id",): menu["id"],
                ("parent_id",): child_menu_item["id"],
            },
            errors,
            {},
        )

        assert not errors

    def test_parent_menu_item_does_not_exist(self, menu: bs_types.Menu):
        errors = {}

        with pytest.raises(
            tk.Invalid, match="The menu item non-existent doesn't exist."
        ):
            validators.blocksmith_parent_menu_item_exists(
                ("parent_id",),
                {("menu_id",): menu["id"], ("parent_id",): "non-existent"},
                errors,
                {},
            )


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestBlocksmithNameIsUnique:
    def test_name_is_unique(self):
        assert (
            validators.blocksmith_name_is_unique("new-unique-name", {})
            == "new-unique-name"
        )

    def test_name_already_exists(self, menu):
        with pytest.raises(
            tk.Invalid, match=f"The name {menu['name']} already exists."
        ):
            validators.blocksmith_name_is_unique(menu["name"], {})


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestBlocksmithSnippetNameIsUnique:
    def test_snippet_name_is_unique(self, snippet: dict[str, Any]):
        errors = {}

        validators.blocksmith_snippet_name_is_unique(
            ("name",), {("name",): "new-unique-name"}, errors, {}
        )

        assert not errors

    def test_snippet_name_already_exists(self, snippet: dict[str, Any]):
        errors = {}

        with pytest.raises(
            tk.Invalid, match=f"The snippet {snippet['name']} already exists."
        ):
            validators.blocksmith_snippet_name_is_unique(
                ("name",), {("name",): snippet["name"]}, errors, {}
            )

    def test_snippet_name_same_as_current_snippet(self, snippet: dict[str, Any]):
        errors = {}
        validators.blocksmith_snippet_name_is_unique(
            ("name",), {("name",): snippet["name"], ("id",): snippet["id"]}, errors, {}
        )
        assert not errors


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestBlocksmithSnippetExists:
    def test_snippet_exists(self, snippet: dict[str, Any]):
        assert validators.blocksmith_snippet_exists(snippet["id"], {}) == snippet["id"]

    def test_snippet_does_not_exist(self):
        with pytest.raises(tk.Invalid, match="The snippet non-existent doesn't exist."):
            validators.blocksmith_snippet_exists("non-existent", {})
