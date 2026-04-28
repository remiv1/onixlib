"""Tests pour le facade Notice et la fonction parse (onixlib.models.notice)."""

from __future__ import annotations

import io
from pathlib import Path
from xml.etree.ElementTree import fromstring

import pytest   # pyright: ignore[reportUnusedImport] # pylint: disable=unused-import

from onixlib.models.notice import Notice, parse
from onixlib.models.product import Product

# Chemin vers les fixtures XML
FIXTURES_DIR = Path(__file__).parent / "fixtures"
NOTICE_V3_0 = FIXTURES_DIR / "notice_v3_0.xml"
NOTICE_EMPTY = FIXTURES_DIR / "notice_empty.xml"


# ---------------------------------------------------------------------------
# Notice.new()
# ---------------------------------------------------------------------------

class TestNoticeNew:
    """
    Tests pour la méthode de fabrique Notice.new().
    Scénarios testés :
    - Création d'une notice et vérification du type retourné
    - Vérification des valeurs sender_name et sent_datetime
    - Aucun produit par défaut
    - Levée d'une KeyError pour une release invalide
    - Vérification du représentation textuelle
    """
    def test_returns_notice_instance(self):
        """Test que Notice.new() retourne une instance de Notice."""
        n = Notice.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        assert isinstance(n, Notice)

    def test_sender_name(self):
        """Test que sender_name est correctement défini dans le header."""
        n = Notice.new(sender_name="DILICOM", sent_datetime="20260428T120000Z")
        assert n.header.sender_name == "DILICOM"

    def test_sent_datetime(self):
        """Test que sent_datetime est correctement défini dans le header."""
        n = Notice.new(sender_name="TEST", sent_datetime="20260101T000000Z")
        assert n.header.sent_datetime == "20260101T000000Z"

    def test_no_products_by_default(self):
        """Test que la liste de produits est vide par défaut."""
        n = Notice.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        assert n.products == []

    def test_invalid_version_raises_keyerror(self):
        """Test que Notice.new() lève KeyError pour une release invalide."""
        with pytest.raises(KeyError):
            Notice.new(sender_name="TEST", sent_datetime="20260428T120000Z", release="9.9")

    def test_repr(self):
        """Test que repr() contient le nom de l'expéditeur."""
        n = Notice.new(sender_name="DILICOM", sent_datetime="20260428T120000Z")
        r = repr(n)
        assert "DILICOM" in r


# ---------------------------------------------------------------------------
# Notice.parse_full() — depuis un chemin
# ---------------------------------------------------------------------------

class TestNoticeParseFullFromPath:
    """
    Tests pour Notice.parse_full() depuis un chemin de fichier.
    Scénarios testés :
    - Chargement depuis un objet Path, une chaîne str et un fichier vide
    - Vérification du sender_name, du nombre de produits, de l'ISBN et du titre
    """
    def test_returns_notice_instance(self):
        """Test que parse_full() retourne une instance de Notice."""
        n = Notice.parse_full(NOTICE_V3_0)
        assert isinstance(n, Notice)

    def test_sender_name(self):
        """Test que le sender_name est correctement lu depuis le fichier XML."""
        n = Notice.parse_full(NOTICE_V3_0)
        assert n.header.sender_name == "EDITIONS EXEMPLE"

    def test_two_products(self):
        """Test que la notice contient bien 2 produits."""
        n = Notice.parse_full(NOTICE_V3_0)
        assert len(n.products) == 2

    def test_first_product_isbn(self):
        """Test que l'ISBN du premier produit est correct."""
        n = Notice.parse_full(NOTICE_V3_0)
        assert n.products[0].isbn == "9782070360024"

    def test_first_product_title(self):
        """Test que le titre du premier produit est correct."""
        n = Notice.parse_full(NOTICE_V3_0)
        assert n.products[0].title == "Du côté de chez Swann"

    def test_empty_notice_has_no_products(self):
        """Test qu'une notice vide ne contient aucun produit."""
        n = Notice.parse_full(NOTICE_EMPTY)
        assert n.products == []

    def test_path_object(self):
        """Test que parse_full() accepte un objet Path."""
        n = Notice.parse_full(Path(NOTICE_V3_0))
        assert len(n.products) == 2

    def test_string_path(self):
        """Test que parse_full() accepte une chaîne de caractères comme chemin."""
        n = Notice.parse_full(str(NOTICE_V3_0))
        assert len(n.products) == 2


