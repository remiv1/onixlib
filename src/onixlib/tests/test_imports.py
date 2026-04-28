"""Tests des imports publics et de l'API de surface de onixlib."""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Imports depuis le package public
# ---------------------------------------------------------------------------

class TestPublicImports:
    """
    Tests des imports depuis le package public onixlib.
    Scénarios testés :
    - Importabilité de toutes les classes et fonctions exposées publiquement
    - Vérification que chaque symbole importé est non-None et/ou callable
    """
    def test_import_parse(self):
        """Test que parse est importable et callable depuis onixlib."""
        from onixlib import parse   # pylint: disable=import-outside-toplevel
        assert callable(parse)

    def test_import_notice(self):
        """Test que Notice est importable depuis onixlib."""
        from onixlib import Notice   # pylint: disable=import-outside-toplevel
        assert Notice is not None

    def test_import_product(self):
        """Test que Product est importable depuis onixlib."""
        from onixlib import Product   # pylint: disable=import-outside-toplevel
        assert Product is not None

    def test_import_contributor(self):
        """Test que Contributor est importable depuis onixlib."""
        from onixlib import Contributor   # pylint: disable=import-outside-toplevel
        assert Contributor is not None

    def test_import_contributor_role(self):
        """Test que ContributorRole est importable depuis onixlib."""
        from onixlib import ContributorRole   # pylint: disable=import-outside-toplevel
        assert ContributorRole is not None

    def test_import_header(self):
        """Test que Header est importable depuis onixlib."""
        from onixlib import Header   # pylint: disable=import-outside-toplevel
        assert Header is not None

    def test_import_collateral_detail(self):
        """Test que CollateralDetail est importable depuis onixlib."""
        from onixlib import CollateralDetail   # pylint: disable=import-outside-toplevel
        assert CollateralDetail is not None

    def test_import_descriptive_detail(self):
        """Test que DescriptiveDetail est importable depuis onixlib."""
        from onixlib import DescriptiveDetail   # pylint: disable=import-outside-toplevel
        assert DescriptiveDetail is not None

    def test_import_product_supply(self):
        """Test que ProductSupply est importable depuis onixlib."""
        from onixlib import ProductSupply   # pylint: disable=import-outside-toplevel
        assert ProductSupply is not None

    def test_import_price(self):
        """Test que Price est importable depuis onixlib."""
        from onixlib import Price   # pylint: disable=import-outside-toplevel
        assert Price is not None

    def test_import_supply_detail(self):
        """Test que SupplyDetail est importable depuis onixlib."""
        from onixlib import SupplyDetail   # pylint: disable=import-outside-toplevel
        assert SupplyDetail is not None

    def test_import_publishing_detail(self):
        """Test que PublishingDetail est importable depuis onixlib."""
        from onixlib import PublishingDetail   # pylint: disable=import-outside-toplevel
        assert PublishingDetail is not None

    def test_import_related_material(self):
        """Test que RelatedMaterial est importable depuis onixlib."""
        from onixlib import RelatedMaterial   # pylint: disable=import-outside-toplevel
        assert RelatedMaterial is not None

    def test_import_related_product(self):
        """Test que RelatedProduct est importable depuis onixlib."""
        from onixlib import RelatedProduct   # pylint: disable=import-outside-toplevel
        assert RelatedProduct is not None

    def test_import_related_work(self):
        """Test que RelatedWork est importable depuis onixlib."""
        from onixlib import RelatedWork   # pylint: disable=import-outside-toplevel
        assert RelatedWork is not None

    def test_import_version_info(self):
        """Test que VersionInfo est importable depuis onixlib."""
        from onixlib import VersionInfo   # pylint: disable=import-outside-toplevel
        assert VersionInfo is not None

    def test_import_available_releases(self):
        """Test que available_releases est importable et callable depuis onixlib."""
        from onixlib import available_releases   # pylint: disable=import-outside-toplevel
        assert callable(available_releases)

    def test_import_register(self):
        """Test que register est importable et callable depuis onixlib."""
        from onixlib import register   # pylint: disable=import-outside-toplevel
        assert callable(register)

    def test_import_book(self):
        """Test que Book (alias de rétro-compatibilité) est importable depuis onixlib."""
        # Alias de rétro-compatibilité
        from onixlib import Book   # pylint: disable=import-outside-toplevel
        assert Book is not None


