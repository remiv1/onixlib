"""ONIX 3.0 facade models.

Re-exports the main facade classes for convenient top-level imports.
"""

from .book import Book  # backward compat alias for Product
from .collateral import CollateralDetail
from .contributor import Contributor, ContributorRole
from .descriptive import DescriptiveDetail
from .header import Header
from .notice import Notice, parse
from .product import Product
from .product_supply import Price, ProductSupply, SupplyDetail
from .publishing import PublishingDetail
from .related_material import RelatedMaterial, RelatedProduct, RelatedWork
from .versions import VersionInfo, available_releases, register

__all__ = [
    "Book",
    "CollateralDetail",
    "Contributor",
    "ContributorRole",
    "DescriptiveDetail",
    "Header",
    "Notice",
    "parse",
    "Price",
    "Product",
    "ProductSupply",
    "PublishingDetail",
    "RelatedMaterial",
    "RelatedProduct",
    "RelatedWork",
    "SupplyDetail",
    # Versioning
    "VersionInfo",
    "available_releases",
    "register",
]