# ---------------------------------------------------------------------------
# Notice.parse_full() — depuis un fichier-objet en mémoire
# ---------------------------------------------------------------------------

class TestNoticeParseFullFromFileObject:
    """
    Tests pour Notice.parse_full() depuis un objet fichier en mémoire.
    Scénarios testés :
    - Chargement depuis un fichier binaire ouvert (BinaryIO)
    - Chargement depuis un BytesIO
    """
    def test_from_binary_io(self):
        """Test que parse_full() accepte un fichier binaire ouvert."""
        with open(NOTICE_V3_0, "rb") as fh:
            n = Notice.parse_full(fh)
        assert len(n.products) == 2

    def test_from_bytes_io(self):
        """Test que parse_full() accepte un BytesIO."""
        xml_bytes = NOTICE_V3_0.read_bytes()
        n = Notice.parse_full(io.BytesIO(xml_bytes))
        assert len(n.products) == 2


# ---------------------------------------------------------------------------
# Notice.add_product()
# ---------------------------------------------------------------------------

class TestNoticeAddProduct:
    """
    Tests pour la méthode Notice.add_product().
    Scénarios testés :
    - Ajout d'un produit et vérification du nombre de produits
    - Vérification que l'ISBN du produit ajouté est accessible
    - Ajout de plusieurs produits et vérification du compte total
    """
    def test_add_one_product(self):
        """Test qu'un produit ajouté est bien présent dans la liste."""
        n = Notice.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        p = Product.new(isbn="9782070360024", title="Test")
        n.add_product(p)
        assert len(n.products) == 1

    def test_add_product_isbn_accessible(self):
        """Test que l'ISBN du produit ajouté est accessible via la notice."""
        n = Notice.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        p = Product.new(isbn="9782070360024", title="Test")
        n.add_product(p)
        assert n.products[0].isbn == "9782070360024"

    def test_add_multiple_products(self):
        """Test que plusieurs produits ajoutés sont tous présents."""
        n = Notice.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        for isbn in ("9782070360024", "9782070413850", "9782070408504"):
            n.add_product(Product.new(isbn=isbn))
        assert len(n.products) == 3


# ---------------------------------------------------------------------------
# Notice.to_xml()
# ---------------------------------------------------------------------------

class TestNoticeToXml:
    """
    Tests pour la sérialisation Notice.to_xml().
    Scénarios testés :
    - to_xml() retourne une chaîne de caractères
    - to_xml() contient le sender_name et l'ISBN d'un produit ajouté
    - to_xml() produit un XML valide
    - Round-trip : sérialisation puis re-parse de la notice
    """
    def test_to_xml_returns_string(self):
        """Test que to_xml() retourne une chaîne de caractères."""
        n = Notice.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        xml = n.to_xml()
        assert isinstance(xml, str)

    def test_to_xml_contains_sender_name(self):
        """Test que to_xml() contient le sender_name."""
        n = Notice.new(sender_name="DILICOM", sent_datetime="20260428T120000Z")
        xml = n.to_xml()
        assert "DILICOM" in xml

    def test_to_xml_is_valid_xml(self):
        """Test que to_xml() produit un XML valide et parseable."""
        n = Notice.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        xml = n.to_xml()
        fromstring(xml)

    def test_to_xml_contains_product_isbn(self):
        """Test que to_xml() contient l'ISBN d'un produit ajouté."""
        n = Notice.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        n.add_product(Product.new(isbn="9782070360024", title="Test"))
        xml = n.to_xml()
        assert "9782070360024" in xml

    def test_roundtrip(self):
        """Sérialise puis re-parse la notice et vérifie la cohérence."""
        n = Notice.new(sender_name="ROUNDTRIP", sent_datetime="20260428T120000Z")
        n.add_product(Product.new(isbn="9782070360024", title="Test roundtrip"))
        xml_bytes = n.to_xml().encode("utf-8")
        n2 = Notice.parse_full(io.BytesIO(xml_bytes))
        assert n2.header.sender_name == "ROUNDTRIP"
        assert len(n2.products) == 1
        assert n2.products[0].isbn == "9782070360024"


