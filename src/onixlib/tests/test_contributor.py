"""Tests pour le facade Contributor (onixlib.models.contributor)."""

from __future__ import annotations

import pytest   # pyright: ignore[reportUnusedImport] # pylint: disable=unused-import

from onixlib.models.contributor import Contributor, ContributorRole


# ---------------------------------------------------------------------------
# Création
# ---------------------------------------------------------------------------

class TestContributorCreation:
    """
    Tests pour la création d'un contributeur et les valeurs par défaut.

    Scénarios testés :
    - Création d'un contributeur vide
    - Valeurs par défaut des champs first_name, last_name, full_name et role
    """
    def test_create_empty(self):
        """Test de création d'un contributeur sans arguments."""
        c = Contributor()
        assert isinstance(c, Contributor)

    def test_first_name_empty_by_default(self):
        """Test que le prénom est une chaîne vide par défaut."""
        c = Contributor()
        assert c.first_name == ""

    def test_last_name_empty_by_default(self):
        """Test que le nom de famille est une chaîne vide par défaut."""
        c = Contributor()
        assert c.last_name == ""

    def test_full_name_empty_by_default(self):
        """Test que le nom complet est une chaîne vide par défaut."""
        c = Contributor()
        assert c.full_name == ""

    def test_role_none_by_default(self):
        """Test que le rôle est None par défaut."""
        c = Contributor()
        assert c.role is None


# ---------------------------------------------------------------------------
# Setters prénom / nom
# ---------------------------------------------------------------------------

class TestContributorNames:
    """Tests pour les setters de prénom, nom et full_name.
    Scénarios testés :
    - Définition du prénom et vérification du champ first_name
    - Définition du nom de famille et vérification du champ last_name
    - Vérification que full_name combine first_name et last_name
    - Vérification que full_name affiche uniquement last_name si first_name est vide
    - Vérification que full_name affiche uniquement first_name si last_name est vide
    - Mise à jour du prénom et vérification de la nouvelle valeur
    - Mise à jour du nom de famille et vérification de la nouvelle valeur
    - Test de noms avec caractères Unicode
    """
    def test_set_first_name(self):
        """Test de définition du prénom."""
        c = Contributor()
        c.first_name = "Marcel"
        assert c.first_name == "Marcel"

    def test_set_last_name(self):
        """Test de définition du nom de famille."""
        c = Contributor()
        c.last_name = "PROUST"
        assert c.last_name == "PROUST"

    def test_full_name_combines(self):
        """Test que full_name combine first_name et last_name."""
        c = Contributor()
        c.first_name = "Marcel"
        c.last_name = "PROUST"
        assert c.full_name == "Marcel PROUST"

    def test_full_name_only_last(self):
        """Test que full_name affiche uniquement last_name si first_name est vide."""
        c = Contributor()
        c.last_name = "PROUST"
        assert c.full_name == "PROUST"

    def test_full_name_only_first(self):
        """Test que full_name affiche uniquement first_name si last_name est vide."""
        c = Contributor()
        c.first_name = "Marcel"
        assert c.full_name == "Marcel"

    def test_update_first_name(self):
        """Test de mise à jour du prénom."""
        c = Contributor()
        c.first_name = "Jean"
        c.first_name = "Marcel"
        assert c.first_name == "Marcel"

    def test_update_last_name(self):
        """Test de mise à jour du nom de famille."""
        c = Contributor()
        c.last_name = "DUPONT"
        c.last_name = "PROUST"
        assert c.last_name == "PROUST"

    def test_unicode_names(self):
        """Test de noms avec caractères Unicode."""
        c = Contributor()
        c.first_name = "André"
        c.last_name = "GÏDE"
        assert c.full_name == "André GÏDE"


# ---------------------------------------------------------------------------
# Rôle
# ---------------------------------------------------------------------------

class TestContributorRole:
    """Tests pour le setter de rôle du contributeur.
    Scénarios testés :
    - Définition du rôle A01 et vérification de sa valeur
    - Définition du rôle B06 et vérification de sa valeur
    - Mise à jour du rôle et vérification de la nouvelle valeur
    - Vérification que le rôle est stocké en tant que string dans l'instance
    """
    def test_set_role_a01(self):
        """Test de définition du rôle A01."""
        c = Contributor()
        c.role = ContributorRole.A01
        assert c.role == ContributorRole.A01

    def test_set_role_b06(self):
        """Test de définition du rôle B06."""
        c = Contributor()
        c.role = ContributorRole.B06
        assert c.role == ContributorRole.B06

    def test_update_role(self):
        """Test de mise à jour du rôle."""
        c = Contributor()
        c.role = ContributorRole.A01
        c.role = ContributorRole.B06
        assert c.role == ContributorRole.B06

    def test_role_value_string(self):
        """Test que le rôle est stocké en tant que string dans l'instance."""
        c = Contributor()
        c.role = ContributorRole.A01
        assert c.role is not None
        assert c.role.value == "A01"    # type: ignore[attr-defined]
