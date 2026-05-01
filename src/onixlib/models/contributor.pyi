from .generated.v3_0 import Contributor as _Contributor
from .generated.v3_0 import List17 as ContributorRole

__all__ = ["Contributor", "ContributorRole"]


class Contributor:
    def __init__(self, raw: _Contributor | None = None) -> None: ...    # pylint: disable=unused-argument

    @property
    def first_name(self) -> str: ...

    @first_name.setter
    def first_name(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def last_name(self) -> str: ...

    @last_name.setter
    def last_name(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def role(self) -> ContributorRole | None: ...

    @role.setter
    def role(self, value: ContributorRole) -> None: ...    # pylint: disable=unused-argument

    @property
    def full_name(self) -> str: ...

    @property
    def raw(self) -> _Contributor: ...

    def __repr__(self) -> str: ...
