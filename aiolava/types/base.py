from typing import TypeVar, Generic

from pydantic import BaseModel
from pydantic.utils import ROOT_KEY


_T = TypeVar("_T")


class LavaType(BaseModel):
    class Config:
        allow_mutation = False


class RootMixin(BaseModel, Generic[_T]):
    def __iter__(self) -> _T:
        return iter(getattr(self, ROOT_KEY))

    def __getitem__(self, item) -> _T:
        return getattr(self, ROOT_KEY)[item]
