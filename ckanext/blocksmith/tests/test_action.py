import pytest


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestCreatePage:
    def test_create_page(self, blocksmith_page):
        assert blocksmith_page is not None
