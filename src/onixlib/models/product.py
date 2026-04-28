"""Facade for the ONIX 3.0 Product block.

This is the central facade: it wraps the xsdata-generated
:class:`~onixlib.models.generated.v3_0.Product` dataclass and composes the
per-block facades (:class:`~onixlib.models.descriptive.DescriptiveDetail`,
:class:`~onixlib.models.collateral.CollateralDetail`, etc.).

Example usage::

    from onixlib import parse

    for product in parse("notice.xml"):
        print(product.isbn, product.title)
        for c in product.contributors:
            print(c.role, c.full_name)
        print(product.collateral.description)
        print(product.publishing.publication_date)
        for ps in product.product_supply:
            for price in ps.prices:
                print(price.amount, price.currency)
"""

from __future__ import annotations

from io import StringIO

from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from onixlib.models.collateral import CollateralDetail
from onixlib.models.contributor import Contributor, ContributorRole
from onixlib.models.descriptive import DescriptiveDetail
from onixlib.models.generated.v3_0 import (
    DescriptiveDetail as _DescriptiveDetail,
    Idvalue,
    List1,
    List2,
    List5,
    List150,
    NotificationType,
    Product as _Product,
    ProductComposition,
    ProductForm,
    ProductIdentifier,
    ProductIdtype,
    RecordReference,
)
from onixlib.models.product_supply import ProductSupply
from onixlib.models.publishing import PublishingDetail
from onixlib.models.related_material import RelatedMaterial

__all__ = ["Product"]

_ISBN13_TYPE = List5.VALUE_15  # "15" – ISBN-13
_GTIN13_TYPE = List5.VALUE_03  # "03" – GTIN-13

_context = XmlContext()
_serializer = XmlSerializer(
    context=_context,
    config=SerializerConfig(pretty_print=True, xml_declaration=True),
)


