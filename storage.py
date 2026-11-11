import json
from pathlib import Path


def guardar_dades(punts, llindar, configuracions, ruta):
    """Desa les mesures en un fitxer JSON."""
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

    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as fitxer:
        json.dump(dades, fitxer, ensure_ascii=False, indent=4)


def carregar_dades(ruta):
    """Llegeix les mesures guardades en un fitxer JSON."""
    ruta = Path(ruta)

    try:
        with open(ruta, "r", encoding="utf-8") as fitxer:
            dades = json.load(fitxer)
    except FileNotFoundError:
        raise ValueError("No s'ha trobat el fitxer de mesures.")
    except json.JSONDecodeError:
        raise ValueError("El fitxer de mesures no conté un JSON vàlid.")

    if "punts" not in dades or "llindar" not in dades or "configuracions" not in dades:
        raise ValueError("El fitxer no conté totes les dades necessàries.")

    return dades
