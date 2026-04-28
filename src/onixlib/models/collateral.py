"""Facade for the ONIX 3.0 CollateralDetail block."""

from __future__ import annotations

from typing import Any
from onixlib.models.generated.v3_0 import (
    CollateralDetail as _CollateralDetail,
    List153,
    List158,
    Text as _Text,
)

__all__ = ["CollateralDetail"]

_DESCRIPTION_TYPE = List153.VALUE_03  # "03" – Description (unrestricted length)
_FRONT_COVER_TYPE = List158.VALUE_01  # "01" – Front cover 2D


def _extract_text(text_obj: _Text | None) -> str:
    """Extract plain-text from an ONIX ``Text`` element.

    ``Text`` is a mixed-content element (XHTML allowed) whose ``content``
    field is a list of strings and inline element objects.  This helper
    joins all the string fragments, stripping surrounding whitespace.
    """
    if text_obj is None:
        return ""
    parts = [item for item in text_obj.content if isinstance(item, str)]
    return "".join(parts).strip()


class CollateralDetail:
    """Ergonomic facade over the ONIX :class:`CollateralDetail` dataclass."""

    def __init__(self, raw: _CollateralDetail) -> None:
        self._raw = raw

    # ------------------------------------------------------------------ #
    # Text contents                                                        #
    # ------------------------------------------------------------------ #

    @property
    def text_contents(self) -> list[tuple[str, str]]:
        """All text contents as ``(type_code, text)`` tuples.

        Type codes come from List 153.  The text may contain XHTML markup.
        """
        result: list[tuple[Any, str]] = []
        for tc in self._raw.text_content:
            type_code = tc.text_type.value.value if tc.text_type else ""
            text = _extract_text(tc.text)
            result.append((type_code, text))
        return result

    @property
    def description(self) -> str | None:
        """Main product description (TextType 03), or ``None`` if absent.

        Falls back to the first available text content if type 03 is not found.
        """
        # First pass: look for the canonical description type
        for tc in self._raw.text_content:
            if tc.text_type and tc.text_type.value == _DESCRIPTION_TYPE:
                return _extract_text(tc.text) or None
        # Fallback: first text content
        if self._raw.text_content:
            tc = self._raw.text_content[0]
            return _extract_text(tc.text) or None
        return None

    # ------------------------------------------------------------------ #
    # Supporting resources                                                 #
    # ------------------------------------------------------------------ #

    @property
    def supporting_resources(self) -> list[tuple[str, list[str]]]:
        """All supporting resources as ``(content_type_code, [url, ...])`` tuples.

        Content type codes come from List 158.  URLs are extracted from
        :class:`ResourceLink` elements across all :class:`ResourceVersion` items.
        """
        result: list[tuple[Any, list[str]]] = []
        for sr in self._raw.supporting_resource:
            content_type = sr.resource_content_type.value.value if sr.resource_content_type else ""
            urls: list[str] = []
            for rv in sr.resource_version:
                for rl in rv.resource_link:
                    if rl.value:
                        urls.append(rl.value)
            result.append((content_type, urls))
        return result

    def _find_cover_url(self) -> str | None:
        for sr in self._raw.supporting_resource:
            if getattr(sr.resource_content_type, "value", None) != _FRONT_COVER_TYPE:
                continue

            for rv in sr.resource_version:
                for rl in rv.resource_link:
                    if rl.value:
                        return rl.value

        return None

    @property
    def cover_url(self) -> str | None:
        """
        URL of the front cover image (ResourceContentType 01), or ``None``.

        Returns the first URL found in the first matching ResourceVersion.
        """
        return self._find_cover_url()


    # ------------------------------------------------------------------ #
    # Raw access                                                           #
    # ------------------------------------------------------------------ #

    @property
    def raw(self) -> _CollateralDetail:
        """Returns the underlying xsdata :class:`CollateralDetail` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        n_texts = len(self._raw.text_content)
        n_resources = len(self._raw.supporting_resource)
        return f"CollateralDetail(text_contents={n_texts}, supporting_resources={n_resources})"
