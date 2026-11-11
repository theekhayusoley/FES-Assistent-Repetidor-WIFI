from pathlib import Path

import flet as ft

from analisi import comparar_configuracions, convertir_rssi
from models import Configuracio
from storage import carregar_dades, guardar_dades

DIRECTORI = Path(__file__).resolve().parent
FITXER_DADES = DIRECTORI / "data" / "mesures.json"

NOMS_CONFIGURACIO = [
    "Router sense repetidor",
    "Repetidor - endoll A",
    "Repetidor - endoll B"
]

PUNTS_PER_DEFECTE = ["Menjador", "Dormitori", "Cuina", "Despatx", "Passadís"]


def main(page: ft.Page):
    page.title = "Assistent Wi-Fi"
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    threshold_field = ft.TextField(label="Llindar mínim (dBm)", value="-67", width=210)
    name_fields = []
    measurement_fields = {}
    cards = []

    for i, nom in enumerate(PUNTS_PER_DEFECTE):
        name_fields.append(
            ft.TextField(label=f"Nom del punt {i + 1}", value=nom, expand=True)
        )

    for point_index in range(5):
        fields_for_point = []

        for config_index, config_name in enumerate(NOMS_CONFIGURACIO):
            field = ft.TextField(
                label=config_name,
                hint_text="Ex. -65",
                width=220
            )
            measurement_fields[(point_index, config_index)] = field
            fields_for_point.append(field)

        cards.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f"Punt de mesura {point_index + 1}",
                            size=17,
                            weight=ft.FontWeight.BOLD
                        ),
                        name_fields[point_index],
                        ft.Column(fields_for_point, spacing=6)
                    ],
                    spacing=8
                ),
                padding=12,
                border=ft.Border.all(1, "#cbd5e1"),
                border_radius=10
            )
        )

    status = ft.Text(
        "Introdueix els noms dels punts, les 15 mesures i el llindar.",
        color="#475569"
    )
    results_panel = ft.Column(spacing=8)

    def recollir_dades():
        punts = []
        for field in name_fields:
            nom = field.value.strip()
            if not nom:
                raise ValueError("Cal introduir el nom dels cinc punts.")
            if nom in punts:
                raise ValueError("Els noms dels punts han de ser diferents.")
            punts.append(nom)

        llindar = convertir_rssi(threshold_field.value, "llindar")
        configuracions = []

        for config_index, config_name in enumerate(NOMS_CONFIGURACIO):
            mesures = {}
            for point_index, punt in enumerate(punts):
                valor = measurement_fields[(point_index, config_index)].value
                mesures[punt] = convertir_rssi(valor, f"{config_name} / {punt}")

            configuracions.append(Configuracio(config_name, mesures))

        return punts, llindar, configuracions

    def analitzar_click(e):
        try:
            punts, llindar, configuracions = recollir_dades()
            comparacio = comparar_configuracions(configuracions, llindar)
            results_panel.controls.clear()

            if len(comparacio["guanyadores"]) > 1:
                recomanacio = "Empat: " + ", ".join(comparacio["guanyadores"])
            else:
                recomanacio = "Configuració recomanada: " + comparacio["guanyadores"][0]

            results_panel.controls.append(
                ft.Text(
                    recomanacio,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="#166534"
                )
            )

            for resultat in comparacio["resultats"]:
                if resultat.punts_febles:
                    punts_febles = ", ".join(resultat.punts_febles)
                else:
                    punts_febles = "Cap"

                results_panel.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(resultat.nom, weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"Punts amb cobertura suficient: {resultat.punts_correctes}/5"),
                                ft.Text(f"Senyal del punt més feble: {resultat.senyal_minim:g} dBm"),
                                ft.Text(f"Punts per sota del llindar: {punts_febles}")
                            ],
                            spacing=4
                        ),
                        padding=10,
                        border=ft.Border.all(1, "#cbd5e1"),
                        border_radius=8
                    )
                )

            status.value = "Anàlisi completada correctament."
            status.color = "#166534"

        except ValueError as error:
            results_panel.controls.clear()
            status.value = str(error)
            status.color = "#b91c1c"

        page.update()

    def desar_click(e):
        try:
            punts, llindar, configuracions = recollir_dades()
            guardar_dades(punts, llindar, configuracions, FITXER_DADES)
            status.value = "Mesures desades correctament."
            status.color = "#166534"
        except (ValueError, OSError) as error:
            status.value = str(error)
            status.color = "#b91c1c"

        page.update()

    def carregar_click(e):
        try:
            dades = carregar_dades(FITXER_DADES)

            if len(dades["punts"]) != 5 or len(dades["configuracions"]) != 3:
                raise ValueError("El fitxer no té cinc punts i tres configuracions.")

            threshold_field.value = str(dades["llindar"])

            for index, punt in enumerate(dades["punts"]):
                name_fields[index].value = str(punt)

            for config_index, configuracio in enumerate(dades["configuracions"]):
                for point_index, punt in enumerate(dades["punts"]):
                    valor = configuracio["mesures"].get(punt, "")
                    measurement_fields[(point_index, config_index)].value = str(valor)

            results_panel.controls.clear()
            status.value = "Mesures carregades correctament."
            status.color = "#166534"

        except (ValueError, KeyError, TypeError, OSError) as error:
            status.value = str(error)
            status.color = "#b91c1c"

        page.update()

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Assistent per triar la ubicació d'un repetidor Wi-Fi",
                    size=25,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Compara el router sol amb dues ubicacions candidates del repetidor. "
                    "Introdueix les mesures RSSI en dBm als mateixos cinc punts i amb el mateix dispositiu."
                ),
                ft.Divider(),
                ft.Text("1. Llindar de cobertura", size=19, weight=ft.FontWeight.BOLD),
                threshold_field,
                ft.Text("2. Mesures de la xarxa", size=19, weight=ft.FontWeight.BOLD),
                *cards,
                ft.Row(
                    [
                        ft.FilledButton("Analitzar cobertura", on_click=analitzar_click),
                        ft.OutlinedButton("Desar mesures", on_click=desar_click),
                        ft.OutlinedButton("Carregar mesures", on_click=carregar_click)
                    ],
                    wrap=True
                ),
                status,
                ft.Divider(),
                ft.Text("3. Resultats", size=19, weight=ft.FontWeight.BOLD),
                results_panel,
                ft.Text(
                    "Nota: RSSI més proper a 0 dBm significa un senyal més fort. "
                    "L'aplicació no mesura el Wi-Fi automàticament; les dades s'introdueixen manualment.",
                    size=12,
                    color="#64748b"
                )
            ],
            spacing=12,
            expand=True
        )
    )


if __name__ == "__main__":
    ft.run(main)
