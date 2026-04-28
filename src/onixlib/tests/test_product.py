"""Tests pour le facade Product (onixlib.models.product)."""

from __future__ import annotations

from xml.etree.ElementTree import fromstring

import pytest   # pyright: ignore[reportUnusedImport] # pylint: disable=unused-import

from onixlib.models.contributor import ContributorRole, Contributor
from onixlib.models.product import Product


# ---------------------------------------------------------------------------
# Product.new() — fabrique
# ---------------------------------------------------------------------------

class TestProductNew:
    """
    Tests pour la méthode de fabrique Product.new().
    Scénarios testés :
    - Création sans argument et vérification du type retourné
    - Définition de l'ISBN et du titre lors de la création
    - Valeurs par défaut : product_form "BC" et product_composition "00"
    - Levée d'une exception pour des codes product_form ou product_composition invalides
    """
    def test_returns_product_instance(self):
        """Test que Product.new() retourne une instance de Product."""
        p = Product.new()
        assert isinstance(p, Product)

    def test_isbn_set(self):
        """Test que l'ISBN est correctement défini lors de la création."""
        p = Product.new(isbn="9782070360024")
        assert p.isbn == "9782070360024"

    def test_isbn_none_by_default(self):
        """Test que l'ISBN est None par défaut."""
        p = Product.new()
        assert p.isbn is None

    def test_title_set(self):
        """Test que le titre est correctement défini lors de la création."""
        p = Product.new(title="Du côté de chez Swann")
        assert p.title == "Du côté de chez Swann"

    def test_title_empty_string_by_default(self):
        """Test que le titre est une chaîne vide par défaut."""
        p = Product.new()
        assert p.title == ""

    def test_isbn_and_title(self):
        """Test que l'ISBN et le titre sont correctement définis ensemble."""
        p = Product.new(isbn="9782070360024", title="Du côté de chez Swann")
        assert p.isbn == "9782070360024"
        assert p.title == "Du côté de chez Swann"

    def test_product_form_default_bc(self):
        """Test que product_form est "BC" (broché) par défaut."""
        p = Product.new()
        assert p.descriptive is not None
        assert p.descriptive.product_form == "BC"

    def test_product_form_custom(self):
        """Test que product_form peut être personnalisé (ex. "BB" pour relié)."""
        p = Product.new(product_form="BB")
        assert p.descriptive is not None
        assert p.descriptive.product_form == "BB"

    def test_product_composition_default_00(self):
        """Test que product_composition est "00" par défaut."""
        p = Product.new()
        assert p.descriptive is not None
        assert p.descriptive.product_composition == "00"

    def test_product_form_invalid_raises(self):
        """Test qu'un code product_form invalide lève une exception."""
        with pytest.raises(Exception):
            Product.new(product_form="INVALID_CODE")

    def test_product_composition_invalid_raises(self):
        """Test qu'un code product_composition invalide lève une exception."""
        with pytest.raises(Exception):
            Product.new(product_composition="INVALID")


# ---------------------------------------------------------------------------
# ISBN getter / setter
# ---------------------------------------------------------------------------

class TestProductIsbn:
    """
    Tests pour le getter et setter isbn.
    Scénarios testés :
    - Définition de l'ISBN et vérification de la valeur
    - Mise à jour d'un ISBN existant
    - Vérification que l'ISBN ne contient pas de tirets
    """
    def test_set_isbn(self):
        """Test de définition de l'ISBN sur un produit vide."""
        p = Product.new()
        p.isbn = "9782070360024"
        assert p.isbn == "9782070360024"

    def test_update_isbn(self):
        """Test de mise à jour d'un ISBN existant."""
        p = Product.new(isbn="9782070360024")
        p.isbn = "9782070413850"
        assert p.isbn == "9782070413850"

    def test_isbn_without_dashes(self):
        """Test que l'ISBN est stocké sans tirets."""
        p = Product.new(isbn="9782070360024")
        assert p.isbn is not None
        assert "-" not in p.isbn


# ---------------------------------------------------------------------------
# Title getter / setter
# ---------------------------------------------------------------------------

class TestProductTitle:
    """
    Tests pour le getter et setter title.
    Scénarios testés :
    - Définition du titre et vérification de la valeur
    - Mise à jour d'un titre existant
    - Titre contenant des caractères Unicode
    """
    def test_set_title(self):
        """Test de définition du titre sur un produit vide."""
        p = Product.new()
        p.title = "L'Étranger"
        assert p.title == "L'Étranger"

    def test_update_title(self):
        """Test de mise à jour d'un titre existant."""
        p = Product.new(title="Premier titre")
        p.title = "Deuxième titre"
        assert p.title == "Deuxième titre"

    def test_title_unicode(self):
        """Test de définition d'un titre avec des caractères Unicode."""
        p = Product.new()
        p.title = "À la recherche du temps perdu"
        assert p.title == "À la recherche du temps perdu"


# ---------------------------------------------------------------------------
# Contributeurs
# ---------------------------------------------------------------------------

