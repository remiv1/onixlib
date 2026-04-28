"""Facade for the ONIX 3.0 DescriptiveDetail block."""

from __future__ import annotations

from typing import Any
from onixlib.models.generated.v3_0 import (  # pylint: disable=unused-import
    Contributor as _Contributor,  # pylint: disable=unused-import
    ContributorRole as _ContributorRole,  # pylint: disable=unused-import
    DescriptiveDetail as _DescriptiveDetail,  # pylint: disable=unused-import
    KeyNames,  # pylint: disable=unused-import  # type: ignore
    List15,  # pylint: disable=unused-import
    List17,  # pylint: disable=unused-import
    List149,  # pylint: disable=unused-import
    NamesBeforeKey,  # pylint: disable=unused-import  # type: ignore
    PersonName,  # pylint: disable=unused-import  # type: ignore
    TitleDetail as _TitleDetail,  # pylint: disable=unused-import
    TitleElement as _TitleElement,  # pylint: disable=unused-import
    TitleElementLevel,  # pylint: disable=unused-import
    TitleText,  # pylint: disable=unused-import
    TitleType,  # pylint: disable=unused-import
)  # pylint: disable=unused-import
from onixlib.models.contributor import Contributor, ContributorRole

__all__ = ["DescriptiveDetail"]

_MAIN_TITLE_TYPE = List15.VALUE_01      # "01" – distinctive title (book)
_PRODUCT_ELEMENT_LEVEL = List149.VALUE_01  # "01" – product level
_AUTHOR_ROLE = List17.A01               # "A01" – written by


