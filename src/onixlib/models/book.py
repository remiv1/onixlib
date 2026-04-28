"""Backward-compatibility re-export.

``Book`` is an alias for :class:`~onixlib.models.product.Product`.

New code should import :class:`~onixlib.models.product.Product` directly.
"""

from .product import Product as Book  # noqa: F401

__all__ = ["Book"]
