from .generated.v3_0 import DescriptiveDetail as _DescriptiveDetail
from .generated.v3_0 import List17
from typing import TypeAlias
from .contributor import Contributor, ContributorRole

__all__ = ["DescriptiveDetail"]

_AUTHOR_ROLE: List17
LanguageEntry: TypeAlias = tuple[str, str]
ExtentEntry: TypeAlias = tuple[str, str, str]
SubjectEntry: TypeAlias = tuple[str, str]
MeasureEntry: TypeAlias = tuple[str, str, str]


class DescriptiveDetail:
    def __init__(self, raw: _DescriptiveDetail) -> None: ...    # pylint: disable=unused-argument

    @property
    def title(self) -> str: ...

    @title.setter
    def title(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def subtitle(self) -> str | None: ...

    @property
    def product_form(self) -> str: ...

    @property
    def product_composition(self) -> str: ...

    @property
    def contributors(self) -> list[Contributor]: ...

    def add_contributor(self, role: ContributorRole = ...) -> Contributor: ...    # pylint: disable=unused-argument

    @property
    def author(self) -> Contributor | None: ...

    @property
    def languages(self) -> list[LanguageEntry]: ...

    @property
    def extents(self) -> list[ExtentEntry]: ...

    @property
    def subjects(self) -> list[SubjectEntry]: ...

    @property
    def measures(self) -> list[MeasureEntry]: ...

    @property
    def raw(self) -> _DescriptiveDetail: ...

    def __repr__(self) -> str: ...
