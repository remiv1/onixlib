from dataclasses import dataclass
from types import ModuleType
from typing import Any


@dataclass(frozen=True)
class VersionInfo:
    release: str
    namespace: str
    module: ModuleType
    message_class: type[Any]
    product_class: type[Any]


def register(info: VersionInfo) -> None: ...    # pylint: disable=unused-argument
def get(release: str) -> VersionInfo: ...    # pylint: disable=unused-argument
def detect_release(namespace: str) -> str | None: ...    # pylint: disable=unused-argument
def available_releases() -> list[str]: ...
