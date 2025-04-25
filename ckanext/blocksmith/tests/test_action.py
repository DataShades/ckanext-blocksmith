import pytest

from ckan.tests.helpers import call_action


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestCreatePage:
    def test_create_page(self, blocksmith_page):
        assert blocksmith_page["name"]
        assert blocksmith_page["title"]
        assert blocksmith_page["html"]
        assert blocksmith_page["editor_data"]
        assert blocksmith_page["published"]
        assert blocksmith_page["order_index"]
        assert blocksmith_page["fullscreen"]


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestGetPage:
    def test_create_page(self, blocksmith_page):
        page = call_action("blocksmith_get_page", name=blocksmith_page["name"])

        assert page["name"] == blocksmith_page["name"]
        assert page["title"] == blocksmith_page["title"]
        assert page["html"] == blocksmith_page["html"]
        assert page["editor_data"] == blocksmith_page["editor_data"]
        assert page["published"] == blocksmith_page["published"]
        assert page["order_index"] == blocksmith_page["order_index"]
        assert page["fullscreen"] == blocksmith_page["fullscreen"]