# ---------------------------------------------------------------------------
# Imports internes (modules individuels)
# ---------------------------------------------------------------------------

class TestInternalImports:
    """
    Tests des imports internes (modules individuels) de onixlib.
    Scénarios testés :
    - Importabilité de chaque module interne
    - Présence des attributs principaux dans chaque module
    """
    def test_models_versions(self):
        """Test que onixlib.models.versions est importable et possède register."""
        import onixlib.models.versions   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.versions, "register")

    def test_models_notice(self):
        """Test que onixlib.models.notice est importable et possède Notice."""
        import onixlib.models.notice   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.notice, "Notice")

    def test_models_product(self):
        """Test que onixlib.models.product est importable et possède Product."""
        import onixlib.models.product   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.product, "Product")

    def test_models_header(self):
        """Test que onixlib.models.header est importable et possède Header."""
        import onixlib.models.header   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.header, "Header")

    def test_models_contributor(self):
        """Test que onixlib.models.contributor est importable et possède Contributor."""
        import onixlib.models.contributor   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.contributor, "Contributor")

    def test_models_descriptive(self):
        """Test que onixlib.models.descriptive est importable et possède DescriptiveDetail."""
        import onixlib.models.descriptive   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.descriptive, "DescriptiveDetail")

    def test_models_collateral(self):
        """Test que onixlib.models.collateral est importable et possède CollateralDetail."""
        import onixlib.models.collateral   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.collateral, "CollateralDetail")

    def test_models_publishing(self):
        """Test que onixlib.models.publishing est importable et possède PublishingDetail."""
        import onixlib.models.publishing   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.publishing, "PublishingDetail")

    def test_models_product_supply(self):
        """Test que onixlib.models.product_supply est importable et possède ProductSupply."""
        import onixlib.models.product_supply   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.product_supply, "ProductSupply")

    def test_models_related_material(self):
        """Test que onixlib.models.related_material est importable et possède RelatedMaterial."""
        import onixlib.models.related_material   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.related_material, "RelatedMaterial")

    def test_models_generated_v3_0(self):
        """Test que onixlib.models.generated.v3_0 est importable et possède Onixmessage."""
        import onixlib.models.generated.v3_0   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.generated.v3_0, "Onixmessage")

    def test_models_generated_v3_0_product(self):
        """Test que onixlib.models.generated.v3_0 possède la classe Product."""
        import onixlib.models.generated.v3_0   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib.models.generated.v3_0, "Product")


# ---------------------------------------------------------------------------
# __all__ du package public
# ---------------------------------------------------------------------------

class TestAllExports:
    """
    Tests pour l'attribut __all__ du package public onixlib.
    Scénarios testés :
    - __all__ est défini dans le package
    - Les symboles principaux (parse, Notice, Product, ContributorRole) y figurent
    """
    def test_all_is_defined(self):
        """Test que __all__ est défini dans le package onixlib."""
        import onixlib   # pylint: disable=import-outside-toplevel
        assert hasattr(onixlib, "__all__")

    def test_all_contains_parse(self):
        """Test que "parse" figure dans __all__."""
        import onixlib   # pylint: disable=import-outside-toplevel
        assert "parse" in onixlib.__all__

    def test_all_contains_notice(self):
        """Test que "Notice" figure dans __all__."""
        import onixlib   # pylint: disable=import-outside-toplevel
        assert "Notice" in onixlib.__all__

    def test_all_contains_product(self):
        """Test que "Product" figure dans __all__."""
        import onixlib   # pylint: disable=import-outside-toplevel
        assert "Product" in onixlib.__all__

    def test_all_contains_contributor_role(self):
        """Test que "ContributorRole" figure dans __all__."""
        import onixlib   # pylint: disable=import-outside-toplevel
        assert "ContributorRole" in onixlib.__all__
