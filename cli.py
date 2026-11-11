"""Terminal version of the main analysis flow (no extra UI dependency)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from analisi import ErrorAnalisi, comparar_configuracions
from models import Configuracio
from storage import ErrorEmmagatzematge, carregar_dades, guardar_dades

DIRECTORI = Path(__file__).resolve().parent
FITXER_EXEMPLE = DIRECTORI / "data" / "exemple_mesures.json"
FITXER_DADES = DIRECTORI / "data" / "mesures.json"


def obtenir_sessio_interactiva() -> tuple[list[str], float, list[Configuracio]]:
    print("\nASSISTENT PER TRIAR LA UBICACIÓ D'UN REPETIDOR WI-FI")
    punts = []
    for i in range(5):
        nom = input(f"Nom del punt {i + 1}: ").strip()
        while not nom:
            print("El nom no pot estar buit.")
            nom = input(f"Nom del punt {i + 1}: ").strip()
        punts.append(nom)

    llindar_text = input("Llindar RSSI en dBm (ex. -67): ").strip()
    llindar = float(llindar_text.replace(",", "."))

    noms_configuracio = [
        "Router sense repetidor",
        "Repetidor - endoll A",
        "Repetidor - endoll B",
    ]
    configuracions = []
    for nom_configuracio in noms_configuracio:
        print(f"\n{nom_configuracio}")
        mesures = {}
        for punt in punts:
            text = input(f"  RSSI de {punt} (dBm): ").strip()
            mesures[punt] = text
        configuracions.append(Configuracio(nom_configuracio, mesures))
    return punts, llindar, configuracions


def mostrar_resultats(comparacio) -> None:
    print("\nRESULTATS DE LA COMPARACIÓ")
    print(f"Llindar seleccionat: {comparacio.llindar:g} dBm")
    for resultat in comparacio.resultats:
        febles = ", ".join(resultat.punts_febles) if resultat.punts_febles else "cap"
        print(
            f"- {resultat.nom}: {resultat.punts_correctes}/5 punts correctes; "
            f"senyal mínim {resultat.senyal_minim:g} dBm; punts febles: {febles}"
        )
    if comparacio.hi_ha_empat:
        print("\nResultat: empat entre " + ", ".join(comparacio.guanyadores))
    else:
        print("\nConfiguració recomanada: " + comparacio.guanyadores[0])


def carregar_exemple() -> tuple[list[str], float, list[Configuracio]]:
    dades = carregar_dades(FITXER_EXEMPLE)
    configuracions = [
        Configuracio(item["nom"], item["mesures"])
        for item in dades["configuracions"]
    ]
    return dades["punts"], dades["llindar"], configuracions


def main() -> int:
    parser = argparse.ArgumentParser(description="Assistent per triar un repetidor Wi-Fi")
    parser.add_argument(
        "--demo", action="store_true", help="executa l'exemple amb dades sintètiques"
    )
    args = parser.parse_args()

    try:
        if args.demo:
            punts, llindar, configuracions = carregar_exemple()
            print("S'està utilitzant un conjunt de dades sintètiques d'exemple.")
        else:
            punts, llindar, configuracions = obtenir_sessio_interactiva()

        comparacio = comparar_configuracions(configuracions, llindar)
        mostrar_resultats(comparacio)

        if not args.demo:
            resposta = input("\nVols desar les mesures? (s/n): ").strip().lower()
            if resposta == "s":
                guardar_dades(punts, comparacio.llindar, configuracions, FITXER_DADES)
                print(f"Dades desades a {FITXER_DADES}")
        return 0
    except (ErrorAnalisi, ErrorEmmagatzematge, ValueError) as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
