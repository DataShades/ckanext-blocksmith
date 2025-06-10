from abc import abstractmethod
from datetime import datetime

from bs4 import BeautifulSoup

import ckan.model as model
import ckan.plugins.toolkit as tk


class BaseOption:
    pass

class ListOption(BaseOption):
    pass

class BaseTag:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    # def options(self) -> type[BaseOption]:
    #     return [
    #         ListOption("zelupa", options=[1, 0])
    #     ]

    # text
    # integer
    # textarea
    # list (bool? true/false)

    @abstractmethod
    def render_html(self) -> str:
        """Renders the tag as HTML.

        Returns:
            The HTML representation of the tag.
        """

    @abstractmethod
    def check_access(self) -> bool:
        """Checks if the tag is accessible to the current user.

        Returns:
            True if the tag is accessible, False otherwise.
        """
        return True


class DateYearTag(BaseTag):
    def render_html(self) -> str:
        return f"<span>{datetime.now().year}</span>"


class PackageTileTag(BaseTag):
    def render_html(self) -> str:
        package = model.Package.get(self.kwargs["package_id"])

        if not package:
            return "<span>Dataset not found</span>"

        return tk.render(
            "snippets/package_list.html", extra_vars={"packages": [package.as_dict()]}
        )

    def check_access(self) -> bool:
        return tk.check_access(
            "package_show",
            {"user": tk.current_user.name},
            {"id": self.kwargs["package_id"]},
        )


class UnknownTag(BaseTag):
    def render_html(self) -> str:
        return f"<strong>Unknown tag: {self.kwargs['id']}</strong>"


class RemoveTag(BaseTag):
    def render_html(self) -> str:
        return ""


def process_tags(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    remove_tag = RemoveTag()

    for tag in soup.find_all("tag"):
        tag_id = tag.get("id", "")  # type: ignore

        if not tag_id or not isinstance(tag_id, str):
            continue

        tag_class = get_tag_class(tag_id)

        tag_instance = tag_class(**tag.attrs)  # type: ignore

        processed_html = (
            tag_instance.render_html()
            if tag_instance.check_access()
            else remove_tag.render_html()
        )

        tag.replace_with(BeautifulSoup(processed_html, "html.parser"))

    return str(soup)


def get_tag_class(tag_id: str) -> type[BaseTag]:
    if tag_id == "date_year":
        return DateYearTag
    elif tag_id == "dataset_tile":
        return PackageTileTag
    else:
        return UnknownTag
