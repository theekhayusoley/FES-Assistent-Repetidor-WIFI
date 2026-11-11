"""Validation and comparison algorithm for Wi-Fi RSSI measurements.

RSSI values are expressed in dBm. Values closer to zero represent a stronger
received signal (for example, -55 dBm is stronger than -78 dBm).
"""

from __future__ import annotations

import math
from typing import Iterable, List, Sequence

from models import Configuracio, ResultatComparacio, ResultatConfiguracio

NUM_PUNTS_ESPERATS = 5
NUM_CONFIGURACIONS_ESPERADES = 3
RSSI_MINIM_ADMES = -120.0
RSSI_MAXIM_ADMES = 0.0


class ErrorAnalisi(ValueError):
    """Raised when the measurements cannot be analysed safely."""


def convertir_rssi(valor: object, camp: str = "RSSI") -> float:
    """Convert an RSSI-like input to a finite dBm float.

    Decimal commas are accepted to make manual entry friendlier in Catalan
    and Spanish locales. This MVP accepts values in the practical validation
    interval [-120, 0] dBm.
    """
    if isinstance(valor, bool) or valor is None:
        raise ErrorAnalisi(f"El valor de {camp} no és un número vàlid.")

    try:
        if isinstance(valor, str):
            text = valor.strip().replace(",", ".")
            if not text:
                raise ValueError
            numero = float(text)
        else:
            numero = float(valor)
    except (TypeError, ValueError, OverflowError):
        raise ErrorAnalisi(f"El valor de {camp} no és un número vàlid.") from None

    if not math.isfinite(numero):
        raise ErrorAnalisi(f"El valor de {camp} ha de ser un número finit.")
    if not RSSI_MINIM_ADMES <= numero <= RSSI_MAXIM_ADMES:
        raise ErrorAnalisi(
            f"El valor de {camp} ha d'estar entre {RSSI_MINIM_ADMES:g} i "
            f"{RSSI_MAXIM_ADMES:g} dBm."
        )
    return numero


def validar_llindar(llindar: object) -> float:
    """Validate and normalize the user-selected RSSI threshold."""
    return convertir_rssi(llindar, "llindar")


def validar_configuracions(
    configuracions: Sequence[Configuracio],
    punts_esperats: Iterable[str] | None = None,
) -> List[Configuracio]:
    """Validate the three configurations and normalize their measurements."""
    if len(configuracions) != NUM_CONFIGURACIONS_ESPERADES:
        raise ErrorAnalisi(
            f"Cal introduir exactament {NUM_CONFIGURACIONS_ESPERADES} configuracions."
        )

    noms_configuracio = []
    for configuracio in configuracions:
        if not isinstance(configuracio, Configuracio):
            raise ErrorAnalisi("Cada configuració ha de ser un objecte Configuracio.")
        if not isinstance(configuracio.nom, str):
            raise ErrorAnalisi("El nom de cada configuració ha de ser text.")
        noms_configuracio.append(configuracio.nom.strip())
    if any(not nom for nom in noms_configuracio):
        raise ErrorAnalisi("Totes les configuracions han de tenir un nom.")
    if len(set(noms_configuracio)) != len(noms_configuracio):
        raise ErrorAnalisi("Els noms de les configuracions han de ser diferents.")

    referent = set(punts_esperats) if punts_esperats is not None else None
    normalitzades: List[Configuracio] = []

    for configuracio in configuracions:
        if not isinstance(configuracio.mesures, dict):
            raise ErrorAnalisi(
                f"Les mesures de '{configuracio.nom}' han de ser un diccionari."
            )

        noms_punts = list(configuracio.mesures.keys())
        if len(noms_punts) != NUM_PUNTS_ESPERATS:
            raise ErrorAnalisi(
                f"La configuració '{configuracio.nom}' ha de tenir exactament "
                f"{NUM_PUNTS_ESPERATS} mesures; en té {len(noms_punts)}."
            )
        if any(not isinstance(p, str) or not p.strip() for p in noms_punts):
            raise ErrorAnalisi("Tots els punts de mesura han de tenir un nom.")

        conjunt_punts = set(noms_punts)
        if referent is None:
            referent = conjunt_punts
        elif conjunt_punts != referent:
            raise ErrorAnalisi(
                "Les tres configuracions han de contenir els mateixos cinc punts de mesura."
            )

        mesures_numeriques = {
            punt: convertir_rssi(valor, f"{configuracio.nom} / {punt}")
            for punt, valor in configuracio.mesures.items()
        }
        normalitzades.append(Configuracio(configuracio.nom.strip(), mesures_numeriques))

    if len(referent or set()) != NUM_PUNTS_ESPERATS:
        raise ErrorAnalisi(
            f"Cal definir exactament {NUM_PUNTS_ESPERATS} punts de mesura diferents."
        )

    return normalitzades


def analitzar_configuracio(
    configuracio: Configuracio, llindar: object
) -> ResultatConfiguracio:
    """Count points that meet the threshold and identify weak points."""
    llindar_validat = validar_llindar(llindar)
    if len(configuracio.mesures) != NUM_PUNTS_ESPERATS:
        raise ErrorAnalisi(
            f"La configuració '{configuracio.nom}' no conté cinc mesures completes."
        )

    mesures = {
        punt: convertir_rssi(valor, f"{configuracio.nom} / {punt}")
        for punt, valor in configuracio.mesures.items()
    }
    punts_febles = [punt for punt, valor in mesures.items() if valor < llindar_validat]
    punts_correctes = NUM_PUNTS_ESPERATS - len(punts_febles)

    return ResultatConfiguracio(
        nom=configuracio.nom,
        punts_correctes=punts_correctes,
        senyal_minim=min(mesures.values()),
        punts_febles=punts_febles,
    )


def comparar_configuracions(
    configuracions: Sequence[Configuracio], llindar: object
) -> ResultatComparacio:
    """Rank configurations by coverage count, then by their weakest RSSI.

    The highest number of points meeting the threshold wins. In case of a tie,
    the setup with the strongest weakest-point reading (largest dBm value) wins.
    If both criteria tie, all tied setups are returned as equivalent winners.
    """
    llindar_validat = validar_llindar(llindar)
    configuracions_valides = validar_configuracions(configuracions)
    resultats = [
        analitzar_configuracio(configuracio, llindar_validat)
        for configuracio in configuracions_valides
    ]

    millor_puntuacio = max(
        (resultat.punts_correctes, resultat.senyal_minim)
        for resultat in resultats
    )
    guanyadores = [
        resultat.nom
        for resultat in resultats
        if (resultat.punts_correctes, resultat.senyal_minim) == millor_puntuacio
    ]

    return ResultatComparacio(
        llindar=llindar_validat,
        resultats=resultats,
        guanyadores=guanyadores,
    )
