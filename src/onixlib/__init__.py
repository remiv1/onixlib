"""onixlib — public API.

Minimal usage::

    from onixlib import parse, Product, ContributorRole

    # Streaming parse
    for product in parse("notice.xml"):
        print(product.isbn, product.title)
        if product.author:
            print(product.author.full_name)
        if product.collateral:
            print(product.collateral.description)
        if product.publishing:
            print(product.publishing.publication_date)
        for ps in product.product_supply:
            for price in ps.prices:
                print(price.amount, price.currency)

    # Full load
    from onixlib import Notice
    notice = Notice.parse_full("notice.xml")
    print(notice.header.sender_name)

    # Build from scratch
    product = Product.new(isbn="9782070360024", title="Du côté de chez Swann")
    c = product.add_contributor(role=ContributorRole.A01)
    c.first_name = "Marcel"
    c.last_name  = "PROUST"
    print(product.to_xml())
"""

from .models.book import Book  # backward compat alias
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
    # Versioning
    "VersionInfo",
    "available_releases",
    "register",
]