# ---------------------------------------------------------------------------
# parse() streaming — depuis un chemin
# ---------------------------------------------------------------------------

class TestParseStreamingFromPath:
    """
    Tests pour la fonction parse() en mode streaming depuis un chemin de fichier.
    Scénarios testés :
    - Émission de produits depuis une notice avec plusieurs produits
    - Chaque élément émis est une instance de Product
    - Vérification des ISBN du premier et deuxième produit
    - Fichier vide n'émet aucun produit
    - Acceptation d'un objet Path, d'une chaîne str
    - Levée d'une exception pour un fichier inexistant
    """
    def test_yields_products(self):
        """Test que parse() émet bien des produits depuis la notice."""
        products = list(parse(NOTICE_V3_0))
        assert len(products) == 2

    def test_yields_product_instances(self):
        """Test que chaque élément émis est une instance de Product."""
        for p in parse(NOTICE_V3_0):
            assert isinstance(p, Product)

    def test_first_product_isbn(self):
        """Test que l'ISBN du premier produit émis est correct."""
        products = list(parse(NOTICE_V3_0))
        assert products[0].isbn == "9782070360024"

    def test_second_product_isbn(self):
        """Test que l'ISBN du deuxième produit émis est correct."""
        products = list(parse(NOTICE_V3_0))
        assert products[1].isbn == "9782070413850"

    def test_empty_file_yields_nothing(self):
        """Test qu'une notice sans produits n'émet aucun élément."""
        products = list(parse(NOTICE_EMPTY))
        assert not products

    def test_path_object(self):
        """Test que parse() accepte un objet Path."""
        products = list(parse(Path(NOTICE_V3_0)))
        assert len(products) == 2

    def test_string_path(self):
        """Test que parse() accepte une chaîne de caractères comme chemin."""
        products = list(parse(str(NOTICE_V3_0)))
        assert len(products) == 2

    def test_nonexistent_file_raises(self):
        """Test que parse() lève une exception pour un fichier inexistant."""
        with pytest.raises(Exception):
            list(parse("/tmp/fichier_qui_nexiste_pas.xml"))


# ---------------------------------------------------------------------------
# parse() streaming — depuis un fichier-objet en mémoire
# ---------------------------------------------------------------------------

class TestParseStreamingFromFileObject:
    """
    Tests pour la fonction parse() en mode streaming depuis un objet fichier.
    Scénarios testés :
    - Chargement depuis un fichier binaire ouvert (BinaryIO)
    - Chargement depuis un BytesIO
    """
    def test_from_binary_io(self):
        """Test que parse() accepte un fichier binaire ouvert."""
        with open(NOTICE_V3_0, "rb") as fh:
            products = list(parse(fh))
        assert len(products) == 2

    def test_from_bytes_io(self):
        """Test que parse() accepte un BytesIO."""
        xml_bytes = NOTICE_V3_0.read_bytes()
        products = list(parse(io.BytesIO(xml_bytes)))
        assert len(products) == 2


# ---------------------------------------------------------------------------
# parse() — version explicite
# ---------------------------------------------------------------------------

class TestParseWithExplicitVersion:
    """
    Tests pour la fonction parse() avec une version ONIX explicite.
    Scénarios testés :
    - Parse réussi avec la version 3.0 forcée
    - Levée d'une KeyError pour une version inconnue
    """
    def test_explicit_v3_0(self):
        """Test que parse() fonctionne correctement avec version="3.0" forcée."""
        products = list(parse(NOTICE_V3_0, version="3.0"))
        assert len(products) == 2

    def test_explicit_unknown_version_raises_keyerror(self):
        """Test que parse() lève KeyError pour une version inconnue."""
        with pytest.raises(KeyError):
            list(parse(NOTICE_V3_0, version="9.9"))


# ---------------------------------------------------------------------------
# Données du premier produit (notice_v3_0.xml)
# ---------------------------------------------------------------------------