class TestProductContributors:
    """
    Tests pour la gestion des contributeurs d'un produit.
    Scénarios testés :
    - Aucun contributeur par défaut
    - author est None par défaut
    - Ajout d'un contributeur avec rôle par défaut (A01) et rôle personnalisé
    - Vérification que author renvoie le premier contributeur A01
    - Vérification de la liste de contributeurs après plusieurs ajouts
    """
    def test_no_contributors_by_default(self):
        """Test que la liste de contributeurs est vide par défaut."""
        p = Product.new()
        assert not p.contributors

    def test_author_none_by_default(self):
        """Test que author est None par défaut."""
        p = Product.new()
        assert p.author is None

    def test_add_contributor_returns_contributor(self):
        """Test que add_contributor() retourne une instance de Contributor."""
        p = Product.new()
        c = p.add_contributor()
        assert isinstance(c, Contributor)

    def test_add_contributor_default_role_a01(self):
        """Test que le rôle par défaut d'un contributeur ajouté est A01."""
        p = Product.new()
        c = p.add_contributor()
        assert c.role == ContributorRole.A01

    def test_add_contributor_custom_role(self):
        """Test que add_contributor() accepte un rôle personnalisé."""
        p = Product.new()
        c = p.add_contributor(role=ContributorRole.B06)
        assert c.role == ContributorRole.B06

    def test_author_after_add_a01(self):
        """Test que author retourne bien le contributeur A01 après ajout."""
        p = Product.new()
        c = p.add_contributor(role=ContributorRole.A01)
        c.first_name = "Marcel"
        c.last_name = "PROUST"
        assert p.author is not None
        assert p.author.last_name == "PROUST"

    def test_contributors_list(self):
        """Test que la liste de contributeurs contient tous les contributeurs ajoutés."""
        p = Product.new()
        p.add_contributor(role=ContributorRole.A01)
        p.add_contributor(role=ContributorRole.B06)
        assert len(p.contributors) == 2


# ---------------------------------------------------------------------------
# Blocs optionnels
# ---------------------------------------------------------------------------

class TestProductBlocks:
    """
    Tests pour les blocs optionnels du produit.
    Scénarios testés :
    - descriptive est présent par défaut (créé par Product.new())
    - collateral, publishing, product_supply et related_material sont
      absents/vides par défaut
    """
    def test_descriptive_not_none(self):
        """Test que le bloc DescriptiveDetail est présent après Product.new()."""
        p = Product.new()
        assert p.descriptive is not None

    def test_collateral_none_by_default(self):
        """Test que le bloc CollateralDetail est None par défaut."""
        p = Product.new()
        assert p.collateral is None

    def test_publishing_none_by_default(self):
        """Test que le bloc PublishingDetail est None par défaut."""
        p = Product.new()
        assert p.publishing is None

    def test_product_supply_empty_by_default(self):
        """Test que la liste product_supply est vide par défaut."""
        p = Product.new()
        assert p.product_supply == []

    def test_related_material_none_by_default(self):
        """Test que le bloc RelatedMaterial est None par défaut."""
        p = Product.new()
        assert p.related_material is None


# ---------------------------------------------------------------------------
# to_xml() / repr
# ---------------------------------------------------------------------------

class TestProductSerialization:
    """
    Tests pour la sérialisation XML et le représentation textuelle du produit.
    Scénarios testés :
    - to_xml() retourne une chaîne de caractères
    - to_xml() contient l'ISBN et le titre
    - to_xml() produit un XML valide (parseable)
    - repr() contient l'ISBN
    - raw retourne l'objet xsdata sous-jacent
    """
    def test_to_xml_returns_string(self):
        """Test que to_xml() retourne une chaîne de caractères."""
        p = Product.new(isbn="9782070360024", title="Test")
        xml = p.to_xml()
        assert isinstance(xml, str)

    def test_to_xml_contains_isbn(self):
        """Test que to_xml() contient l'ISBN du produit."""
        p = Product.new(isbn="9782070360024", title="Test")
        xml = p.to_xml()
        assert "9782070360024" in xml

    def test_to_xml_contains_title(self):
        """Test que to_xml() contient le titre du produit."""
        p = Product.new(isbn="9782070360024", title="Du côté de chez Swann")
        xml = p.to_xml()
        assert "Du côté de chez Swann" in xml

    def test_to_xml_is_valid_xml(self):
        """Test que to_xml() produit un XML valide et parseable."""
        p = Product.new(isbn="9782070360024", title="Test")
        xml = p.to_xml()
        # Ne lève pas d'exception si c'est du XML valide
        fromstring(xml)

    def test_repr(self):
        """Test que repr() contient l'ISBN du produit."""
        p = Product.new(isbn="9782070360024", title="Test")
        r = repr(p)
        assert "9782070360024" in r

    def test_raw_property(self):
        """Test que raw retourne l'objet xsdata sous-jacent."""
        p = Product.new()
        assert p.raw is not None