class DescriptiveDetail:
    """Ergonomic facade over the ONIX :class:`DescriptiveDetail` dataclass."""

    def __init__(self, raw: _DescriptiveDetail) -> None:
        self._raw = raw
        self._contributors: list[Contributor] | None = None

    # ------------------------------------------------------------------ #
    # Title                                                                #
    # ------------------------------------------------------------------ #

    def _find_main_title_element(self):
        """Return the (td, te) pair for the main product title, or (None, None)."""
        for td in self._raw.title_detail:
            if td.title_type and td.title_type.value == _MAIN_TITLE_TYPE:
                for te in td.title_element:
                    if (
                        te.title_element_level
                        and te.title_element_level.value == _PRODUCT_ELEMENT_LEVEL
                    ):
                        return td, te
        return None, None

    @property
    def title(self) -> str:
        """Main title of the product (TitleType 01, element level 01)."""
        td, te = self._find_main_title_element()
        if te and te.title_text:
            return te.title_text.value

        # fallback
        for td in self._raw.title_detail:
            for te in td.title_element:
                if te.title_text:
                    return te.title_text.value
        return ""

    @title.setter
    def title(self, value: str) -> None:
        td, te = self._find_main_title_element()
        if te:
            if te.title_text is None:
                te.title_text = TitleText(value=value)
            else:
                te.title_text.value = value
            return

        # Build missing structure
        te = _TitleElement(
            title_element_level=TitleElementLevel(value=_PRODUCT_ELEMENT_LEVEL),
            title_text=TitleText(value=value),
        )
        td = _TitleDetail(
            title_type=TitleType(value=_MAIN_TITLE_TYPE),
            title_element=[te],
        )
        self._raw.title_detail.append(td)

    @property
    def subtitle(self) -> str | None:
        """Subtitle of the product, or ``None`` if absent."""
        for td in self._raw.title_detail:
            if td.title_type and td.title_type.value == _MAIN_TITLE_TYPE:
                for te in td.title_element:
                    if te.subtitle:
                        return te.subtitle.value
        return None

    # ------------------------------------------------------------------ #
    # Product form                                                         #
    # ------------------------------------------------------------------ #

    @property
    def product_form(self) -> str:
        """Product form code (List 150), e.g. ``"BC"`` for paperback."""
        return self._raw.product_form.value.value if self._raw.product_form else ""

    @property
    def product_composition(self) -> str:
        """Product composition code (List 2), e.g. ``"00"`` for single-component."""
        return self._raw.product_composition.value.value if self._raw.product_composition else ""

    # ------------------------------------------------------------------ #
    # Contributors                                                         #
    # ------------------------------------------------------------------ #

    @property
    def contributors(self) -> list[Contributor]:
        """All contributors for this product, in ONIX order."""
        if self._contributors is None:
            self._contributors = [Contributor(c) for c in self._raw.contributor]
        return self._contributors

    def add_contributor(self, role: ContributorRole = _AUTHOR_ROLE) -> Contributor:
        """Append a new contributor with the given role.

        Args:
            role: ONIX contributor role code (``List17`` enum value).
                  Defaults to ``A01`` (written by).

        Returns:
            The newly created :class:`Contributor` facade.
        """
        raw_c = _Contributor(
            contributor_role=[_ContributorRole(value=role)],
        )
        self._raw.contributor.append(raw_c)
        facade = Contributor(raw_c)
        if self._contributors is not None:
            self._contributors.append(facade)
        return facade

    @property
    def author(self) -> Contributor | None:
        """First contributor with role ``A01`` (written by), or ``None``."""
        for c in self.contributors:
            if c.role == _AUTHOR_ROLE:
                return c
        return None

    # ------------------------------------------------------------------ #
    # Languages                                                            #
    # ------------------------------------------------------------------ #

    @property
    def languages(self) -> list[tuple[str, str]]:
        """List of ``(role_code, language_code)`` tuples.

        Role codes come from List 22 (e.g. ``"01"`` = language of text).
        Language codes come from List 74 (ISO 639-2/B, e.g. ``"fre"``).
        """
        result: list[tuple[Any, Any]] = []
        for lang in self._raw.language:
            role = lang.language_role.value.value if lang.language_role else ""
            code = lang.language_code.value.value if lang.language_code else ""
            result.append((role, code))
        return result

    # ------------------------------------------------------------------ #
    # Extents                                                              #
    # ------------------------------------------------------------------ #

    @property
    def extents(self) -> list[tuple[str, str, str]]:
        """List of ``(extent_type, value, unit)`` tuples.

        All values are ONIX code strings (e.g. extent_type ``"00"`` = main
        content page count from List 23).
        """
        result: list[tuple[Any, Any, Any]] = []
        for ext in self._raw.extent:
            ext_type = ext.extent_type.value.value if ext.extent_type else ""
            ext_value = ext.extent_value.value if ext.extent_value else ""
            ext_unit = ext.extent_unit.value.value if ext.extent_unit else ""
            result.append((ext_type, ext_value, ext_unit))
        return result

    # ------------------------------------------------------------------ #
    # Subjects                                                             #
    # ------------------------------------------------------------------ #

    @property
    def subjects(self) -> list[tuple[str, str]]:
        """List of ``(scheme_code, subject_code_or_heading)`` tuples.

        Scheme codes come from List 27. The second element is the
        ``SubjectCode`` when available, otherwise ``SubjectHeadingText``.
        """
        result: list[tuple[Any, str]] = []
        for subj in self._raw.subject:
            scheme = subj.subject_scheme_identifier.value.value \
                        if subj.subject_scheme_identifier else ""
            code = ""
            if subj.subject_code:
                code = subj.subject_code.value
            elif subj.subject_heading_text:
                code = subj.subject_heading_text.value
            result.append((scheme, code))
        return result

    # ------------------------------------------------------------------ #
    # Measures                                                             #
    # ------------------------------------------------------------------ #

    @property
    def measures(self) -> list[tuple[str, str, str]]:
        """List of ``(measure_type, measurement, unit)`` tuples.

        Measure type codes come from List 48 (e.g. ``"01"`` = height).
        """
        result: list[tuple[Any, str, Any]] = []
        for meas in self._raw.measure:
            meas_type = meas.measure_type.value.value if meas.measure_type else ""
            measurement = meas.measurement.value if meas.measurement else ""
            unit = meas.measure_unit_code.value.value if meas.measure_unit_code else ""
            result.append((meas_type, str(measurement), unit))
        return result

    # ------------------------------------------------------------------ #
    # Raw access                                                           #
    # ------------------------------------------------------------------ #

    @property
    def raw(self) -> _DescriptiveDetail:
        """Returns the underlying xsdata :class:`DescriptiveDetail` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        return f"DescriptiveDetail(title={self.title!r}, product_form={self.product_form!r})"
