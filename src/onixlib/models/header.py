"""Facade for the ONIX 3.0 Header block.

Wraps the xsdata-generated :class:`~onixlib.models.generated.v3_0.Header`
dataclass and exposes ergonomic properties.

Example usage::

    from onixlib.models.header import Header

    # Read from a parsed Notice:
    header = notice.header
    print(header.sender_name)
    print(header.message_number)

    # Build from scratch:
    header = Header.new(
        sender_name="DILICOM",
        sent_datetime="20260428T040029Z",
    )
    header.sender_gln = "3025590000008"
    header.sender_email = "bdd@dilicom.fr"
    header.addressee_name = "EDITIONS EXEMPLE"
    header.message_number = "000000001"
"""

from __future__ import annotations

from .generated.v3_0 import (
    Addressee as _Addressee,
    AddresseeIdentifier as _AddresseeIdentifier,
    AddresseeIdtype,
    AddresseeName,
    EmailAddress,
    Header as _Header,
    Idvalue,
    List44,
    MessageNumber,
    Sender as _Sender,
    SenderIdentifier as _SenderIdentifier,
    SenderIdtype,
    SenderName,
    SentDateTime,
)

__all__ = ["Header"]

_GLN_TYPE = List44.VALUE_06  # "06" — Global Location Number


class Header:
    """Ergonomic facade over the ONIX :class:`Header` dataclass."""

    def __init__(self, raw: _Header) -> None:
        self._raw = raw

    # ------------------------------------------------------------------ #
    # Factory                                                              #
    # ------------------------------------------------------------------ #

    @classmethod
    def new(cls, sender_name: str, sent_datetime: str) -> "Header":
        """Create a minimal Header with the required fields.

        Args:
            sender_name:    Human-readable name of the sender organisation.
            sent_datetime:  Timestamp in ONIX format, e.g. ``"20260428T040029Z"``.
        """
        raw = _Header(
            sender=_Sender(sender_name=SenderName(value=sender_name)),
            sent_date_time=SentDateTime(value=sent_datetime),
        )
        return cls(raw)

    # ------------------------------------------------------------------ #
    # Sender                                                               #
    # ------------------------------------------------------------------ #

    @property
    def sender_name(self) -> str:
        """Human-readable name of the message sender."""
        return self._raw.sender.sender_name.value if self._raw.sender.sender_name else ""

    @sender_name.setter
    def sender_name(self, value: str) -> None:
        if self._raw.sender.sender_name is None:
            self._raw.sender.sender_name = SenderName(value=value)
        else:
            self._raw.sender.sender_name.value = value

    @property
    def sender_gln(self) -> str | None:
        """GLN (Global Location Number) of the sender, or ``None`` if absent."""
        for si in self._raw.sender.sender_identifier:
            if si.sender_idtype.value == _GLN_TYPE:
                return si.idvalue.value
        return None

    @sender_gln.setter
    def sender_gln(self, value: str) -> None:
        for si in self._raw.sender.sender_identifier:
            if si.sender_idtype.value == _GLN_TYPE:
                si.idvalue.value = value
                return
        self._raw.sender.sender_identifier.append(
            _SenderIdentifier(
                sender_idtype=SenderIdtype(value=_GLN_TYPE),
                idvalue=Idvalue(value=value),
            )
        )

    @property
    def sender_email(self) -> str | None:
        """Email address of the sender, or ``None`` if absent."""
        return self._raw.sender.email_address.value if self._raw.sender.email_address else None

    @sender_email.setter
    def sender_email(self, value: str) -> None:
        if self._raw.sender.email_address is None:
            self._raw.sender.email_address = EmailAddress(value=value)
        else:
            self._raw.sender.email_address.value = value

    # ------------------------------------------------------------------ #
    # Addressee                                                            #
    # ------------------------------------------------------------------ #

    @property
    def addressee_name(self) -> str | None:
        """Human-readable name of the message addressee, or ``None`` if absent."""
        if not self._raw.addressee:
            return None
        addr = self._raw.addressee[0]
        return addr.addressee_name.value if addr.addressee_name else None

    @addressee_name.setter
    def addressee_name(self, value: str) -> None:
        if not self._raw.addressee:
            self._raw.addressee.append(
                _Addressee(addressee_name=AddresseeName(value=value))
            )
        else:
            addr = self._raw.addressee[0]
            if addr.addressee_name is None:
                addr.addressee_name = AddresseeName(value=value)
            else:
                addr.addressee_name.value = value

    @property
    def addressee_gln(self) -> str | None:
        """GLN of the addressee, or ``None`` if absent."""
        if not self._raw.addressee:
            return None
        for ai in self._raw.addressee[0].addressee_identifier:
            if ai.addressee_idtype.value == _GLN_TYPE:
                return ai.idvalue.value
        return None

    @addressee_gln.setter
    def addressee_gln(self, value: str) -> None:
        if not self._raw.addressee:
            self._raw.addressee.append(_Addressee())
        addr = self._raw.addressee[0]
        for ai in addr.addressee_identifier:
            if ai.addressee_idtype.value == _GLN_TYPE:
                ai.idvalue.value = value
                return
        addr.addressee_identifier.append(
            _AddresseeIdentifier(
                addressee_idtype=AddresseeIdtype(value=_GLN_TYPE),
                idvalue=Idvalue(value=value),
            )
        )

    # ------------------------------------------------------------------ #
    # Message metadata                                                     #
    # ------------------------------------------------------------------ #

    @property
    def message_number(self) -> str | None:
        """Sequential message number, or ``None`` if absent."""
        return str(self._raw.message_number.value) if self._raw.message_number else None

    @message_number.setter
    def message_number(self, value: str) -> None:
        if self._raw.message_number is None:
            self._raw.message_number = MessageNumber(value=int(value))
        else:
            self._raw.message_number.value = int(value)

    @property
    def sent_datetime(self) -> str:
        """Send timestamp in ONIX format (e.g. ``"20260428T040029Z"``)."""
        return self._raw.sent_date_time.value

    @sent_datetime.setter
    def sent_datetime(self, value: str) -> None:
        self._raw.sent_date_time.value = value

    # ------------------------------------------------------------------ #
    # Raw access                                                           #
    # ------------------------------------------------------------------ #

    @property
    def raw(self) -> _Header:
        """Returns the underlying xsdata :class:`Header` dataclass."""
        return self._raw

    def __repr__(self) -> str:
        return f"Header(sender={self.sender_name!r}, message_number={self.message_number!r})"
