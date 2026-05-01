"""stub for collateral module"""

from .generated.v3_0 import CollateralDetail as _CollateralDetail
from typing import TypeAlias

__all__ = ["CollateralDetail"]

TextContentEntry: TypeAlias = tuple[str, str]
SupportingResourceEntry: TypeAlias = tuple[str, list[str]]


class CollateralDetail:
    def __init__(self, raw: _CollateralDetail) -> None: ... # pylint: disable=unused-argument

    @property
    def text_contents(self) -> list[TextContentEntry]: ...

    @property
    def description(self) -> str | None: ...

    @property
    def supporting_resources(self) -> list[SupportingResourceEntry]: ...

    @property
    def cover_url(self) -> str | None: ...

    @property
    def raw(self) -> _CollateralDetail: ...

    def __repr__(self) -> str: ...
