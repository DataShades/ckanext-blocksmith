import pytest

from ckan.tests.helpers import call_action


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestCreatePage:
    def test_create_page(self, page):
        assert page["id"]
        assert page["url"]
        assert page["title"]
        assert page["html"]
        assert page["data"]
        assert page["published"]
        assert page["fullscreen"] is False
        assert page["created_at"]
        assert page["modified_at"]


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestGetPage:
    def test_create_page(self, page):
        page = call_action("blocksmith_get_page", id=page["id"])

        assert page["id"] == page["id"]
        assert page["url"] == page["url"]
        assert page["title"] == page["title"]
        assert page["html"] == page["html"]
        assert page["data"] == page["data"]
        assert page["published"] == page["published"]
        assert page["fullscreen"] == page["fullscreen"]
        assert page["created_at"] == page["created_at"]
        assert page["modified_at"] == page["modified_at"]


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestUpdatePage:
    def test_update_page(self, page):
        updated_page = call_action(
            "blocksmith_update_page",
            id=page["id"],
            title="New Title",
            url="/new-url",
            html="New HTML",
            data="New Data",
            published=True,
            fullscreen=True,
        )

        assert updated_page["url"] == "/new-url"
        assert updated_page["title"] == "New Title"
        assert updated_page["html"] == "New HTML"
        assert updated_page["data"] == "New Data"
        assert updated_page["published"]
        assert updated_page["fullscreen"]
        assert updated_page["created_at"] == page["created_at"]
        assert updated_page["modified_at"] != page["modified_at"]


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestListPages:
    def test_list_pages(self, page):
        pages = call_action("blocksmith_list_pages")

        assert len(pages) == 1
        assert pages[0]["url"] == page["url"]
        assert pages[0]["title"] == page["title"]
        assert pages[0]["html"] == page["html"]
        assert pages[0]["data"] == page["data"]
        assert pages[0]["published"] == page["published"]
        assert pages[0]["fullscreen"] == page["fullscreen"]
        assert pages[0]["created_at"] == page["created_at"]
        assert pages[0]["modified_at"] == page["modified_at"]
