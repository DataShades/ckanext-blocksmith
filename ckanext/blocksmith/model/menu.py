import sqlalchemy as sa
from sqlalchemy.orm import relationship
from typing_extensions import Self

import ckan.model as model
import ckan.plugins.toolkit as tk
import ckan.types as types
from ckan.model.types import make_uuid

import ckanext.blocksmith.types as blocksmith_types
from ckanext.blocksmith.model.base import BaseModelMixin


class MenuModel(tk.BaseModel, BaseModelMixin):
    __tablename__ = "blocksmith_menu"

    id = sa.Column(sa.Text, primary_key=True, default=make_uuid)
    name = sa.Column(sa.Text, nullable=False, unique=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    modified_at = sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())

    items = relationship(
        "MenuItemModel",
        back_populates="menu",
        cascade="all, delete-orphan",
    )

    @classmethod
    def get_by_id(cls, menu_id: str) -> Self | None:
        return model.Session.query(cls).filter(cls.id == menu_id).first()

    @classmethod
    def get_by_name(cls, name: str) -> Self | None:
        return model.Session.query(cls).filter(cls.name == name).first()

    @classmethod
    def get_all(cls) -> list[Self]:
        return model.Session.query(cls).order_by(cls.modified_at.desc()).all()

    def dictize(self, context: types.Context) -> blocksmith_types.Menu:
        return blocksmith_types.Menu(
            id=str(self.id),
            name=str(self.name),
            items=[item.dictize(context) for item in self.items],  # type: ignore
            created_at=self.created_at.isoformat(),
            modified_at=self.modified_at.isoformat(),
        )


class MenuItemModel(tk.BaseModel, BaseModelMixin):
    __tablename__ = "blocksmith_menu_item"

    id = sa.Column(sa.Text, primary_key=True, default=make_uuid)
    title = sa.Column(sa.Text, nullable=False)
    url = sa.Column(sa.String, unique=True, nullable=False)
    order = sa.Column(sa.Integer, nullable=False, default=0)
    parent_id = sa.Column(sa.Text, nullable=True)
    classes = sa.Column("classes", sa.String, nullable=True)
    menu_id = sa.Column(sa.Text, sa.ForeignKey("blocksmith_menu.id"), nullable=False)

    menu = relationship("MenuModel", back_populates="items")

    @classmethod
    def get_by_id(cls, menu_item_id: str) -> Self | None:
        return model.Session.query(cls).filter(cls.id == menu_item_id).first()

    @classmethod
    def get_by_menu_id(cls, menu_id: str) -> list[Self]:
        return model.Session.query(cls).filter(cls.menu_id == menu_id).all()

    def dictize(self, context: types.Context) -> blocksmith_types.MenuItem:
        return blocksmith_types.MenuItem(
            id=str(self.id),
            title=str(self.title),
            url=str(self.url),
            order=int(self.order),  # type: ignore
            parent_id=str(self.parent_id) if self.parent_id else None,
            classes=str(self.classes) if self.classes else None,
            menu_id=str(self.menu_id),
        )
