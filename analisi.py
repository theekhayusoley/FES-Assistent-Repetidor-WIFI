from models import Configuracio, ResultatConfiguracio

NUM_PUNTS = 5
NUM_CONFIGURACIONS = 3


def convertir_rssi(valor, nom_camp="RSSI"):
    """Converteix una entrada a un valor RSSI vàlid."""
    try:
        numero = float(str(valor).strip().replace(",", "."))
    except ValueError:
        raise ValueError("El valor de " + nom_camp + " no és un número vàlid.")

    if numero < -120 or numero > 0 or numero != numero:
        raise ValueError("El valor de " + nom_camp + " ha d'estar entre -120 i 0 dBm.")

    return numero


def validar_configuracions(configuracions):
    """Comprova que hi hagi tres configuracions amb els mateixos cinc punts."""
    if len(configuracions) != NUM_CONFIGURACIONS:
        raise ValueError("Cal introduir exactament tres configuracions.")

    punts_referencia = []
    for punt in configuracions[0].mesures:
        punts_referencia.append(punt)

    configuracions_valides = []

    for configuracio in configuracions:
        if len(configuracio.mesures) != NUM_PUNTS:
            raise ValueError("Cada configuració ha de tenir cinc mesures.")

        for punt in punts_referencia:
            if punt not in configuracio.mesures:
                raise ValueError("Les tres configuracions han de tenir els mateixos cinc punts.")

        for punt in configuracio.mesures:
            if punt not in punts_referencia:
                raise ValueError("Les tres configuracions han de tenir els mateixos cinc punts.")

        mesures_valides = {}
        for punt in configuracio.mesures:
            valor = convertir_rssi(configuracio.mesures[punt], punt)
            mesures_valides[punt] = valor

        configuracions_valides.append(
            Configuracio(configuracio.nom, mesures_valides)
        )

    return configuracions_valides


def analitzar_configuracio(configuracio, llindar):
    """Compta els punts amb cobertura suficient i busca el senyal més feble."""
    punts_febles = []
    senyal_minim = None

    for punt in configuracio.mesures:
        valor = configuracio.mesures[punt]

        if valor < llindar:
            punts_febles.append(punt)

        if senyal_minim is None or valor < senyal_minim:
            senyal_minim = valor

    punts_correctes = NUM_PUNTS - len(punts_febles)

    return ResultatConfiguracio(
        configuracio.nom,
        punts_correctes,
        senyal_minim,
        punts_febles
    )


def comparar_configuracions(configuracions, llindar):
    """Compara les tres configuracions segons els dos criteris del projecte."""
    llindar = convertir_rssi(llindar, "llindar")
    configuracions = validar_configuracions(configuracions)

    resultats = []
    for configuracio in configuracions:
        resultat = analitzar_configuracio(configuracio, llindar)
        resultats.append(resultat)

    # Primer criteri: nombre de punts que compleixen el llindar.
    max_punts = resultats[0].punts_correctes
    for resultat in resultats:
        if resultat.punts_correctes > max_punts:
            max_punts = resultat.punts_correctes

    finalistes = []
    for resultat in resultats:
        if resultat.punts_correctes == max_punts:
            finalistes.append(resultat)

    # Segon criteri: valor més alt del punt més feble.
    millor_senyal = finalistes[0].senyal_minim
    for resultat in finalistes:
        if resultat.senyal_minim > millor_senyal:
            millor_senyal = resultat.senyal_minim

    guanyadores = []
    for resultat in finalistes:
        if resultat.senyal_minim == millor_senyal:
            guanyadores.append(resultat.nom)

    return {
        "llindar": llindar,
        "resultats": resultats,
        "guanyadores": guanyadores
    }
