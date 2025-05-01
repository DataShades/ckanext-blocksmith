from typing import Callable

import pytest

import ckan.plugins.toolkit as tk

import ckanext.blocksmith.types as bs_types


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestCreateMenu:
    def test_create_menu(self, menu: bs_types.Menu):
        assert menu["id"]
        assert menu["name"]
        assert menu["items"] == []

    @pytest.mark.parametrize(
        "name, is_valid",
        [
            ("a", False),  # invalid, too short
            ("just a title", False),  # invalid, not a slug
            ("valid-name", True),  # valid
            ("valid_name_with_underscores", True),  # valid
            ("valid-name-with-numbers-123", True),  # valid
        ],
    )
    def test_create_menu_with_improper_name(
        self, menu_factory: Callable[..., bs_types.Menu], name: str, is_valid: bool
    ):
        if is_valid:
            menu_factory(name=name)
        else:
            with pytest.raises(tk.ValidationError):
                menu_factory(name=name)


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestCreateMenuItem:
    def test_create_menu_item(
        self,
        menu: bs_types.Menu,
        menu_item_factory: Callable[..., bs_types.MenuItem],
    ):
        menu_item = menu_item_factory(menu_id=menu["id"])

        assert menu_item["id"]
        assert menu_item["title"]
        assert menu_item["url"]
        assert menu_item["order"] == 0
        assert menu_item["parent_id"] is None
        assert menu_item["classes"] == "some-class some-other-class"
        assert menu_item["menu_id"] == menu["id"]

    def test_create_menu_item_with_non_existing_parent(
        self, menu_item_factory: Callable[..., bs_types.MenuItem]
    ):
        with pytest.raises(tk.ValidationError, match="The menu item 123 doesn't exist"):
            menu_item_factory(parent_id="123")

    def test_create_menu_item_with_parent_from_other_menu(
        self,
        menu: bs_types.Menu,
        menu_item_factory: Callable[..., bs_types.MenuItem],
    ):
        parent_menu_item = menu_item_factory(menu_id=menu["id"])

        with pytest.raises(tk.ValidationError, match="doesn't exist in the same menu"):
            menu_item_factory(parent_id=parent_menu_item["id"])

    def test_create_menu_item_with_parent_from_same_menu(
        self,
        menu: bs_types.Menu,
        menu_item_factory: Callable[..., bs_types.MenuItem],
    ):
        parent_menu_item = menu_item_factory(menu_id=menu["id"])
        child_menu_item = menu_item_factory(
            menu_id=menu["id"], parent_id=parent_menu_item["id"]
        )

        assert child_menu_item["id"]
        assert child_menu_item["title"]
        assert child_menu_item["url"]
        assert child_menu_item["order"] == 0
        assert child_menu_item["parent_id"] == parent_menu_item["id"]
        assert child_menu_item["menu_id"] == menu["id"]
