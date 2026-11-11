import json


def guardar_dades(punts, llindar, configuracions, ruta):
    """Desa els noms, el llindar i les mesures en un fitxer JSON."""
    dades = {
        "punts": punts,
        "llindar": llindar,
        "configuracions": []
    }

    for configuracio in configuracions:
        dades["configuracions"].append({
            "nom": configuracio.nom,
            "mesures": configuracio.mesures
        })

    with open(ruta, "w", encoding="utf-8") as fitxer:
        json.dump(dades, fitxer, ensure_ascii=False, indent=4)


def carregar_dades(ruta):
    """Carrega les dades d'un fitxer JSON i en comprova l'estructura."""
    try:
        with open(ruta, "r", encoding="utf-8") as fitxer:
            dades = json.load(fitxer)
    except FileNotFoundError:
        raise ValueError("No s'ha trobat el fitxer de mesures.")
    except json.JSONDecodeError:
        raise ValueError("El fitxer de mesures no conté un JSON vàlid.")

    if not isinstance(dades, dict):
        raise ValueError("El contingut del fitxer no és correcte.")

    if "punts" not in dades or "llindar" not in dades or "configuracions" not in dades:
        raise ValueError("El fitxer no conté totes les dades necessàries.")

    if not isinstance(dades["punts"], list) or len(dades["punts"]) != 5:
        raise ValueError("El fitxer ha de contenir cinc punts de mesura.")

    if not isinstance(dades["configuracions"], list) or len(dades["configuracions"]) != 3:
        raise ValueError("El fitxer ha de contenir tres configuracions.")

    for configuracio in dades["configuracions"]:
        if not isinstance(configuracio, dict):
            raise ValueError("Una configuració del fitxer no és correcta.")

        if "nom" not in configuracio or "mesures" not in configuracio:
            raise ValueError("Falten dades d'una configuració.")

        if not isinstance(configuracio["mesures"], dict):
            raise ValueError("Les mesures del fitxer no són correctes.")

        if len(configuracio["mesures"]) != 5:
            raise ValueError("Cada configuració ha de tenir cinc mesures.")

    return dades
