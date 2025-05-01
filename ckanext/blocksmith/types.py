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


class MenuItem(TypedDict):
    id: str
    title: str
    url: str
    order: int
    parent_id: str | None
    classes: str | None
    menu_id: str


class Menu(TypedDict):
    id: str
    name: str
    items: list[MenuItem]
    created_at: str
    modified_at: str
