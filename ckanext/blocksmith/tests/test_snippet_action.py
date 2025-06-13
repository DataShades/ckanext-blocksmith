import pytest

from ckan.tests.helpers import call_action


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestCreateSnippet:
    def test_create_snippet(self, snippet):
        assert snippet["id"]
        assert snippet["name"]
        assert snippet["title"]
        assert snippet["html"]
        assert snippet["created_at"]
        assert snippet["modified_at"]


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestGetSnippet:
    def test_create_snippet(self, snippet):
        snippet = call_action("blocksmith_get_snippet", id=snippet["id"])

        assert snippet["id"] == snippet["id"]
        assert snippet["name"] == snippet["name"]
        assert snippet["title"] == snippet["title"]
        assert snippet["html"] == snippet["html"]
        assert snippet["created_at"] == snippet["created_at"]
        assert snippet["modified_at"] == snippet["modified_at"]


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestUpdateSnippet:
    def test_update_snippet(self, snippet):
        updated_snippet = call_action(
            "blocksmith_update_snippet",
            id=snippet["id"],
            title="New Title",
            name="new_title",
            html="New HTML",
        )

        assert updated_snippet["name"] == "new_title"
        assert updated_snippet["title"] == "New Title"
        assert updated_snippet["html"] == "New HTML"
        assert updated_snippet["created_at"] == snippet["created_at"]
        assert updated_snippet["modified_at"] != snippet["modified_at"]


@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestListSnippets:
    def test_list_snippets(self, snippet):
        snippets = call_action("blocksmith_list_snippets")

        assert len(snippets) == 1
        assert snippets[0]["name"] == snippet["name"]
        assert snippets[0]["title"] == snippet["title"]
        assert snippets[0]["html"] == snippet["html"]
        assert snippets[0]["created_at"] == snippet["created_at"]
        assert snippets[0]["modified_at"] == snippet["modified_at"]

    def test_list_snippets2(self, snippet):
        snippets = call_action("blocksmith_list_snippets")

        assert len(snippets) == 1
        assert snippets[0]["name"] == snippet["name"]
        assert snippets[0]["title"] == snippet["title"]
        assert snippets[0]["html"] == snippet["html"]
        assert snippets[0]["created_at"] == snippet["created_at"]
        assert snippets[0]["modified_at"] == snippet["modified_at"]
