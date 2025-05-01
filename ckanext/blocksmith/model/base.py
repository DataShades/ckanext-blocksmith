from typing import Any

from typing_extensions import Self

import ckan.model as model


class BaseModelMixin:
    @classmethod
    def create(cls, data_dict: dict[str, Any]) -> Self:
        entity = cls(**data_dict)

        model.Session.add(entity)
        model.Session.commit()

        return entity

    def delete(self) -> None:
        model.Session().autoflush = False
        model.Session.delete(self)
        model.Session.commit()

    def update(self, data_dict: dict[str, Any]) -> None:
        for key, value in data_dict.items():
            setattr(self, key, value)
        model.Session.commit()
