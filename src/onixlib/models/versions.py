"""ONIX version registry.

Maps ONIX release strings (e.g. ``"3.0"``) to the generated module that
implements that version, along with its root message class, product class,
and XML namespace.

When a new ONIX release is generated (e.g. ``v3_1.py``), register it here::

    from onixlib.models.generated import v3_1 as _v3_1

    register(VersionInfo(
        release="3.1",
        namespace="http://www.editeur.org/onix/3.1/reference",
        module=_v3_1,
        message_class=_v3_1.Onixmessage,
        product_class=_v3_1.Product,
    ))

The :func:`parse` function in :mod:`onixlib.models.notice` uses this
registry to auto-detect the version of an incoming ONIX file.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import ModuleType
from typing import Any


@dataclass(frozen=True)
class VersionInfo:
    """Metadata about a registered ONIX version."""

    release: str         # e.g. "3.0"
    namespace: str       # XML namespace used by this release
    module: ModuleType   # generated module (e.g. v3_0)
    message_class: type[Any]  # Onixmessage class for this release
    product_class: type[Any]  # Product class for this release


_REGISTRY: dict[str, VersionInfo] = {}


def register(info: VersionInfo) -> None:
    """Register an ONIX version.

    Args:
        info: :class:`VersionInfo` describing the version.
    """
    _REGISTRY[info.release] = info


def get(release: str) -> VersionInfo:
    """Return the :class:`VersionInfo` for a registered ONIX version.

    Args:
        release: ONIX release string, e.g. ``"3.0"``.

    Raises:
        KeyError: if the version has not been registered.
    """
    if release not in _REGISTRY:
        available = list(_REGISTRY)
        raise KeyError(
            f"ONIX version {release!r} is not registered. "
            f"Available versions: {available}"
        )
    return _REGISTRY[release]


def detect_release(namespace: str) -> str | None:
    """Infer the ONIX release string from an XML namespace URI.

    Args:
        namespace: The XML namespace to look up, e.g.
                   ``"http://www.editeur.org/onix/3.0/reference"``.

    Returns:
        The matching release string, or ``None`` if the namespace is not
        recognised.
    """
    for info in _REGISTRY.values():
        if info.namespace == namespace:
            return info.release
    return None


def available_releases() -> list[str]:
    """Return the list of all registered release strings."""
    return list(_REGISTRY)


# --------------------------------------------------------------------------- #
# Built-in version registrations                                              #
# --------------------------------------------------------------------------- #

from onixlib.models.generated import v3_0 as _v3_0  # pylint: disable=wrong-import-position

register(VersionInfo(
    release="3.0",
    namespace="http://www.editeur.org/onix/3.0/reference",
    module=_v3_0,
    message_class=_v3_0.Onixmessage,
    product_class=_v3_0.Product,
))
