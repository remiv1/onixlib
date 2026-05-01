"""onixlib - Une bibliothèque Python pour manipuler les fichiers ONIX."""

from .models.book import Book
from .models.collateral import CollateralDetail
from .models.contributor import Contributor, ContributorRole
from .models.descriptive import DescriptiveDetail
from .models.header import Header
from .models.notice import Notice, parse
from .models.product import Product
from .models.product_supply import Price, ProductSupply, SupplyDetail
from .models.publishing import PublishingDetail
from .models.related_material import RelatedMaterial, RelatedProduct, RelatedWork
from .models.versions import VersionInfo, available_releases, register

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
    "VersionInfo",
    "available_releases",
    "register",
]
