from typing import TypedDict


class Page(TypedDict):
    id: str
    url: str
    title: str
    html: str | None
    data: str | None
    created_at: str
    modified_at: str
    fullscreen: bool
    published: bool
