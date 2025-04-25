from typing import TypedDict


class Page(TypedDict):
    id: str
    name: str
    title: str
    html: str | None
    data: str | None
    published: bool
    created_at: str
    modified_at: str
    fullscreen: bool
