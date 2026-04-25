"""Utilitaires de formatage et de parsing des dates ONIX 3.0.

Selon la norme ISO 8601 et les recommandations du guide pratique ONIX CLIL (§ 8.7),
les dates ONIX sont encodées sous forme de chaînes dont le format est identifié par
un code de la liste de codes 55 (DateFormat).

Formats pris en charge :

    +---------+-----------------------------+---------------------------+
    |  Code   |  Format                     |  Exemple                  |
    +=========+=============================+===========================+
    |   00    |  YYYYMMDD                   |  20150403                 |
    |   01    |  YYYYMM                     |  201504                   |
    |   02    |  YYYY                       |  2015                     |
    |   03    |  YYYYQ  (trimestre 1–4)     |  20152                    |
    |   04    |  YYYYWnn  (semaine ISO)     |  201514                   |
    |   05    |  YYYYMMDDTHHmm              |  20150403T1527            |
    |   06    |  YYYYMMDDTHHmmss            |  20150403T152746          |
    |   07    |  YYYYMMDDTHHmmssZ  (UTC)    |  20150403T152746Z         |
    |   08    |  YYYYMMDDTHHmm±HHmm         |  20150403T1527+0100       |
    |   09    |  YYYYMMDDTHHmmss±HHmm       |  20150403T152746+0100     |
    +---------+-----------------------------+---------------------------+

Convention minuit (§ 8.7.2)
----------------------------
Lorsqu'une date de début s'applique à minuit, elle doit être exprimée
par ``00:00`` (et non ``24:00``).  Une date de fin s'appliquant à minuit
doit être exprimée par ``24:00`` (et non ``00:00``) ; dans les formats
ONIX sans heure (code ``00``), cette convention est portée par le rôle
de date (PriceDateRole) et non par la chaîne elle-même.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone
from typing import Union

# ---------------------------------------------------------------------------
# Type utilitaire
# ---------------------------------------------------------------------------

DateLike = Union[date, datetime]

# ---------------------------------------------------------------------------
# Constantes — ONIX Code List 55 : DateFormat
# ---------------------------------------------------------------------------

FMT_YYYYMMDD = "00"          # 20150403
FMT_YYYYMM = "01"            # 201504
FMT_YYYY = "02"              # 2015
FMT_YYYYQ = "03"             # 20152          (trimestre 1–4)
FMT_YYYYWNN = "04"           # 201514         (semaine ISO)
FMT_YYYYMMDD_THHMM = "05"    # 20150403T1527
FMT_YYYYMMDD_THHMMSS = "06"  # 20150403T152746
FMT_YYYYMMDD_THHMMSSZ = "07" # 20150403T152746Z  (UTC)
FMT_YYYYMMDD_THHMM_TZ = "08" # 20150403T1527+0100
FMT_YYYYMMDD_THHMMSS_TZ = "09"  # 20150403T152746+0100

# Expression régulière pour extraire le décalage UTC (±HHMM) en fin de chaîne
_RE_TZ_OFFSET = re.compile(r"^(.+?)([+-]\d{4})$")

# Masques strptime internes
_STRPTIME_THHMM = "%Y%m%dT%H%M"
_STRPTIME_THHMMSS = "%Y%m%dT%H%M%S"


# ---------------------------------------------------------------------------
# Parsing (format in)
# ---------------------------------------------------------------------------

def parse_onix_date(date_str: str, date_format: str) -> DateLike | None:
    """Parse une chaîne de date ONIX selon le code de format (liste de codes 55).

    Args:
        date_str:    Chaîne de date brute extraite du XML ONIX.
        date_format: Code de format ONIX (liste de codes 55, voir constantes
                     ``FMT_*`` de ce module).

    Returns:
        Un objet :class:`datetime.date` pour les formats sans heure, un objet
        :class:`datetime.datetime` (éventuellement avec fuseau horaire) pour
        les formats avec heure, ou ``None`` si *date_str* est vide.

    Raises:
        ValueError: Si la chaîne ne correspond pas au format attendu, ou si le
                    code de format est inconnu.
    """
    if not date_str or not date_str.strip():
        date_returned = None

    date_str = date_str.strip()

    if date_format == FMT_YYYYMMDD:
        date_returned = datetime.strptime(date_str, "%Y%m%d").date()

    elif date_format == FMT_YYYYMM:
        date_returned =  datetime.strptime(date_str + "01", "%Y%m%d").date()

    elif date_format == FMT_YYYY:
        date_returned =  date(int(date_str), 1, 1)

    elif date_format == FMT_YYYYQ:
        year = int(date_str[:4])
        quarter = int(date_str[4])
        if not 1 <= quarter <= 4:
            raise ValueError(f"Trimestre invalide : {quarter!r} dans {date_str!r}")
        month = (quarter - 1) * 3 + 1
        date_returned =  date(year, month, 1)

    elif date_format == FMT_YYYYWNN:
        year = int(date_str[:4])
        week = int(date_str[4:])
        # Premier lundi de la semaine ISO donnée
        date_returned =  datetime.strptime(f"{year}-W{week:02d}-1", "%G-W%V-%u").date()

    elif date_format == FMT_YYYYMMDD_THHMM:
        date_returned =  datetime.strptime(date_str, _STRPTIME_THHMM)

    elif date_format == FMT_YYYYMMDD_THHMMSS:
        date_returned =  datetime.strptime(date_str, _STRPTIME_THHMMSS)

    elif date_format == FMT_YYYYMMDD_THHMMSSZ:
        dt = datetime.strptime(date_str.rstrip("Z"), "%Y%m%dT%H%M%S")
        date_returned =  dt.replace(tzinfo=timezone.utc)

    elif date_format in (FMT_YYYYMMDD_THHMM_TZ, FMT_YYYYMMDD_THHMMSS_TZ):
        date_returned =  _parse_datetime_with_offset(date_str, date_format)
    else:
        raise ValueError(f"Code de format ONIX inconnu : {date_format!r}")
    return date_returned


def _parse_datetime_with_offset(date_str: str, date_format: str) -> datetime:
    """Parse un datetime ONIX accompagné d'un décalage UTC (±HHMM).

    Args:
        date_str:    Chaîne de date incluant le décalage, ex. ``20150403T1527+0100``.
        date_format: Code ``FMT_YYYYMMDD_THHMM_TZ`` ou ``FMT_YYYYMMDD_THHMMSS_TZ``.

    Returns:
        Objet :class:`datetime.datetime` avec fuseau horaire.

    Raises:
        ValueError: Si le décalage UTC est absent ou malformé.
    """
    match = _RE_TZ_OFFSET.match(date_str)
    if not match:
        raise ValueError(
            f"Décalage UTC manquant ou malformé dans la chaîne : {date_str!r}"
        )

    dt_part, tz_part = match.group(1), match.group(2)
    sign = 1 if tz_part[0] == "+" else -1
    tz_hours = int(tz_part[1:3])
    tz_minutes = int(tz_part[3:5])
    offset = timezone(timedelta(hours=sign * tz_hours, minutes=sign * tz_minutes))

    strptime_fmt = (
        _STRPTIME_THHMM if date_format == FMT_YYYYMMDD_THHMM_TZ
        else _STRPTIME_THHMMSS
    )
    return datetime.strptime(dt_part, strptime_fmt).replace(tzinfo=offset)


# ---------------------------------------------------------------------------
# Formatage (format out)
# ---------------------------------------------------------------------------

def format_onix_date(dt: object, date_format: str) -> str:
    """Formate une date Python en chaîne ONIX selon le code de format (liste 55).

    Args:
        dt:          Objet :class:`datetime.date` ou :class:`datetime.datetime`.
        date_format: Code de format ONIX (liste de codes 55, voir constantes
                     ``FMT_*`` de ce module).

    Returns:
        Chaîne de date au format ONIX attendu (ex. ``"20150403"``).

    Raises:
        TypeError:  Si *dt* n'est pas un objet ``date`` ou ``datetime``.
        ValueError: Si le code de format est inconnu, ou si un format horodaté
                    est demandé avec un simple objet :class:`~datetime.date`.
    """
    if not isinstance(dt, date):
        raise TypeError(
            f"dt doit être un objet date ou datetime, reçu : {type(dt)!r}"
        )

    if date_format == FMT_YYYYMMDD:
        return dt.strftime("%Y%m%d")

    if date_format == FMT_YYYYMM:
        return dt.strftime("%Y%m")

    if date_format == FMT_YYYY:
        return dt.strftime("%Y")

    if date_format == FMT_YYYYQ:
        quarter = (dt.month - 1) // 3 + 1
        return f"{dt.year}{quarter}"

    if date_format == FMT_YYYYWNN:
        iso = dt.isocalendar()
        return f"{iso[0]}{iso[1]:02d}"

    # Formats avec composante horaire — requiert un datetime
    if date_format in (
        FMT_YYYYMMDD_THHMM,
        FMT_YYYYMMDD_THHMMSS,
        FMT_YYYYMMDD_THHMMSSZ,
        FMT_YYYYMMDD_THHMM_TZ,
        FMT_YYYYMMDD_THHMMSS_TZ,
    ):
        if not isinstance(dt, datetime):
            raise ValueError(
                f"Le format {date_format!r} requiert un objet datetime ; "
                f"un objet date a été fourni."
            )
        return _format_onix_datetime(dt, date_format)

    raise ValueError(f"Code de format ONIX inconnu : {date_format!r}")


def _format_onix_datetime(dt: datetime, date_format: str) -> str:
    """Formate la partie horodatage d'une date ONIX."""

    if date_format == FMT_YYYYMMDD_THHMM:
        return dt.strftime(_STRPTIME_THHMM)

    if date_format == FMT_YYYYMMDD_THHMMSS:
        return dt.strftime(_STRPTIME_THHMMSS)

    if date_format == FMT_YYYYMMDD_THHMMSSZ:
        utc_dt = dt.astimezone(timezone.utc) if dt.tzinfo is not None else dt
        return utc_dt.strftime(_STRPTIME_THHMMSS) + "Z"

    if date_format == FMT_YYYYMMDD_THHMM_TZ:
        return dt.strftime(_STRPTIME_THHMM) + _format_utc_offset(dt)

    if date_format == FMT_YYYYMMDD_THHMMSS_TZ:
        return dt.strftime(_STRPTIME_THHMMSS) + _format_utc_offset(dt)

    raise ValueError(f"Format datetime ONIX inconnu : {date_format!r}")


def _format_utc_offset(dt: datetime) -> str:
    """Retourne le décalage UTC d'un datetime au format ``±HHMM``.

    Args:
        dt: Objet :class:`datetime.datetime` avec fuseau horaire.

    Returns:
        Chaîne de décalage, ex. ``"+0100"`` ou ``"-0500"``.

    Raises:
        ValueError: Si *dt* ne contient pas d'information de fuseau horaire.
    """
    if dt.tzinfo is None:
        raise ValueError(
            "Le datetime fourni ne contient pas d'information de fuseau horaire "
            "(tzinfo est None). Utilisez un datetime avec fuseau pour les formats "
            "FMT_YYYYMMDD_THHMM_TZ et FMT_YYYYMMDD_THHMMSS_TZ."
        )
    offset = dt.utcoffset()
    if offset is None:
        raise ValueError(
            "utcoffset() a retourné None ; vérifiez l'implémentation du fuseau horaire."
        )
    total_minutes = int(offset.total_seconds() / 60)
    sign = "+" if total_minutes >= 0 else "-"
    hours, minutes = divmod(abs(total_minutes), 60)
    return f"{sign}{hours:02d}{minutes:02d}"
