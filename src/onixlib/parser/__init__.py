"""Streaming ONIX 3.0 parser.

For backward compatibility, this module re-exports :func:`parse` from
:mod:`onixlib.models.notice`.

Prefer importing directly from :mod:`onixlib` or :mod:`onixlib.models.notice`.
"""

from ..models.notice import parse  # noqa: F401

__all__ = ["parse"]