class TestNoticeProductData:
    """
    Tests de vérification des données extraites du fichier notice_v3_0.xml.
    Scénarios testés :
    - Premier produit : auteur, prénom, nom de famille
    - Premier produit : description dans CollateralDetail
    - Premier produit : statut et date de publication dans PublishingDetail
    - Premier produit : prix et devise dans ProductSupply
    - Deuxième produit : absence de CollateralDetail et product_form "BB"
    """
    @pytest.fixture(scope="class")
    def products(self):
        """Fixture retournant la liste des produits du fichier notice_v3_0.xml."""
        return list(parse(NOTICE_V3_0))

    def test_first_product_has_author(self, products: list[Product]):
        """Test que le premier produit possède un auteur."""
        assert products[0].author is not None

    def test_first_product_author_last_name(self, products: list[Product]):
        """Test que le nom de l'auteur du premier produit est correct."""
        assert products[0].author is not None
        assert products[0].author.last_name == "PROUST"

    def test_first_product_author_first_name(self, products: list[Product]):
        """Test que le prénom de l'auteur du premier produit est correct."""
        assert products[0].author is not None
        assert products[0].author.first_name == "Marcel"

    def test_first_product_collateral_description(self, products: list[Product]):
        """Test que la description du premier produit est présente et non vide."""
        assert products[0].collateral is not None
        desc = products[0].collateral.description
        assert desc is not None
        assert len(desc) > 0

    def test_first_product_publishing_status(self, products: list[Product]):
        """Test que le statut de publication du premier produit est "04" (actif)."""
        assert products[0].publishing is not None
        assert products[0].publishing.publishing_status == "04"

    def test_first_product_publication_date(self, products: list[Product]):
        """Test que la date de publication du premier produit est correcte."""
        assert products[0].publishing is not None
        assert products[0].publishing.publication_date == "19130114"

    def test_first_product_price(self, products: list[Product]):
        """Test que le prix du premier produit est 12,50 EUR."""
        ps_list = products[0].product_supply
        assert len(ps_list) == 1
        prices = ps_list[0].prices
        assert len(prices) == 1
        assert str(prices[0].amount) == "12.50"
        assert prices[0].currency == "EUR"

    def test_second_product_no_collateral(self, products: list[Product]):
        """Test que le deuxième produit n'a pas de CollateralDetail."""
        assert products[1].collateral is None

    def test_second_product_form_bb(self, products: list[Product]):
        """Test que le product_form du deuxième produit est "BB" (relié)."""
        assert products[1].descriptive is not None
        assert products[1].descriptive.product_form == "BB"


# ---------------------------------------------------------------------------
# Création complète d'un fichier ONIX et vérification de l'intégrité
# ---------------------------------------------------------------------------

