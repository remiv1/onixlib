"""Facade for the ONIX 3.0 RelatedMaterial block."""

from __future__ import annotations

from .generated.v3_0 import (
    List5,
    RelatedMaterial as _RelatedMaterial,
    RelatedProduct as _RelatedProduct,
    RelatedWork as _RelatedWork,
)

__all__ = ["RelatedMaterial"]

_ISBN13_TYPE = List5.VALUE_15  # "15" – ISBN-13


class RelatedProduct:
    """Lightweight facade over one ONIX ``<RelatedProduct>`` element."""

    def __init__(self, raw: _RelatedProduct) -> None:
        self._raw = raw

    @property
    def relation_codes(self) -> list[str]:
        """List of product relation codes (List 51)."""
        return [
            prc.value.value
            for prc in self._raw.product_relation_code
            if prc.value
        ]

    @property
    def isbn(self) -> str | None:
        """ISBN-13 of the related product, or ``None`` if not available."""
        for pi in self._raw.product_identifier:
            if pi.product_idtype and pi.product_idtype.value == _ISBN13_TYPE:
                return pi.idvalue.value if pi.idvalue else None
        return None

    @property
    def raw(self) -> _RelatedProduct:
        """Returns the underlying xsdata ``RelatedProduct`` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        return f"RelatedProduct(isbn={self.isbn!r}, relations={self.relation_codes!r})"


class RelatedWork:
    """Lightweight facade over one ONIX ``<RelatedWork>`` element."""

    def __init__(self, raw: _RelatedWork) -> None:
        self._raw = raw

    @property
    def relation_code(self) -> str | None:
        """Work relation code (List 179), or ``None`` if absent."""
        if self._raw.work_relation_code:
            return self._raw.work_relation_code.value.value
        return None

    @property
    def work_identifiers(self) -> list[tuple[str, str]]:
        """List of ``(idtype_code, idvalue)`` tuples for this work."""
        return [
            (
                wi.work_idtype.value.value if wi.work_idtype else "",
                wi.idvalue.value if wi.idvalue else "",
            )
            for wi in self._raw.work_identifier
        ]

    @property
    def raw(self) -> _RelatedWork:
        """Returns the underlying xsdata ``RelatedWork`` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        r = f"RelatedWork(relation={self.relation_code!r}, identifiers={self.work_identifiers!r})"
        return r


class RelatedMaterial:
    """Ergonomic facade over the ONIX :class:`RelatedMaterial` dataclass."""

    def __init__(self, raw: _RelatedMaterial) -> None:
        self._raw = raw

    # ------------------------------------------------------------------ #
    # Related products                                                     #
    # ------------------------------------------------------------------ #

    @property
    def related_products(self) -> list[RelatedProduct]:
        """All related products in this block."""
        return [RelatedProduct(rp) for rp in self._raw.related_product]

    # ------------------------------------------------------------------ #
    # Related works                                                        #
    # ------------------------------------------------------------------ #

    @property
    def related_works(self) -> list[RelatedWork]:
        """All related works in this block."""
        return [RelatedWork(rw) for rw in self._raw.related_work]

    # ------------------------------------------------------------------ #
    # Raw access                                                           #
    # ------------------------------------------------------------------ #

    @property
    def raw(self) -> _RelatedMaterial:
        """Returns the underlying xsdata :class:`RelatedMaterial` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        return (
            f"RelatedMaterial("
            f"related_products={len(self._raw.related_product)}, "
            f"related_works={len(self._raw.related_work)})"
        )
