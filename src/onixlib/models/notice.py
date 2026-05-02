"""Facade for the ONIX 3.0 ONIXMessage (Notice) and streaming parser.

:class:`Notice` wraps the xsdata-generated
:class:`~onixlib.models.generated.v3_0.Onixmessage` dataclass and exposes the
header and the list of products through their respective facades.

:func:`parse` is a streaming generator that yields one
:class:`~onixlib.models.product.Product` per ``<Product>`` element without
loading the entire file into memory.

Example usage::

    # Streaming (memory-efficient, recommended for large files)
    from onixlib import parse

    for product in parse("notice.xml"):
        print(product.isbn, product.title)
        print(product.collateral.description)
        for ps in product.product_supply:
            for price in ps.prices:
                print(price.amount, price.currency)

    # Full load (convenient for small files)
    from onixlib.models.notice import Notice

    notice = Notice.parse_full("notice.xml")
    print(notice.header.sender_name)
    for product in notice.products:
        print(product.isbn, product.title)
"""

from __future__ import annotations

from io import BytesIO, StringIO
from pathlib import Path
from typing import BinaryIO, Generator, Union
from xml.etree.ElementTree import iterparse, tostring

from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .generated.v3_0 import (
    Onixmessage as _Onixmessage,
    OnixmessageRelease,
)
from .header import Header
from .product import Product
from . import versions as _versions

__all__ = ["Notice", "parse"]

_xml_context = XmlContext()
_xml_parser = XmlParser(context=_xml_context)
_xml_serializer = XmlSerializer(
    context=_xml_context,
    config=SerializerConfig(indent="  ", xml_declaration=True),
)

_DEFAULT_RELEASE = "3.0"


# ---------------------------------------------------------------------------
# Streaming parser
# ---------------------------------------------------------------------------

def parse(
    source: Union[str, Path, BinaryIO],
    version: str | None = None,
) -> Generator[Product, None, None]:
    """Stream an ONIX file, yielding one :class:`Product` per ``<Product>``.

    Each ``<Product>`` element is deserialised independently via xsdata so
    the entire file is never held in memory at once.  This is the recommended
    approach for large ONIX feeds.

    The ONIX version is auto-detected from the ``release`` attribute on the
    root element.  Pass *version* explicitly (e.g. ``"3.0"``) to skip
    detection or to force a specific version.

    Args:
        source:  Path to the XML file (``str`` or :class:`~pathlib.Path`),
                 or a binary file object opened for reading.
        version: ONIX release string (e.g. ``"3.0"``).  When ``None``
                 (default), the version is detected from the ``release``
                 attribute of the root element.

    Yields:
        A :class:`~onixlib.models.product.Product` facade for every product.

    Raises:
        KeyError: if the detected or requested version is not registered.
    """
    if isinstance(source, Path):
        source = str(source)

    product_tag: str | None = None
    product_class: type | None = None

    if version is not None:
        info = _versions.get(version)
        product_tag = f"{{{info.namespace}}}Product"
        product_class = info.product_class

    for event, elem in iterparse(source, events=("start", "end")):
        if event == "start" and product_tag is None:
            # First start event → root element; detect version from release attr.
            release = elem.get("release", _DEFAULT_RELEASE)
            info = _versions.get(release)
            product_tag = f"{{{info.namespace}}}Product"
            product_class = info.product_class
        elif event == "end" and product_tag and elem.tag == product_tag:
            xml_bytes = tostring(elem, encoding="unicode").encode("utf-8")
            raw_product = _xml_parser.parse(  # pyright: ignore[reportUnknownVariableType]
                BytesIO(xml_bytes), product_class
            )
            yield Product(raw_product)  # pyright: ignore[reportUnknownArgumentType]
            elem.clear()


# --------------------------------------------------------------------------- #
# Notice facade                                                               #
# --------------------------------------------------------------------------- #

class Notice:
    """Ergonomic facade over the ONIX :class:`Onixmessage` dataclass."""

    def __init__(self, raw: _Onixmessage) -> None:
        self._raw = raw
        self._header: Header | None = None
        self._products: list[Product] | None = None

    # ------------------------------------------------------------------ #
    # Factories                                                            #
    # ------------------------------------------------------------------ #

    @classmethod
    def parse_full(
        cls,
        source: Union[str, Path, BinaryIO],
        version: str = _DEFAULT_RELEASE
    ) -> "Notice":
        """Load and parse an entire ONIX file into a :class:`Notice`.

        The whole file is loaded into memory at once.  Use :func:`parse`
        for large files instead.

        Args:
            source:  Path to the XML file (``str`` or :class:`~pathlib.Path`),
                     or a binary file object opened for reading.
            version: ONIX release string (e.g. ``"3.0"``).  Defaults to the
                     current default release.  Pass the appropriate value when
                     reading files of a different version.

        Returns:
            A :class:`Notice` wrapping the parsed :class:`Onixmessage`.
        """
        info = _versions.get(version)
        if isinstance(source, (str, Path)):
            with open(source, "rb") as fh:
                raw: _Onixmessage = _xml_parser.parse(fh, info.message_class)
        else:
            raw = _xml_parser.parse(source, info.message_class)
        return cls(raw)

    @classmethod
    def new(
        cls,
        sender_name: str,
        sent_datetime: str,
        release: str = _DEFAULT_RELEASE,
    ) -> "Notice":
        """Create a new empty ONIX message.

        Args:
            sender_name:    Human-readable name of the sending organisation.
            sent_datetime:  Send timestamp in ONIX format, e.g.
                            ``"20260428T040029Z"``.
            release:        ONIX release attribute (default ``"3.0"``).
                            Must match a registered version in
                            :mod:`onixlib.models.versions`.
        """
        _versions.get(release)  # validate version is registered
        header = Header.new(sender_name=sender_name, sent_datetime=sent_datetime)
        raw = _Onixmessage(
            header=header.raw,
            product=[],
            release=OnixmessageRelease(release),
        )
        return cls(raw)

    # ------------------------------------------------------------------ #
    # Header                                                               #
    # ------------------------------------------------------------------ #

    @property
    def header(self) -> Header:
        """Facade over the ``<Header>`` block."""
        if self._header is None:
            self._header = Header(self._raw.header)
        return self._header

    # ------------------------------------------------------------------ #
    # Products                                                             #
    # ------------------------------------------------------------------ #

    @property
    def products(self) -> list[Product]:
        """List of all :class:`Product` facades in this message."""
        if self._products is None:
            self._products = [Product(p) for p in self._raw.product]
        return self._products

    def add_product(self, product: Product) -> None:
        """Append a product to this notice.

        Args:
            product: A :class:`Product` facade (its underlying raw object
                     will be attached to the message).
        """
        self._raw.product.append(product.raw)
        if self._products is not None:
            self._products.append(product)

    # ------------------------------------------------------------------ #
    # Serialization                                                        #
    # ------------------------------------------------------------------ #

    def to_xml(self) -> str:
        """Serialize this notice to an ONIX 3.0 XML string."""
        release = self._raw.release.value if self._raw.release else _DEFAULT_RELEASE
        ns = _versions.get(release).namespace
        out = StringIO()
        _xml_serializer.write(out, self._raw, ns_map={None: ns})  # type: ignore[misc]
        return out.getvalue()

    # ------------------------------------------------------------------ #
    # Raw access                                                           #
    # ------------------------------------------------------------------ #

    @property
    def raw(self) -> _Onixmessage:
        """Returns the underlying xsdata :class:`Onixmessage` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        return (
            f"Notice("
            f"sender={self.header.sender_name!r}, "
            f"products={len(self._raw.product)})"
        )
