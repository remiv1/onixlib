"""Gestion du manifeste .meta.toml pour les fichiers XSD ONIX."""

from __future__ import annotations

import hashlib
import tomllib
from datetime import datetime, timezone
from logging import getLogger
from pathlib import Path
from typing import Any

META_FILENAME = ".meta.toml"

logger = getLogger(__name__)


def _compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


class Meta:
    """Gère le fichier .meta.toml associé à un répertoire de fichiers XSD."""

    def __init__(self, xsd_dir: Path) -> None:
        self.xsd_dir = xsd_dir
        self._path = xsd_dir / META_FILENAME

    def write(self, version: str, source: str) -> dict[str, str]:
        """
        Écrit .meta.toml avec SHA-256 et métadonnées.

        Arguments :
        - version : version ONIX (ex : "3.0")
        - source : source d'origine (URL ou chemin)

        Return :
        - dictionnaire des checksums {nom_fichier: sha256}
        """
        checksums = {
            xsd.name: _compute_sha256(xsd) for xsd in sorted(self.xsd_dir.glob("*.xsd"))
        }
        lines = [
            f'version = "{version}"',
            f'source = "{source}"',
            f'generated_at = "{datetime.now(timezone.utc).isoformat()}"',
            "",
            "[files]",
        ] + [f'"{fname}" = "{sha}"' for fname, sha in checksums.items()]
        self._path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        logger.info("Manifeste écrit : %s", self._path)
        return checksums

    def verify(self) -> bool:
        """
        Vérifie les checksums SHA-256 par rapport au .meta.toml.

        Return :
        - True si tous les fichiers sont intègres, False sinon
        """
        if not self._path.exists():
            return False
        with open(self._path, "rb") as f:
            meta = tomllib.load(f)
        for fname, expected_sha in meta.get("files", {}).items():
            actual = self.xsd_dir / fname
            if not actual.exists() or _compute_sha256(actual) != expected_sha:
                return False
        return True

    def read(self) -> dict[str, Any] | None:
        """
        Lit les métadonnées du .meta.toml si présent.

        Return :
        - dictionnaire des métadonnées ou None si .meta.toml absent
        """
        if not self._path.exists():
            return None
        with open(self._path, "rb") as f:
            return tomllib.load(f)
