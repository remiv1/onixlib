"""
CLI onix-generate — Télécharge les XSD ONIX, gère les versions et génère les dataclasses Python.

Usages :
    onix-generate --source https://editeur.org/.../xsd.zip --version 3.0
    onix-generate --source /chemin/vers/xsds/ --version 3.0
    onix-generate --from-file xsd_sources.toml
    onix-generate --from-file xsd_sources.toml --version 3.0
    onix-generate --list-versions
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import tomllib
import urllib.request
from typing import Any
from logging import getLogger
from pathlib import Path
from .meta import Meta
from .utils import find_project_root, is_url, is_zip, extract_zip

PROJECT_ROOT = find_project_root()
DEFAULT_XSD_BASE_DIR = PROJECT_ROOT / "documentations" / "xsd_onix3"
DEFAULT_SRC_DIR = PROJECT_ROOT / "src"
DEFAULT_SOURCES_FILE = PROJECT_ROOT / "xsd_sources.toml"


logger = getLogger(__name__)


def normalize_version(version: str) -> str:
    """
    Convertit une version X.Y en suffixe de package vX_Y.

    Arguments :
    - version : chaîne de version (ex : "3.0")

    Return :
    - suffixe de package (ex : "v3_0")
    """
    return "v" + version.replace(".", "_")


def resolve_path(raw: str, base: Path) -> Path:
    """
    Résout un chemin local, relatif à base si nécessaire.

    Arguments :
    - raw : chemin brut (absolu ou relatif)
    - base : chemin de base pour les chemins relatifs

    Return :
    - Path absolu vers le fichier ou dossier
    """
    p = Path(raw)
    return p if p.is_absolute() else (base / p).resolve()


def _download_source_from_url(source: str, dest_dir: Path) -> None:
    if not source.startswith("https://"):
        logger.warning("URL non-HTTPS détectée : %s", source)
    logger.info("Téléchargement depuis %s", source)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
        tmp_path = Path(tmp.name)
    try:
        urllib.request.urlretrieve(source, tmp_path)
        if is_zip(tmp_path):
            extract_zip(tmp_path, dest_dir)
        else:
            fname = source.rstrip("/").split("/")[-1]
            if not fname.lower().endswith(".xsd"):
                fname += ".xsd"
            shutil.copy2(tmp_path, dest_dir / fname)
    finally:
        tmp_path.unlink(missing_ok=True)


def _download_source_from_path(source_path: Path, dest_dir: Path) -> None:
    if not source_path.exists():
        logger.error("Chemin introuvable : %s", source_path)
        sys.exit(1)
    if source_path.is_dir():
        xsd_files = list(source_path.glob("*.xsd"))
        if not xsd_files:
            logger.error("Aucun fichier .xsd trouvé dans le dossier : %s", source_path)
            sys.exit(1)
        if source_path.resolve() == dest_dir.resolve():
            logger.debug(
                "Source et destination identiques (%s), aucune copie nécessaire.",
                source_path,
            )
        else:
            for xsd in xsd_files:
                shutil.copy2(xsd, dest_dir / xsd.name)
            logger.debug(
                "Copié %d fichier(s) XSD depuis %s", len(xsd_files), source_path
            )
    elif source_path.suffix.lower() == ".zip":
        extract_zip(source_path, dest_dir)
    elif source_path.suffix.lower() == ".xsd":
        shutil.copy2(source_path, dest_dir / source_path.name)
    else:
        logger.error("Type de source non reconnu : %s", source_path)
        sys.exit(1)


def download_source(source: str, dest_dir: Path, base_path: Path) -> None:
    """
    Télécharge ou copie les XSD depuis une URL ou un chemin local.

    Arguments :
    - source : URL ou chemin local vers les XSD (dossier ou ZIP)
    - dest_dir : répertoire de destination pour les XSD extraits
    - base_path : chemin de base pour résoudre les chemins relatifs

    Return :
    - None (les fichiers sont écrits dans dest_dir)
    """
    dest_dir.mkdir(parents=True, exist_ok=True)

    if is_url(source):
        _download_source_from_url(source, dest_dir)
    else:
        source_path = resolve_path(source, base_path)
        _download_source_from_path(source_path, dest_dir)


def generate_models(version: str, xsd_dir: Path, src_dir: Path) -> None:
    """
    Lance xsdata pour générer les dataclasses dans models/generated/v{X_Y}.py.

    Arguments :
    - version : version ONIX (ex : "3.0")
    - xsd_dir : répertoire contenant les fichiers .xsd
    - src_dir : répertoire src Python de base (contenant onixlib/)

    Return :
    - None (les fichiers sont écrits dans src_dir/onixlib/models/generated/)
    """
    pkg_suffix = normalize_version(version)
    package = f"onixlib.models.generated.{pkg_suffix}"
    # xsdata single-package écrit un fichier .py dans le package parent
    (src_dir / "onixlib" / "models" / "generated").mkdir(parents=True, exist_ok=True)

    # On passe uniquement le XSD d'entrée "reference" plutôt que tout le dossier.
    # Cela évite que xsdata traite aussi les variantes "_short" et les doublons
    # XHTML (ONIX_XHTML_Subset_reference.xsd / _short.xsd), qui produiraient
    # ~130 warnings "Duplicate type". xsdata résout les xs:import automatiquement.
    reference_xsd = next(xsd_dir.glob("*reference*.xsd"), None)
    xsd_source = str(reference_xsd) if reference_xsd else str(xsd_dir)
    if reference_xsd:
        logger.debug("Entrée XSD : %s (imports résolus automatiquement)", reference_xsd.name)
    else:
        logger.warning("Aucun fichier *reference*.xsd trouvé, passage du dossier entier.")

    cmd = [
        sys.executable,
        "-m",
        "xsdata",
        "generate",
        xsd_source,
        "--package",
        package,
        "--output",
        "dataclasses",
        "--structure-style",
        "single-package",
        "--docstring-style",
        "reStructuredText",
    ]
    logger.info("Génération des modèles pour ONIX %s", version)
    logger.debug("Commande xsdata : %s", " ".join(cmd))
    result = subprocess.run(cmd, cwd=src_dir, check=True)  # package résolu depuis src/
    if result.returncode != 0:
        logger.error("xsdata a échoué avec le code %d", result.returncode)
        sys.exit(result.returncode)
    logger.info(
        "Modèles générés pour ONIX %s dans %s",
        version,
        package.replace(".", "/") + ".py",
    )


def process_version(
    version: str,
    source: str,
    base_path: Path,
    xsd_base_dir: Path,
    src_dir: Path,
    force: bool = False,
) -> None:
    """
    Traite une version ONIX : télécharge les XSD, vérifie l'intégrité, génère les modèles.

    Arguments :
    - version : version ONIX (ex : "3.0")
    - source : URL ou chemin local vers les XSD
    - base_path : chemin de base pour résoudre les chemins relatifs
    - xsd_base_dir : répertoire de base pour stocker les XSD versionnés
    - src_dir : répertoire src Python de base (contenant onixlib/)
    - force : si True, force le re-téléchargement même si les XSD sont déjà intègres
    """
    logger.info("Traitement de la version ONIX %s", version)
    print(f"\n{'='*60}")
    print(f"  ONIX {version}")
    print(f"{'='*60}")
    xsd_dir = xsd_base_dir / version
    if xsd_dir.exists() and Meta(xsd_dir).verify() and not force:
        logger.warning(
            "XSD déjà intègres pour ONIX %s dans %s (--force pour re-télécharger).",
            version,
            xsd_dir.relative_to(PROJECT_ROOT),
        )
    else:
        download_source(source, xsd_dir, base_path)
        Meta(xsd_dir).write(version, source)
    generate_models(version, xsd_dir, src_dir)
    logger.info("Version ONIX %s traitée avec succès.", version)


def list_versions(sources_file: Path, xsd_base_dir: Path) -> None:
    """
    Affiche les versions définies dans le fichier de sources avec leur statut d'intégrité.

    Arguments :
    - sources_file : chemin vers le fichier TOML de sources
    - xsd_base_dir : répertoire de base où sont stockés les XSD versionnés

    Return :
    - None (affiche la liste des versions et leur statut)
    """
    if not sources_file.exists():
        logger.error("Fichier introuvable : %s", sources_file)
        sys.exit(1)
    with open(sources_file, "rb") as f:
        config = tomllib.load(f)
    versions = config.get("versions", {})
    if not versions:
        logger.warning("Aucune version définie dans %s", sources_file)
        return
    logger.info("Versions définies dans %s : %d", sources_file, len(versions))
    for ver, cfg in versions.items():
        meta = Meta(xsd_base_dir / ver).read()
        status = "✓ téléchargée" if meta else "  non téléchargée"
        logger.info("Version %s : %s", ver, status.strip())
        print(f"  {ver}  [{status}]  {cfg.get('description', '')}")
        if meta:
            print(f"         source    : {meta.get('source', '?')}")
            print(f"         téléchargé: {meta.get('generated_at', '?')}")
    print()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="onix-generate",
        description="Télécharge les XSD ONIX et génère les dataclasses Python versionnées.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
    onix-generate --source https://editeur.org/.../ONIX_3-0_XSD.zip --version 3.0
    onix-generate --source /chemin/vers/xsds/ --version 3.0
    onix-generate --from-file xsd_sources.toml
    onix-generate --from-file xsd_sources.toml --version 3.0
    onix-generate --list-versions
    onix-generate --from-file xsd_sources.toml --version 3.0 --force
        """,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--source",
        metavar="URL_OU_CHEMIN",
        help="URL HTTPS, dossier ou zip contenant les XSD.",
    )
    group.add_argument(
        "--from-file",
        metavar="FICHIER_TOML",
        nargs="?",
        const=str(DEFAULT_SOURCES_FILE),
        help=f"Fichier TOML de sources (défaut : {DEFAULT_SOURCES_FILE.name}).",
    )
    group.add_argument(
        "--list-versions",
        action="store_true",
        help="Liste les versions et leur statut.",
    )
    parser.add_argument(
        "--version",
        metavar="X.Y",
        help="Version ONIX (ex : 3.0). Requis avec --source.",
    )
    parser.add_argument(
        "--xsd-dir",
        metavar="CHEMIN",
        default=None,
        help="Répertoire de stockage des XSD versionnés.",
    )
    parser.add_argument(
        "--output-dir",
        metavar="CHEMIN",
        default=None,
        help="Répertoire src Python de sortie.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force le re-téléchargement même si XSD déjà intègres.",
    )
    return parser


