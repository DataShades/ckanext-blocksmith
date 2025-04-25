import pytest


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
