"""Tests pour le registre de versions ONIX (onixlib.models.versions)."""

from __future__ import annotations

import pytest   # pyright: ignore[reportUnusedImport] # pylint: disable=unused-import
import types

from onixlib.models import versions as _ver
from onixlib.models.versions import VersionInfo, available_releases, detect_release, get, register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_fake_version(release: str, namespace: str) -> VersionInfo:

    mod = types.ModuleType(f"fake_{release.replace('.', '_')}")

    class FakeMessage:
        """Classe de message factice pour les tests de registre de versions."""
        pass    # pylint: disable=unnecessary-pass

    class FakeProduct:
        """Classe de produit factice pour les tests de registre de versions."""
        pass    # pylint: disable=unnecessary-pass

    mod.FakeMessage = FakeMessage  # type: ignore[attr-defined]
    mod.FakeProduct = FakeProduct  # type: ignore[attr-defined]
    return VersionInfo(
        release=release,
        namespace=namespace,
        module=mod,
        message_class=FakeMessage,
        product_class=FakeProduct,
    )


# ---------------------------------------------------------------------------
# available_releases / registrations existantes
# ---------------------------------------------------------------------------

class TestAvailableReleases:
    """
    Tests pour la fonction available_releases().
    Scénarios testés :
    - Vérification que la version 3.0 est bien enregistrée
    - Vérification que la fonction retourne une liste
    """
    def test_v3_0_is_registered(self):
        """Test que la version 3.0 est bien enregistrée dans le registre."""
        assert "3.0" in available_releases()

    def test_returns_list(self):
        """Test que available_releases() retourne une liste."""
        result = available_releases()
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# get()
# ---------------------------------------------------------------------------

class TestGet:
    """
    Tests pour la fonction get().
    Scénarios testés :
    - Récupération des métadonnées de la version 3.0 (release, namespace,
      classe message, classe produit)
    - Levée d'une KeyError pour une version inconnue
    - Vérification que le message d'erreur liste les versions disponibles
    """
    def test_get_v3_0(self):
        """Test que get("3.0") retourne le bon release string."""
        info = get("3.0")
        assert info.release == "3.0"

    def test_get_v3_0_namespace(self):
        """Test que le namespace de la version 3.0 est correct."""
        info = get("3.0")
        assert info.namespace == "http://www.editeur.org/onix/3.0/reference"

    def test_get_v3_0_has_message_class(self):
        """Test que la classe message de la version 3.0 est définie."""
        info = get("3.0")
        assert info.message_class is not None

    def test_get_v3_0_has_product_class(self):
        """Test que la classe produit de la version 3.0 est définie."""
        info = get("3.0")
        assert info.product_class is not None

    def test_get_unknown_version_raises_keyerror(self):
        """Test que get() lève KeyError pour une version inconnue."""
        with pytest.raises(KeyError, match="9.9"):
            get("9.9")

    def test_get_error_message_lists_available(self):
        """Test que le message d'erreur contient les versions disponibles."""
        with pytest.raises(KeyError) as exc_info:
            get("0.0")
        assert "3.0" in str(exc_info.value)


# ---------------------------------------------------------------------------
# register()
# ---------------------------------------------------------------------------

class TestRegister:
    """
    Tests pour la fonction register().
    Scénarios testés :
    - Enregistrement d'une nouvelle version et vérification qu'elle est accessible via get()
    - Écrasement d'une version existante et vérification de la nouvelle valeur
    """
    def test_register_new_version(self):
        """Test qu'une nouvelle version enregistrée est accessible via get()."""
        fake = _make_fake_version("99.0", "http://example.com/onix/99.0")
        register(fake)
        try:
            assert get("99.0").release == "99.0"
        finally:
            # Nettoyage pour ne pas polluer les autres tests
            _ver._REGISTRY.pop("99.0", None)    # pylint: disable=protected-access # type: ignore[attr-defined]

    def test_register_overwrites_existing(self):
        """Test que register() écrase silencieusement une version déjà enregistrée."""
        fake = _make_fake_version("3.0", "http://example.com/onix/99.0/override")
        original = _ver._REGISTRY.get("3.0")    # pylint: disable=protected-access # type: ignore[attr-defined]
        register(fake)
        try:
            assert get("3.0").namespace == "http://example.com/onix/99.0/override"
        finally:
            if original is not None:
                _ver._REGISTRY["3.0"] = original    # pylint: disable=protected-access # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# detect_release()
# ---------------------------------------------------------------------------

class TestDetectRelease:
    """
    Tests pour la fonction detect_release().
    Scénarios testés :
    - Détection correcte de la version 3.0 depuis son namespace exact
    - Retour None pour un namespace inconnu
    - Retour None pour une chaîne vide
    - Retour None pour un namespace partiel (pas de correspondance exacte)
    """
    def test_detect_v3_0_namespace(self):
        """Test que le namespace de la version 3.0 est correctement détecté."""
        ns = "http://www.editeur.org/onix/3.0/reference"
        assert detect_release(ns) == "3.0"

    def test_detect_unknown_namespace_returns_none(self):
        """Test que detect_release() retourne None pour un namespace inconnu."""
        assert detect_release("http://unknown.example.com/onix/0.0") is None

    def test_detect_empty_string_returns_none(self):
        """Test que detect_release() retourne None pour une chaîne vide."""
        assert detect_release("") is None

    def test_detect_partial_namespace_returns_none(self):
        """Test que la correspondance partielle de namespace retourne None."""
        # Correspondance partielle ne suffit pas
        assert detect_release("http://www.editeur.org/onix/3.0") is None
