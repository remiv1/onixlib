from pathlib import Path
from typing import BinaryIO, Generator
from typing import TypeAlias
from .generated.v3_0 import Onixmessage as _Onixmessage
from .header import Header
from .product import Product

__all__ = ["Notice", "parse"]

ProductStream: TypeAlias = Generator[Product, None, None]


def parse(source: str | Path | BinaryIO, version: str | None = None) -> ProductStream: ...    # pylint: disable=unused-argument


class Notice:
    def __init__(self, raw: _Onixmessage) -> None: ...    # pylint: disable=unused-argument

    @classmethod
    def parse_full(
        cls,
        source: str | Path | BinaryIO,    # pylint: disable=unused-argument
        version: str = "3.0",    # pylint: disable=unused-argument
    ) -> "Notice": ...

    @classmethod
    def new(
        cls,
        sender_name: str,    # pylint: disable=unused-argument
        sent_datetime: str,    # pylint: disable=unused-argument
        release: str = "3.0",    # pylint: disable=unused-argument
    ) -> "Notice": ...

    @property
    def header(self) -> Header: ...

    @property
    def products(self) -> list[Product]: ...

    def add_product(self, product: Product) -> None: ...    # pylint: disable=unused-argument

    def to_xml(self) -> str: ...

    @property
    def raw(self) -> _Onixmessage: ...

    def __repr__(self) -> str: ...
