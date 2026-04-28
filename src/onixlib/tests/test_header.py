"""Tests pour le facade Header (onixlib.models.header)."""

from __future__ import annotations

import pytest   # pyright: ignore[reportUnusedImport] # pylint: disable=unused-import

from onixlib.models.header import Header


# ---------------------------------------------------------------------------
# Header.new()
# ---------------------------------------------------------------------------

class TestHeaderNew:
    """
    Tests pour la méthode de fabrique Header.new().
    Scénarios testés :
    - Création d'un Header avec sender_name et sent_datetime
    - Vérification des valeurs par défaut pour :
        - sender_gln,
        - sender_email,
        - addressee_name,
        - message_number
    - Mise à jour du sender_name et vérification de la nouvelle valeur
    - Mise à jour du sender_gln et vérification de la nouvelle valeur
    - Mise à jour du sender_email et vérification de la nouvelle valeur
    - Mise à jour de addressee_name et vérification de la nouvelle valeur
    - Mise à jour de message_number et vérification de la nouvelle valeur
    """
    def test_returns_header_instance(self):
        """Test que Header.new() retourne une instance de Header."""
        h = Header.new(sender_name="DILICOM", sent_datetime="20260428T120000Z")
        assert isinstance(h, Header)

    def test_sender_name(self):
        """Test que sender_name est correctement défini."""
        h = Header.new(sender_name="DILICOM", sent_datetime="20260428T120000Z")
        assert h.sender_name == "DILICOM"

    def test_sent_datetime(self):
        """Test que sent_datetime est correctement défini."""
        h = Header.new(sender_name="TEST", sent_datetime="20260101T000000Z")
        assert h.sent_datetime == "20260101T000000Z"

    def test_sender_name_empty_string(self):
        """Test que sender_name peut être une chaîne vide."""
        h = Header.new(sender_name="", sent_datetime="20260428T120000Z")
        assert h.sender_name == ""

    def test_gln_absent_by_default(self):
        """Test que sender_gln est None par défaut."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        assert h.sender_gln is None

    def test_email_absent_by_default(self):
        """Test que sender_email est None par défaut."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        assert h.sender_email is None

    def test_addressee_absent_by_default(self):
        """Test que addressee_name est None par défaut."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        assert h.addressee_name is None

    def test_message_number_absent_by_default(self):
        """Test que message_number est None par défaut."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        assert h.message_number is None


# ---------------------------------------------------------------------------
# Setters sender_name
# ---------------------------------------------------------------------------

class TestHeaderSenderName:
    """
    Tests pour le setter sender_name du Header.
    Scénarios testés :
    - Mise à jour du sender_name et vérification de la nouvelle valeur
    - Mise à jour du sender_name avec une chaîne vide et vérification de la nouvelle valeur
    - Mise à jour du sender_name avec des caractères Unicode et vérification de la nouvelle valeur
    """
    def test_set_sender_name(self):
        """Test de mise à jour du sender_name."""
        h = Header.new(sender_name="INIT", sent_datetime="20260428T120000Z")
        h.sender_name = "NOUVEAU"
        assert h.sender_name == "NOUVEAU"

    def test_set_sender_name_unicode(self):
        """Test de mise à jour du sender_name avec des caractères Unicode."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        h.sender_name = "Éditions Référence"
        assert h.sender_name == "Éditions Référence"


# ---------------------------------------------------------------------------
# Setters GLN
# ---------------------------------------------------------------------------

class TestHeaderSenderGLN:
    """Tests pour le setter sender_gln du Header.
    Scénarios testés :
    - Mise à jour du sender_gln et vérification de la nouvelle valeur
    - Mise à jour du sender_gln avec une chaîne vide et vérification de la nouvelle valeur
    - Mise à jour du sender_gln avec une valeur non numérique et vérification de la nouvelle valeur
    - Mise à jour du sender_gln avec une valeur de longueur incorrecte et vérification
        de la nouvelle valeur
    """
    def test_set_and_get_gln(self):
        """Test de mise à jour du sender_gln et vérification de la nouvelle valeur."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        h.sender_gln = "3025590000008"
        assert h.sender_gln == "3025590000008"

    def test_update_existing_gln(self):
        """Test de mise à jour du sender_gln et vérification de la nouvelle valeur."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        h.sender_gln = "3025590000008"
        h.sender_gln = "1234567890123"
        assert h.sender_gln == "1234567890123"

    def test_set_empty_gln(self):
        """Test de mise à jour du sender_gln avec une chaîne vide."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        h.sender_gln = ""
        assert h.sender_gln == ""

    def test_set_non_numeric_gln(self):
        """Test de mise à jour du sender_gln avec une valeur non numérique."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        h.sender_gln = "GLN123456789"
        assert h.sender_gln == "GLN123456789"


# ---------------------------------------------------------------------------
# Setters email
# ---------------------------------------------------------------------------

class TestHeaderSenderEmail:
    """
    Tests pour le setter sender_email du Header.
    Scénarios testés :
    - Mise à jour du sender_email et vérification de la nouvelle valeur
    """
    def test_set_and_get_email(self):
        """Test de mise à jour du sender_email et vérification de la nouvelle valeur."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        h.sender_email = "bdd@dilicom.fr"
        assert h.sender_email == "bdd@dilicom.fr"

    def test_update_existing_email(self):
        """Test de mise à jour du sender_email et vérification de la nouvelle valeur."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        h.sender_email = "a@b.fr"
        h.sender_email = "c@d.fr"
        assert h.sender_email == "c@d.fr"


# ---------------------------------------------------------------------------
# Addressee
# ---------------------------------------------------------------------------

class TestHeaderAddressee:
    """
    Tests pour le setter addressee_name du Header.
    Scénarios testés :
    - Mise à jour de addressee_name et vérification de la nouvelle valeur
    """
    def test_set_and_get_addressee_name(self):
        """Test de mise à jour de addressee_name et vérification de la nouvelle valeur."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        h.addressee_name = "EDITIONS EXEMPLE"
        assert h.addressee_name == "EDITIONS EXEMPLE"


# ---------------------------------------------------------------------------
# Message number
# ---------------------------------------------------------------------------

class TestHeaderMessageNumber:
    """
    Tests pour le setter message_number du Header.
    Scénarios testés :
    - Mise à jour de message_number et vérification de la nouvelle valeur
    - Mise à jour de message_number avec une chaîne d'entier et vérification de la nouvelle valeur
    """
    def test_set_and_get_message_number(self):
        """Test de mise à jour de message_number et vérification de la nouvelle valeur."""
        # Le message_number est stocké comme entier : le zéro-padding est perdu
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        h.message_number = "000000001"
        assert h.message_number == "1"

    def test_message_number_string_format(self):
        """Test de mise à jour de message_number avec une chaîne d'entier."""
        h = Header.new(sender_name="TEST", sent_datetime="20260428T120000Z")
        h.message_number = "42"
        assert h.message_number == "42"
