"""Module de modélisation du header d'un message ONIX.

Ce module définit les dataclasses correspondant au bloc ``<Header>`` d'un
message ONIX 3.0.  Chaque classe reflète fidèlement la hiérarchie XML :

.. code-block:: xml

    <Header>
      <Sender>
        <SenderIdentifier>
          <SenderIDType>06</SenderIDType>
          <IDValue>1234567890123</IDValue>
        </SenderIdentifier>
        <SenderName>Expéditeur Exemple</SenderName>
        <EmailAddress>contact@exemple.fr</EmailAddress>
      </Sender>
      <Addressee>
        <AddresseeIdentifier>
          <AddresseeIDType>06</AddresseeIDType>
          <IDValue>9876543210987</IDValue>
        </AddresseeIdentifier>
        <AddresseeName>Destinataire Exemple</AddresseeName>
      </Addressee>
      <MessageNumber>000000001</MessageNumber>
      <SentDateTime>20260101T000000Z</SentDateTime>
    </Header>

Chaque classe expose deux méthodes symétriques :

* ``from_xml(element)`` — désérialise un ``xml.etree.ElementTree.Element``
  vers la dataclass.
* ``to_xml()`` — sérialise la dataclass en ``xml.etree.ElementTree.Element``
  prêt à être intégré dans un arbre XML.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from xml.etree.ElementTree import Element, SubElement

@dataclass
class SenderIdentifier:
    """Identifiant qualifié de l'expéditeur (bloc ``<SenderIdentifier>``).

    Un identifiant ONIX est toujours composé de deux éléments : un **type**
    qui précise le référentiel utilisé (liste de codes ONIX 44, p. ex. ``06``
    pour GLN) et une **valeur** dans ce référentiel.

    Attributes:
        sender_id_type: Code du type d'identifiant (liste de codes ONIX 44).
            Exemple : ``"06"`` pour un GLN (Global Location Number).
        id_value: Valeur de l'identifiant dans le référentiel désigné par
            ``sender_id_type``. Exemple : ``"1234567890123"``.
    """

    sender_id_type: str
    id_value: str

    @staticmethod
    def from_xml(element: Element) -> SenderIdentifier:
        """Construit un :class:`SenderIdentifier` depuis un élément XML.

        Args:
            element: Élément ``<SenderIdentifier>`` issu du parsing XML.

        Returns:
            Instance peuplée avec les valeurs lues dans l'élément.
        """
        return SenderIdentifier(
            sender_id_type=element.findtext("SenderIDType", ""),
            id_value=element.findtext("IDValue", ""),
        )

    def to_xml(self) -> Element:
        """Sérialise l'identifiant en élément ``<SenderIdentifier>``.

        Returns:
            Élément XML ``<SenderIdentifier>`` contenant ``<SenderIDType>``
            et ``<IDValue>``.
        """
        el = Element("SenderIdentifier")
        SubElement(el, "SenderIDType").text = self.sender_id_type
        SubElement(el, "IDValue").text = self.id_value
        return el


@dataclass
class Sender:
    """Expéditeur du message ONIX (bloc ``<Sender>``).

    Identifie l'organisation qui génère et émet le fichier ONIX.  Le nom
    est obligatoire ; l'identifiant structuré et l'adresse e-mail sont
    facultatifs mais recommandés pour faciliter les rapprochements
    automatiques entre partenaires.

    Attributes:
        sender_name: Nom lisible de l'expéditeur (élément ``<SenderName>``).
            Exemple : ``"Expéditeur Exemple"``.
        sender_identifier: Identifiant qualifié de l'expéditeur
            (bloc ``<SenderIdentifier>``).  ``None`` si absent du message.
        email_address: Adresse e-mail de contact de l'expéditeur
            (élément ``<EmailAddress>``).  ``None`` si absente.
    """

    sender_name: str
    sender_identifier: Optional[SenderIdentifier] = None
    email_address: Optional[str] = None

    @staticmethod
    def from_xml(element: Element) -> Sender:
        """Construit un :class:`Sender` depuis un élément XML.

        Args:
            element: Élément ``<Sender>`` issu du parsing XML.

        Returns:
            Instance peuplée avec les valeurs lues dans l'élément.
        """
        identifier_el = element.find("SenderIdentifier")
        return Sender(
            sender_name=element.findtext("SenderName", ""),
            sender_identifier=SenderIdentifier.from_xml(identifier_el) \
                                    if identifier_el is not None \
                                    else None,
            email_address=element.findtext("EmailAddress"),
        )

    def to_xml(self) -> Element:
        """Sérialise l'expéditeur en élément ``<Sender>``.

        Les éléments optionnels (``<SenderIdentifier>``, ``<EmailAddress>``)
        ne sont inclus dans l'arbre que s'ils sont renseignés.

        Returns:
            Élément XML ``<Sender>`` complet.
        """
        el = Element("Sender")
        if self.sender_identifier is not None:
            el.append(self.sender_identifier.to_xml())
        SubElement(el, "SenderName").text = self.sender_name
        if self.email_address is not None:
            SubElement(el, "EmailAddress").text = self.email_address
        return el


@dataclass
class AddresseeIdentifier:
    """Identifiant qualifié du destinataire (bloc ``<AddresseeIdentifier>``).

    Symétrique de :class:`SenderIdentifier` mais appliqué au destinataire
    du message.

    Attributes:
        addressee_id_type: Code du type d'identifiant (liste de codes ONIX 44).
            Exemple : ``"06"`` pour un GLN.
        id_value: Valeur de l'identifiant. Exemple : ``"9876543210987"``.
    """

    addressee_id_type: str
    id_value: str

    @staticmethod
    def from_xml(element: Element) -> AddresseeIdentifier:
        """Construit un :class:`AddresseeIdentifier` depuis un élément XML.

        Args:
            element: Élément ``<AddresseeIdentifier>`` issu du parsing XML.

        Returns:
            Instance peuplée avec les valeurs lues dans l'élément.
        """
        return AddresseeIdentifier(
            addressee_id_type=element.findtext("AddresseeIDType", ""),
            id_value=element.findtext("IDValue", ""),
        )

    def to_xml(self) -> Element:
        """Sérialise l'identifiant en élément ``<AddresseeIdentifier>``.

        Returns:
            Élément XML ``<AddresseeIdentifier>`` contenant
            ``<AddresseeIDType>`` et ``<IDValue>``.
        """
        el = Element("AddresseeIdentifier")
        SubElement(el, "AddresseeIDType").text = self.addressee_id_type
        SubElement(el, "IDValue").text = self.id_value
        return el


@dataclass
class Addressee:
    """Destinataire du message ONIX (bloc ``<Addressee>``).

    Identifie l'organisation à qui le fichier ONIX est destiné.  Le nom
    est obligatoire ; l'identifiant structuré est facultatif.

    Attributes:
        addressee_name: Nom lisible du destinataire (élément
            ``<AddresseeName>``).  Exemple : ``"Destinataire Exemple"``.
        addressee_identifier: Identifiant qualifié du destinataire
            (bloc ``<AddresseeIdentifier>``).  ``None`` si absent du message.
    """

    addressee_name: str
    addressee_identifier: Optional[AddresseeIdentifier] = None

    @staticmethod
    def from_xml(element: Element) -> Addressee:
        """Construit un :class:`Addressee` depuis un élément XML.

        Args:
            element: Élément ``<Addressee>`` issu du parsing XML.

        Returns:
            Instance peuplée avec les valeurs lues dans l'élément.
        """
        identifier_el = element.find("AddresseeIdentifier")
        return Addressee(
            addressee_name=element.findtext("AddresseeName", ""),
            addressee_identifier=AddresseeIdentifier.from_xml(identifier_el) \
                                        if identifier_el is not None \
                                        else None,
        )

    def to_xml(self) -> Element:
        """Sérialise le destinataire en élément ``<Addressee>``.

        L'élément ``<AddresseeIdentifier>`` n'est inclus que s'il est
        renseigné.

        Returns:
            Élément XML ``<Addressee>`` complet.
        """
        el = Element("Addressee")
        if self.addressee_identifier is not None:
            el.append(self.addressee_identifier.to_xml())
        SubElement(el, "AddresseeName").text = self.addressee_name
        return el


@dataclass
class Header:
    """En-tête d'un message ONIX (bloc ``<Header>``).

    Le header est le premier bloc d'un message ONIX.  Il identifie
    l'expéditeur, le destinataire, numérote le message et horodate son
    envoi.  Ces informations sont indispensables pour tracer les échanges
    et détecter d'éventuels messages manquants ou dupliqués.

    Attributes:
        sender: Expéditeur du message (bloc ``<Sender>``).
        addressee: Destinataire du message (bloc ``<Addressee>``).
        message_number: Numéro séquentiel du message (élément
            ``<MessageNumber>``).  Exemple : ``"000000001"``.
        sent_datetime: Horodatage d'envoi au format ONIX
            (élément ``<SentDateTime>``).  Exemple : ``"20260101T000000Z"``
            (voir liste de codes ONIX 55 pour les formats supportés).
    """

    sender: Sender
    addressee: Addressee
    message_number: str
    sent_datetime: str

    @staticmethod
    def from_xml(element: Element) -> Header:
        """Construit un :class:`Header` depuis un élément XML.

        Args:
            element: Élément ``<Header>`` issu du parsing XML.

        Returns:
            Instance peuplée avec les valeurs lues dans l'élément.
            Si les blocs ``<Sender>`` ou ``<Addressee>`` sont absents,
            des instances vides sont utilisées en repli.
        """
        sender_el = element.find("Sender")
        addressee_el = element.find("Addressee")
        return Header(
            sender=Sender.from_xml(sender_el)
                        if sender_el is not None
                        else Sender(sender_name=""),
            addressee=Addressee.from_xml(addressee_el)
                        if addressee_el is not None
                        else Addressee(addressee_name=""),
            message_number=element.findtext("MessageNumber", ""),
            sent_datetime=element.findtext("SentDateTime", ""),
        )

    def to_xml(self) -> Element:
        """Sérialise le header en élément ``<Header>``.

        Les sous-éléments sont générés dans l'ordre prescrit par la norme
        ONIX : ``<Sender>``, ``<Addressee>``, ``<MessageNumber>``,
        ``<SentDateTime>``.

        Returns:
            Élément XML ``<Header>`` complet, prêt à être inséré dans
            un arbre ``ONIXMessage``.
        """
        el = Element("Header")
        el.append(self.sender.to_xml())
        el.append(self.addressee.to_xml())
        SubElement(el, "MessageNumber").text = self.message_number
        SubElement(el, "SentDateTime").text = self.sent_datetime
        return el
