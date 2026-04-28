"""ONIX 3.0 facade models.

Re-exports the main facade classes for convenient top-level imports.
"""

from onixlib.models.book import Book  # backward compat alias for Product
from onixlib.models.collateral import CollateralDetail
from onixlib.models.contributor import Contributor, ContributorRole
from onixlib.models.descriptive import DescriptiveDetail
from onixlib.models.header import Header
from onixlib.models.notice import Notice, parse
from onixlib.models.product import Product
from onixlib.models.product_supply import Price, ProductSupply, SupplyDetail
from onixlib.models.publishing import PublishingDetail
from onixlib.models.related_material import RelatedMaterial, RelatedProduct, RelatedWork
from onixlib.models.versions import VersionInfo, available_releases, register

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
