from .generated.v3_0 import Header as _Header   # type: ignore

__all__ = ["Header"]


class Header:
    def __init__(self, raw: _Header) -> None: ...    # pylint: disable=unused-argument

    @classmethod
    def new(cls, sender_name: str, sent_datetime: str) -> "Header": ...    # pylint: disable=unused-argument

    @property
    def sender_name(self) -> str: ...

    @sender_name.setter
    def sender_name(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def sender_gln(self) -> str | None: ...

    @sender_gln.setter
    def sender_gln(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def sender_email(self) -> str | None: ...

    @sender_email.setter
    def sender_email(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def addressee_name(self) -> str | None: ...

    @addressee_name.setter
    def addressee_name(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def addressee_gln(self) -> str | None: ...

    @addressee_gln.setter
    def addressee_gln(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def message_number(self) -> str | None: ...

    @message_number.setter
    def message_number(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def sent_datetime(self) -> str: ...

    @sent_datetime.setter
    def sent_datetime(self, value: str) -> None: ...    # pylint: disable=unused-argument

    @property
    def raw(self) -> _Header: ...

    def __repr__(self) -> str: ...
