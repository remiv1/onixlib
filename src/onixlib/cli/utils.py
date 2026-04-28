"""Utilitaires pour les commandes CLI."""

from __future__ import annotations

import zipfile
from pathlib import Path
from logging import getLogger

logger = getLogger(__name__)


def find_project_root() -> Path:
    """
    Trouve la racine du projet en cherchant un fichier pyproject.toml dans les parents.
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    return Path.cwd()


def is_url(source: str) -> bool:
    """
    Détermine si une source est une URL.

    Arguments :
    - source : chaîne à tester

    Return :
    - True si source est une URL, False sinon
    """
    return source.startswith("http://") or source.startswith("https://")


def is_zip(path: Path) -> bool:
    """
    Détermine si un chemin pointe vers un fichier ZIP valide.

    Arguments :
    - path : chemin vers le fichier à tester

    Return :
    - True si le fichier est un ZIP valide, False sinon
    """
    try:
        return zipfile.is_zipfile(path)
    except (OSError, zipfile.BadZipFile):
        return False


def extract_zip(zip_path: Path, dest_dir: Path) -> int:
    """
    Extrait les fichiers .xsd d'une archive ZIP vers un répertoire de destination.

    Arguments :
    - zip_path : chemin vers le fichier ZIP
    - dest_dir : répertoire où extraire les fichiers .xsd

    Return :
    - nombre de fichiers .xsd extraits
    """
    with zipfile.ZipFile(zip_path) as zf:
        xsd_files = [n for n in zf.namelist() if n.lower().endswith(".xsd")]
        if not xsd_files:
            logger.warning("Aucun fichier .xsd trouvé dans l'archive %s", zip_path)
            return 0
        for name in xsd_files:
            (dest_dir / Path(name).name).write_bytes(zf.read(name))
    logger.info("Extrait %d fichier(s) XSD de l'archive %s", len(xsd_files), zip_path)
    return len(xsd_files)