class TestOnixFileCreation:
    """
    Tests de création d'un fichier ONIX complet à partir d'un objet Notice
    entièrement peuplé, puis vérification de la lisibilité et de l'intégrité.
    Scénarios testés :
    - Sérialisation vers un fichier temporaire sur disque (tmp_path)
    - Le fichier créé existe et n'est pas vide
    - Le XML produit est valide et parseable
    - La structure ONIX de base est présente (<ONIXMessage>, <Header>, <Product>)
    - Après re-parsing, toutes les données sont préservées :
      sender_name, nombre de produits, ISBN, titre, auteur,
      description CollateralDetail, statut de publication et prix
    """

    @pytest.fixture(scope="class")
    def tmp_onix_path(self, tmp_path_factory: pytest.TempPathFactory) -> Path:
        """Fixture qui sérialise notice_v3_0.xml vers un fichier temporaire."""
        n = Notice.parse_full(NOTICE_V3_0)
        xml_str = n.to_xml()
        path = tmp_path_factory.mktemp("onix") / "notice_output.xml"
        path.write_text(xml_str, encoding="utf-8")
        return path

    def test_file_is_created(self, tmp_onix_path: Path):
        """Test que le fichier ONIX est bien créé sur disque."""
        assert tmp_onix_path.exists()

    def test_file_is_not_empty(self, tmp_onix_path: Path):
        """Test que le fichier ONIX créé n'est pas vide."""
        assert tmp_onix_path.stat().st_size > 0

    def test_file_is_valid_xml(self, tmp_onix_path: Path):
        """Test que le fichier ONIX produit est un XML valide et parseable."""
        fromstring(tmp_onix_path.read_text(encoding="utf-8"))

    def test_file_contains_onixmessage_root(self, tmp_onix_path: Path):
        """Test que le XML contient l'élément racine ONIXMessage."""
        content = tmp_onix_path.read_text(encoding="utf-8")
        assert "ONIXMessage" in content

    def test_file_contains_header_element(self, tmp_onix_path: Path):
        """Test que le XML contient un bloc Header."""
        content = tmp_onix_path.read_text(encoding="utf-8")
        assert "Header" in content and "SenderName" in content

    def test_file_contains_product_element(self, tmp_onix_path: Path):
        """Test que le XML contient au moins un bloc Product."""
        root = fromstring(tmp_onix_path.read_text(encoding="utf-8"))
        ns = {"onix": "http://www.editeur.org/onix/3.0/reference"}
        assert root.find("onix:Product", ns) is not None

    def test_file_contains_first_isbn(self, tmp_onix_path: Path):
        """Test que le XML contient l'ISBN du premier produit."""
        content = tmp_onix_path.read_text(encoding="utf-8")
        assert "9782070360024" in content

    def test_file_contains_second_isbn(self, tmp_onix_path: Path):
        """Test que le XML contient l'ISBN du second produit."""
        content = tmp_onix_path.read_text(encoding="utf-8")
        assert "9782070413850" in content

    def test_reparsed_sender_name(self, tmp_onix_path: Path):
        """Test que le sender_name est préservé après re-parsing du fichier."""
        n2 = Notice.parse_full(tmp_onix_path)
        assert n2.header.sender_name == "EDITIONS EXEMPLE"

    def test_reparsed_product_count(self, tmp_onix_path: Path):
        """Test que le nombre de produits est préservé après re-parsing."""
        n2 = Notice.parse_full(tmp_onix_path)
        assert len(n2.products) == 2

    def test_reparsed_first_isbn(self, tmp_onix_path: Path):
        """Test que l'ISBN du premier produit est préservé après re-parsing."""
        products = list(parse(tmp_onix_path))
        assert products[0].isbn == "9782070360024"

    def test_reparsed_first_title(self, tmp_onix_path: Path):
        """Test que le titre du premier produit est préservé après re-parsing."""
        products = list(parse(tmp_onix_path))
        assert products[0].title == "Du côté de chez Swann"

    def test_reparsed_author(self, tmp_onix_path: Path):
        """Test que l'auteur du premier produit est préservé après re-parsing."""
        products = list(parse(tmp_onix_path))
        assert products[0].author is not None
        assert products[0].author.last_name == "PROUST"
        assert products[0].author.first_name == "Marcel"

    def test_reparsed_collateral_description(self, tmp_onix_path: Path):
        """Test que la description CollateralDetail est préservée après re-parsing."""
        products = list(parse(tmp_onix_path))
        assert products[0].collateral is not None
        assert products[0].collateral.description is not None
        assert len(products[0].collateral.description) > 0

    def test_reparsed_publishing_status(self, tmp_onix_path: Path):
        """Test que le statut de publication est préservé après re-parsing."""
        products = list(parse(tmp_onix_path))
        assert products[0].publishing is not None
        assert products[0].publishing.publishing_status == "04"

    def test_reparsed_publication_date(self, tmp_onix_path: Path):
        """Test que la date de publication est préservée après re-parsing."""
        products = list(parse(tmp_onix_path))
        assert products[0].publishing is not None
        assert products[0].publishing.publication_date == "19130114"

    def test_reparsed_price(self, tmp_onix_path: Path):
        """Test que le prix et la devise sont préservés après re-parsing."""
        products = list(parse(tmp_onix_path))
        ps_list = products[0].product_supply
        assert len(ps_list) == 1
        prices = ps_list[0].prices
        assert len(prices) == 1
        assert str(prices[0].amount) == "12.50"
        assert prices[0].currency == "EUR"
