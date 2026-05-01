from .generated.v3_0 import RelatedMaterial as _RelatedMaterial
from .generated.v3_0 import RelatedProduct as _RelatedProduct
from .generated.v3_0 import RelatedWork as _RelatedWork
from typing import TypeAlias

__all__ = ["RelatedMaterial"]

WorkIdentifierEntry: TypeAlias = tuple[str, str]


class RelatedProduct:
    def __init__(self, raw: _RelatedProduct) -> None: ...    # pylint: disable=unused-argument

    @property
    def relation_codes(self) -> list[str]: ...

    @property
    def isbn(self) -> str | None: ...

    @property
    def raw(self) -> _RelatedProduct: ...

    def __repr__(self) -> str: ...


class RelatedWork:
    def __init__(self, raw: _RelatedWork) -> None: ...    # pylint: disable=unused-argument

    @property
    def relation_code(self) -> str | None: ...

    @property
    def work_identifiers(self) -> list[WorkIdentifierEntry]: ...

    @property
    def raw(self) -> _RelatedWork: ...

    def __repr__(self) -> str: ...


class RelatedMaterial:
    def __init__(self, raw: _RelatedMaterial) -> None: ...    # pylint: disable=unused-argument

    @property
    def related_products(self) -> list[RelatedProduct]: ...

    @property
    def related_works(self) -> list[RelatedWork]: ...

    @property
    def raw(self) -> _RelatedMaterial: ...

    def __repr__(self) -> str: ...
