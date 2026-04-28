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

from onixlib.models.book import Book  # backward compat alias
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
