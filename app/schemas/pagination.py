from typing import Annotated, TypeVar, Generic, Any, Sequence, Optional
from fastapi import Query
from pydantic import BaseModel
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
import math

class PaginationParams(BaseModel, AbstractParams):
    page: Annotated[int, Query(ge=1)] = 1
    size: Annotated[int, Query(ge=1, le=100)] = 5

    def to_raw_params(self):
        return RawParams(
            limit=self.size,
            offset=(self.page-1) * self.size
        )
    
T = TypeVar("T")
    
class Page(AbstractPage[T], Generic[T]):
    items: list[T]
    total: int
    current_page: int
    size: int
    pages: int

    __params_type__ = PaginationParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: PaginationParams,
        *,
        total: Optional[int] = None,
        **kwargs: Any
    ) -> "Page[T]":
        assert total is not None, "total must be provided"

        return cls(
            items=items,
            total=total or 0,
            current_page=params.page,
            size=params.size,
            pages=math.ceil(total/params.size) if total else 0
        )