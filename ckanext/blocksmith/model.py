from typing import Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from typing_extensions import Self

import ckan.model as model
import ckan.plugins.toolkit as tk
from ckan.model.types import make_uuid


class PageModel(tk.BaseModel):
    __tablename__ = "blocksmith_page"

    id = sa.Column(sa.Text, primary_key=True, default=make_uuid)
    name = sa.Column(sa.String, unique=True, nullable=False)
    title = sa.Column(sa.Text, nullable=False)
    html = sa.Column(sa.Text)
    editor_data = sa.Column(JSONB)
    published = sa.Column(sa.Boolean, default=False)
    order_index = sa.Column(sa.Integer, default=0)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    modified_at = sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    fullscreen = sa.Column(sa.Boolean, default=False)

    @classmethod
    def create(cls, data_dict: dict[str, Any]) -> Self:
        page = cls(**data_dict)

        model.Session.add(page)
        model.Session.commit()

        return page

    def delete(self) -> None:
        model.Session().autoflush = False
        model.Session.delete(self)
        model.Session.commit()

    def dictize(self, context):
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "html": self.html,
            "editor_data": self.editor_data,
            "published": self.published,
            "order_index": self.order_index,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "fullscreen": self.fullscreen,
        }

    @classmethod
    def get(cls, id_or_name: str) -> Self | None:
        return (
            model.Session.query(cls)
            .filter(sa.or_(cls.id == id_or_name, cls.name == id_or_name))
            .first()
        )

    @classmethod
    def get_all(cls) -> list[Self]:
        return model.Session.query(cls).order_by(cls.order_index).all()

    def update(self, data_dict: dict[str, Any]) -> None:
        for key, value in data_dict.items():
            setattr(self, key, value)

        model.Session.commit()