class Product:
    """Ergonomic facade over the ONIX :class:`Product` dataclass."""

    def __init__(self, raw: _Product) -> None:
        self._raw = raw
        self._descriptive: DescriptiveDetail | None = None
        self._collateral: CollateralDetail | None = None
        self._publishing: PublishingDetail | None = None
        self._related_material: RelatedMaterial | None = None

    # ------------------------------------------------------------------ #
    # Factory                                                              #
    # ------------------------------------------------------------------ #

    @classmethod
    def new(
        cls,
        isbn: str | None = None,
        title: str | None = None,
        product_form: str = "BC",
        product_composition: str = "00",
    ) -> "Product":
        """Create a new Product with sensible defaults.

        Args:
            isbn:                ISBN-13 (no dashes).
            title:               Main title.
            product_form:        ONIX List 150 code, e.g. ``"BC"`` (paperback),
                                 ``"BB"`` (hardback).
            product_composition: ONIX List 2 code, e.g. ``"00"`` (single-component).
        """
        pf_enum = List150(product_form)
        pc_enum = List2(product_composition)
        descriptive = _DescriptiveDetail(
            product_composition=ProductComposition(value=pc_enum),
            product_form=ProductForm(value=pf_enum),
        )
        raw = _Product(
            record_reference=RecordReference(value=isbn or ""),
            notification_type=NotificationType(value=List1.VALUE_03),
            product_identifier=[],
            descriptive_detail=descriptive,
        )
        product = cls(raw)
        if isbn:
            product.isbn = isbn
        if title:
            product.title = title
        return product

    # ------------------------------------------------------------------ #
    # Identifier                                                           #
    # ------------------------------------------------------------------ #

    @property
    def isbn(self) -> str | None:
        """ISBN-13 (or GTIN-13) of the product, or ``None`` if absent."""
        for pi in self._raw.product_identifier:
            if pi.product_idtype.value in (_ISBN13_TYPE, _GTIN13_TYPE):
                return pi.idvalue.value
        return None

    @isbn.setter
    def isbn(self, value: str) -> None:
        for pi in self._raw.product_identifier:
            if pi.product_idtype.value == _ISBN13_TYPE:
                pi.idvalue.value = value
                return
        self._raw.product_identifier.append(
            ProductIdentifier(
                product_idtype=ProductIdtype(value=_ISBN13_TYPE),
                idvalue=Idvalue(value=value),
            )
        )

    # ------------------------------------------------------------------ #
    # Title / author shortcuts (delegate to descriptive)                  #
    # ------------------------------------------------------------------ #

    @property
    def title(self) -> str:
        """Main title of the product. Delegates to :attr:`descriptive`."""
        return self.descriptive.title if self.descriptive else ""

    @title.setter
    def title(self, value: str) -> None:
        if self.descriptive is None:
            raise AttributeError(
                "This product has no DescriptiveDetail. "
                "Use Product.new() or initialise raw.descriptive_detail first."
            )
        self.descriptive.title = value

    @property
    def contributors(self) -> list[Contributor]:
        """All contributors. Delegates to :attr:`descriptive`."""
        return self.descriptive.contributors if self.descriptive else []

    def add_contributor(self, role: ContributorRole = ContributorRole.A01) -> Contributor:
        """Append a contributor. Delegates to :attr:`descriptive`.

        Args:
            role: ONIX contributor role (``List17`` enum). Defaults to ``A01``.
        """
        if self.descriptive is None:
            raise AttributeError(
                "This product has no DescriptiveDetail. "
                "Use Product.new() or initialise raw.descriptive_detail first."
            )
        return self.descriptive.add_contributor(role)

    @property
    def author(self) -> Contributor | None:
        """First contributor with role ``A01`` (written by). Delegates to :attr:`descriptive`."""
        return self.descriptive.author if self.descriptive else None

    # ------------------------------------------------------------------ #
    # Block facades                                                        #
    # ------------------------------------------------------------------ #

    @property
    def descriptive(self) -> DescriptiveDetail | None:
        """Facade over the ``<DescriptiveDetail>`` block, or ``None``."""
        if self._descriptive is None and self._raw.descriptive_detail is not None:
            self._descriptive = DescriptiveDetail(self._raw.descriptive_detail)
        return self._descriptive

    @property
    def collateral(self) -> CollateralDetail | None:
        """Facade over the ``<CollateralDetail>`` block, or ``None``."""
        if self._collateral is None and self._raw.collateral_detail is not None:
            self._collateral = CollateralDetail(self._raw.collateral_detail)
        return self._collateral

    @property
    def publishing(self) -> PublishingDetail | None:
        """Facade over the ``<PublishingDetail>`` block, or ``None``."""
        if self._publishing is None and self._raw.publishing_detail is not None:
            self._publishing = PublishingDetail(self._raw.publishing_detail)
        return self._publishing

    @property
    def product_supply(self) -> list[ProductSupply]:
        """List of facades over each ``<ProductSupply>`` block."""
        return [ProductSupply(ps) for ps in self._raw.product_supply]

    @property
    def related_material(self) -> RelatedMaterial | None:
        """Facade over the ``<RelatedMaterial>`` block, or ``None``."""
        if self._related_material is None and self._raw.related_material is not None:
            self._related_material = RelatedMaterial(self._raw.related_material)
        return self._related_material

    # ------------------------------------------------------------------ #
    # Serialization                                                        #
    # ------------------------------------------------------------------ #

    def to_xml(self) -> str:
        """Serialize this product to an ONIX 3.0 XML string."""
        out = StringIO()
        _serializer.write(out, self._raw)
        return out.getvalue()

    # ------------------------------------------------------------------ #
    # Raw access                                                           #
    # ------------------------------------------------------------------ #

    @property
    def raw(self) -> _Product:
        """Returns the underlying xsdata :class:`Product` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        return f"Product(isbn={self.isbn!r}, title={self.title!r})"
