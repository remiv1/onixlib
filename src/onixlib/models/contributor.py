"""
Façade ergonomique pour les contributeurs ONIX 3.0.

Exemple d'utilisation :

    from onixlib import ContributorRole

    auteur = book.author
    auteur.first_name = "André"
    auteur.last_name  = "RAVIER"
    auteur.role       = ContributorRole.A01

    # Ou depuis zéro :
    nouveau = book.add_contributor(role=ContributorRole.B06)
    nouveau.first_name = "Jean"
    nouveau.last_name  = "DUPONT"
"""

from __future__ import annotations

from onixlib.models.generated.v3_0 import (
    Contributor as _Contributor,
    ContributorRole as _ContributorRole,
    KeyNames,
    NamesBeforeKey,
    List17 as ContributorRole,
)

__all__ = ["Contributor", "ContributorRole"]


class Contributor:
    """Façade ergonomique sur la dataclass ONIX :class:`Contributor` générée."""

    def __init__(self, raw: _Contributor | None = None) -> None:
        if raw is None:
            raw = _Contributor()
        self._raw = raw

    # ------------------------------------------------------------------ #
    # Prénom                                                               #
    # ------------------------------------------------------------------ #

    @property
    def first_name(self) -> str:
        """Prénom(s) du contributeur (NamesBeforeKey)."""
        return self._raw.names_before_key.value if self._raw.names_before_key else ""

    @first_name.setter
    def first_name(self, value: str) -> None:
        if self._raw.names_before_key is None:
            self._raw.names_before_key = NamesBeforeKey(value=value)
        else:
            self._raw.names_before_key.value = value

    # ------------------------------------------------------------------ #
    # Nom de famille                                                        #
    # ------------------------------------------------------------------ #

    @property
    def last_name(self) -> str:
        """Nom de famille principal du contributeur (KeyNames)."""
        return self._raw.key_names.value if self._raw.key_names else ""

    @last_name.setter
    def last_name(self, value: str) -> None:
        if self._raw.key_names is None:
            self._raw.key_names = KeyNames(value=value)
        else:
            self._raw.key_names.value = value

    # ------------------------------------------------------------------ #
    # Rôle                                                                 #
    # ------------------------------------------------------------------ #

    @property
    def role(self) -> ContributorRole | None:
        """Premier rôle du contributeur (code ONIX List 17, ex. A01 = auteur)."""
        if not self._raw.contributor_role:
            return None
        return self._raw.contributor_role[0].value

    @role.setter
    def role(self, value: ContributorRole) -> None:
        if self._raw.contributor_role:
            self._raw.contributor_role[0].value = value
        else:
            self._raw.contributor_role.append(_ContributorRole(value=value))

    # ------------------------------------------------------------------ #
    # Propriétés dérivées                                                   #
    # ------------------------------------------------------------------ #

    @property
    def full_name(self) -> str:
        """Nom complet : prénom + nom de famille."""
        return " ".join(p for p in (self.first_name, self.last_name) if p)

    # ------------------------------------------------------------------ #
    # Accès au modèle généré                                                #
    # ------------------------------------------------------------------ #

    @property
    def raw(self) -> _Contributor:
        """Retourne la dataclass ONIX sous-jacente."""
        return self._raw

    def __repr__(self) -> str:
        role = self.role.value if self.role is not None else None
        return f"Contributor(full_name={self.full_name!r}, role={role!r})"
