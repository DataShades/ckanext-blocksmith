from typing import Any

import sqlalchemy as sa
from typing_extensions import Self

import ckan.model as model
import ckan.plugins.toolkit as tk
import ckan.types as types
from ckan.model.types import make_uuid

import ckanext.blocksmith.types as blocksmith_types


class PageModel(tk.BaseModel):
    __tablename__ = "blocksmith_page"

    id = sa.Column(sa.Text, primary_key=True, default=make_uuid)
    url = sa.Column(sa.String, unique=True, nullable=False)
    title = sa.Column(sa.Text, nullable=False)
    html = sa.Column(sa.Text)
    data = sa.Column(sa.Text)
    published = sa.Column(sa.Boolean, default=False)
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

    def dictize(self, context: types.Context) -> blocksmith_types.Page:
        return blocksmith_types.Page(
            id=str(self.id),
            url=str(self.url),
            title=str(self.title),
            html=str(self.html) if self.html else None,
            data=str(self.data) if self.data else None,
            published=bool(self.published),
            created_at=self.created_at.isoformat(),
            modified_at=self.modified_at.isoformat(),
            fullscreen=bool(self.fullscreen),
        )

    @classmethod
    def get_by_id(cls, page_id: str) -> Self | None:
        return model.Session.query(cls).filter(cls.id == page_id).first()

    @classmethod
    def get_by_url(cls, page_url: str) -> Self | None:
        return model.Session.query(cls).filter(cls.url == page_url).first()

    @classmethod
    def get_all(cls) -> list[Self]:
        return model.Session.query(cls).order_by(cls.modified_at.desc()).all()

    def update(self, data_dict: dict[str, Any]) -> None:
        for key, value in data_dict.items():
            setattr(self, key, value)

        model.Session.commit()
