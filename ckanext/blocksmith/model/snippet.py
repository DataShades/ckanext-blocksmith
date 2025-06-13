
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from typing_extensions import Self

import ckan.model as model
import ckan.plugins.toolkit as tk
import ckan.types as types
from ckan.model.types import make_uuid

import ckanext.blocksmith.types as blocksmith_types
from ckanext.blocksmith.model.base import BaseModelMixin


class SnippetModel(tk.BaseModel, BaseModelMixin):
    __tablename__ = "blocksmith_snippet"

    id = sa.Column(sa.Text, primary_key=True, default=make_uuid)
    title = sa.Column(sa.Text, nullable=False)
    name = sa.Column(sa.String, unique=True, nullable=False)
    html = sa.Column(sa.Text)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    modified_at = sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    extras = sa.Column(MutableDict.as_mutable(JSONB))

    def dictize(self, context: types.Context) -> blocksmith_types.Snippet:
        return blocksmith_types.Snippet(
            id=str(self.id),
            title=str(self.title),
            name=str(self.name),
            html=str(self.html) if self.html else None,
            created_at=self.created_at.isoformat(),
            modified_at=self.modified_at.isoformat(),
            extras=self.extras,  # type: ignore
        )

    @classmethod
    def get_by_id(cls, snippet_id: str) -> Self | None:
        return model.Session.query(cls).filter(cls.id == snippet_id).first()

    @classmethod
    def get_by_name(cls, snippet_name: str) -> Self | None:
        return model.Session.query(cls).filter(cls.name == snippet_name).first()

    @classmethod
    def get_all(cls) -> list[Self]:
        return model.Session.query(cls).order_by(cls.modified_at.desc()).all()