def _process_from_file(
    parser: argparse.ArgumentParser,
    sources_file: Path,
    version: str | None,
    xsd_base_dir: Path,
    src_dir: Path,
    force: bool,
) -> None:
    if not sources_file.exists():
        parser.error(f"Fichier introuvable : {sources_file}")

    with open(sources_file, "rb") as f:
        config = tomllib.load(f)
    versions_cfg: dict[str, Any] = config.get("versions", {})
    if not versions_cfg:
        parser.error(f"Aucune version définie dans {sources_file}.")

    target_versions: list[str] = [version] if version else list(versions_cfg.keys())
    for ver in target_versions:
        if ver not in versions_cfg:
            print(
                f"Version '{ver}' introuvable dans {sources_file.name}.",
                file=sys.stderr,
            )
            sys.exit(1)
        ver_cfg: dict[str, Any] = versions_cfg[ver]
        if "source" not in ver_cfg:
            print(f"Clé 'source' manquante pour la version {ver}.", file=sys.stderr)
            sys.exit(1)
        process_version(
            ver, ver_cfg["source"], sources_file.parent, xsd_base_dir, src_dir, force
        )


def main() -> None:
    """
    Point d'entrée du CLI onix-generate.
    """
    parser = _build_parser()
    args = parser.parse_args()

    xsd_base_dir: Path = (
        Path(args.xsd_dir).resolve() if args.xsd_dir else DEFAULT_XSD_BASE_DIR
    )
    src_dir: Path = (
        Path(args.output_dir).resolve() if args.output_dir else DEFAULT_SRC_DIR
    )

    if args.list_versions:
        sf = Path(args.from_file).resolve() if args.from_file else DEFAULT_SOURCES_FILE
        list_versions(sf, xsd_base_dir)
        return

    if args.source:
        if not args.version:
            parser.error("--version est requis avec --source (ex : --version 3.0).")
        process_version(
            args.version, args.source, PROJECT_ROOT, xsd_base_dir, src_dir, args.force
        )
        return

    _process_from_file(
        parser,
        Path(args.from_file).resolve(),
        args.version,
        xsd_base_dir,
        src_dir,
        args.force,
    )


if __name__ == "__main__":
    main()
