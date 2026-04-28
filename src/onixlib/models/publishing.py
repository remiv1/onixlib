"""Facade for the ONIX 3.0 PublishingDetail block."""

from __future__ import annotations

from typing import Any
from .generated.v3_0 import (
    List163,
    PublishingDetail as _PublishingDetail,
)

__all__ = ["PublishingDetail"]

_PUBLICATION_DATE_ROLE = List163.VALUE_01  # "01" – Nominal publication date


class PublishingDetail:
    """Ergonomic facade over the ONIX :class:`PublishingDetail` dataclass."""

    def __init__(self, raw: _PublishingDetail) -> None:
        self._raw = raw

    # ------------------------------------------------------------------ #
    # Imprint                                                              #
    # ------------------------------------------------------------------ #

    @property
    def imprint_name(self) -> str | None:
        """Name of the first imprint, or ``None`` if absent."""
        if not self._raw.imprint:
            return None
        imp = self._raw.imprint[0]
        return imp.imprint_name.value if imp.imprint_name else None

    @imprint_name.setter
    def imprint_name(self, value: str) -> None:
        from .generated.v3_0 import Imprint as _Imprint, ImprintName    # pylint: disable=import-outside-toplevel
        if not self._raw.imprint:
            self._raw.imprint.append(_Imprint(imprint_name=ImprintName(value=value)))
        else:
            imp = self._raw.imprint[0]
            if imp.imprint_name is None:
                imp.imprint_name = ImprintName(value=value)
            else:
                imp.imprint_name.value = value

    # ------------------------------------------------------------------ #
    # Publisher                                                            #
    # ------------------------------------------------------------------ #

    @property
    def publisher_name(self) -> str | None:
        """Name of the first publisher, or ``None`` if absent."""
        if not self._raw.publisher:
            return None
        pub = self._raw.publisher[0]
        return pub.publisher_name.value if pub.publisher_name else None

    # ------------------------------------------------------------------ #
    # Publishing status                                                    #
    # ------------------------------------------------------------------ #

    @property
    def publishing_status(self) -> str | None:
        """Publishing status code (List 64), or ``None`` if absent.

        Common values: ``"02"`` = forthcoming, ``"04"`` = active,
        ``"07"`` = out of print.
        """
        if self._raw.publishing_status is None:
            return None
        return self._raw.publishing_status.value.value

    # ------------------------------------------------------------------ #
    # Publishing dates                                                     #
    # ------------------------------------------------------------------ #

    @property
    def publication_date(self) -> str | None:
        """Nominal publication date string (DateRole 01), or ``None`` if absent.

        The date string is in the format specified by the ``DateFormat``
        element in the same block (default YYYYMMDD).
        """
        for pd in self._raw.publishing_date:
            if pd.publishing_date_role and pd.publishing_date_role.value == _PUBLICATION_DATE_ROLE:
                return pd.date.value if pd.date else None
        # Fallback: first date found
        if self._raw.publishing_date:
            pd = self._raw.publishing_date[0]
            return pd.date.value if pd.date else None
        return None

    @property
    def publishing_dates(self) -> list[tuple[str, str]]:
        """All publishing dates as ``(role_code, date_string)`` tuples.

        Role codes come from List 163.
        """
        result: list[tuple[Any, Any]] = []
        for pd in self._raw.publishing_date:
            role = pd.publishing_date_role.value.value if pd.publishing_date_role else ""
            date = pd.date.value if pd.date else ""
            result.append((role, date))
        return result

    # ------------------------------------------------------------------ #
    # Raw access                                                           #
    # ------------------------------------------------------------------ #

    @property
    def raw(self) -> _PublishingDetail:
        """Returns the underlying xsdata :class:`PublishingDetail` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        return (
            f"PublishingDetail("
            f"publisher={self.publisher_name!r}, "
            f"status={self.publishing_status!r}, "
            f"date={self.publication_date!r})"
        )
