from models import Configuracio, ResultatConfiguracio

NUM_PUNTS = 5
NUM_CONFIGURACIONS = 3


def convertir_rssi(valor, nom_camp="RSSI"):
    """Converteix una entrada a un valor RSSI vàlid."""
    try:
        numero = float(str(valor).strip().replace(",", "."))
    except ValueError:
        raise ValueError(f"El valor de {nom_camp} no és un número vàlid.")

    if not -120 <= numero <= 0:
        raise ValueError(f"El valor de {nom_camp} ha d'estar entre -120 i 0 dBm.")

    return numero


def validar_configuracions(configuracions):
    """Comprova que hi hagi tres configuracions amb els mateixos cinc punts."""
    if len(configuracions) != NUM_CONFIGURACIONS:
        raise ValueError("Cal introduir exactament tres configuracions.")

    punts_referencia = None
    configuracions_valides = []

    for configuracio in configuracions:
        if not isinstance(configuracio, Configuracio):
            raise ValueError("La configuració introduïda no és vàlida.")

        if not isinstance(configuracio.mesures, dict):
            raise ValueError("Les mesures han d'estar guardades en un diccionari.")

        if len(configuracio.mesures) != NUM_PUNTS:
            raise ValueError(f"Cada configuració ha de tenir {NUM_PUNTS} mesures.")

        punts = set(configuracio.mesures.keys())
        if punts_referencia is None:
            punts_referencia = punts
        elif punts != punts_referencia:
            raise ValueError("Les tres configuracions han de tenir els mateixos cinc punts.")

        mesures_valides = {}
        for punt, valor in configuracio.mesures.items():
            mesures_valides[punt] = convertir_rssi(valor, punt)

        configuracions_valides.append(
            Configuracio(configuracio.nom, mesures_valides)
        )

    return configuracions_valides


def analitzar_configuracio(configuracio, llindar):
    """Compta els punts que arriben al llindar i identifica els punts febles."""
    punts_febles = []

    for punt, valor in configuracio.mesures.items():
        if valor < llindar:
            punts_febles.append(punt)

    punts_correctes = NUM_PUNTS - len(punts_febles)
    senyal_minim = min(configuracio.mesures.values())

    return ResultatConfiguracio(
        configuracio.nom,
        punts_correctes,
        senyal_minim,
        punts_febles
    )


def comparar_configuracions(configuracions, llindar):
    """Compara les tres configuracions i retorna la recomanació."""
    llindar = convertir_rssi(llindar, "llindar")
    configuracions = validar_configuracions(configuracions)

    resultats = []
    for configuracio in configuracions:
        resultat = analitzar_configuracio(configuracio, llindar)
        resultats.append(resultat)

    # Primer criteri: guanya qui té més punts amb cobertura suficient.
    max_punts = max(resultat.punts_correctes for resultat in resultats)
    finalistes = [
        resultat for resultat in resultats
        if resultat.punts_correctes == max_punts
    ]

    # Segon criteri: en cas d'empat, guanya el senyal mínim més alt.
    millor_senyal = max(resultat.senyal_minim for resultat in finalistes)
    guanyadores = [
        resultat.nom for resultat in finalistes
        if resultat.senyal_minim == millor_senyal
    ]

    return {
        "llindar": llindar,
        "resultats": resultats,
        "guanyadores": guanyadores
    }
