from .generated.v3_0 import PublishingDetail as _PublishingDetail
from typing import TypeAlias

__all__ = ["PublishingDetail"]

PublishingDateEntry: TypeAlias = tuple[str, str]


class PublishingDetail:
    def __init__(self, raw: _PublishingDetail) -> None: ...    # pylint: disable=unused-argument

    @property
    def imprint_name(self) -> str | None: ...

    @imprint_name.setter
    def imprint_name(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def publisher_name(self) -> str | None: ...

    @property
    def publishing_status(self) -> str | None: ...

    @property
    def publication_date(self) -> str | None: ...

    @property
    def publishing_dates(self) -> list[PublishingDateEntry]: ...

    @property
    def raw(self) -> _PublishingDetail: ...

    def __repr__(self) -> str: ...
