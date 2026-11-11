"""Flet interface for the Wi-Fi repeater placement assistant."""

from __future__ import annotations

from pathlib import Path

try:
    import flet as ft
except ImportError as exc:  # friendly message when dependencies are missing
    raise SystemExit(
        "Flet no està instal·lat. Executa 'python -m pip install -r requirements.txt'."
    ) from exc

from analisi import ErrorAnalisi, comparar_configuracions, convertir_rssi
from models import Configuracio
from storage import ErrorEmmagatzematge, carregar_dades, guardar_dades

DIRECTORI = Path(__file__).resolve().parent
FITXER_DADES = DIRECTORI / "data" / "mesures.json"
NOMS_CONFIGURACIO = [
    "Router sense repetidor",
    "Repetidor - endoll A",
    "Repetidor - endoll B",
]
PUNTS_PER_DEFECTE = ["Menjador", "Dormitori", "Cuina", "Despatx", "Passadís"]


def main(page: ft.Page) -> None:
    page.title = "Assistent Wi-Fi"
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    threshold_field = ft.TextField(label="Llindar mínim (dBm)", value="-67", width=210)
    name_fields = [
        ft.TextField(label=f"Nom del punt {i + 1}", value=nom, expand=True)
        for i, nom in enumerate(PUNTS_PER_DEFECTE)
    ]
    measurement_fields: dict[tuple[int, int], ft.TextField] = {}
    cards = []

    for point_index in range(5):
        fields_for_point = []
        for config_index, config_name in enumerate(NOMS_CONFIGURACIO):
            field = ft.TextField(
                label=config_name,
                hint_text="Ex. -65",
                width=220,
            )
            measurement_fields[(point_index, config_index)] = field
            fields_for_point.append(field)
        cards.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Punt de mesura {point_index + 1}", size=17, weight=ft.FontWeight.BOLD),
                        name_fields[point_index],
                        ft.Column(fields_for_point, spacing=6),
                    ],
                    spacing=8,
                ),
                padding=12,
                border=ft.Border.all(1, "#cbd5e1"),
                border_radius=10,
            )
        )

    status = ft.Text("Introdueix els noms dels punts, les 15 mesures i el llindar.", color="#475569")
    results_panel = ft.Column(spacing=8)

    def collect_data():
        points = [field.value.strip() for field in name_fields]
        if any(not point for point in points):
            raise ErrorAnalisi("Cal introduir el nom dels cinc punts de mesura.")
        if len(set(points)) != 5:
            raise ErrorAnalisi("Els noms dels cinc punts han de ser diferents.")

        threshold = convertir_rssi(threshold_field.value, "llindar")
        configurations = []
        for config_index, config_name in enumerate(NOMS_CONFIGURACIO):
            readings = {}
            for point_index, point in enumerate(points):
                field = measurement_fields[(point_index, config_index)]
                readings[point] = convertir_rssi(
                    field.value,
                    f"{config_name} / {point}",
                )
            configurations.append(Configuracio(config_name, readings))
        return points, threshold, configurations

    def analyse_click(_event):
        try:
            _points, threshold, configurations = collect_data()
            comparison = comparar_configuracions(configurations, threshold)
            results_panel.controls.clear()
            for result in comparison.resultats:
                weak_points = ", ".join(result.punts_febles) if result.punts_febles else "Cap"
                results_panel.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(result.nom, weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"Punts amb cobertura suficient: {result.punts_correctes}/5"),
                                ft.Text(f"Senyal del punt més feble: {result.senyal_minim:g} dBm"),
                                ft.Text(f"Punts per sota del llindar: {weak_points}"),
                            ],
                            spacing=4,
                        ),
                        padding=10,
                        border=ft.Border.all(1, "#cbd5e1"),
                        border_radius=8,
                    )
                )
            if comparison.hi_ha_empat:
                recommendation = "Empat: " + ", ".join(comparison.guanyadores)
            else:
                recommendation = "Configuració recomanada: " + comparison.guanyadores[0]
            results_panel.controls.insert(
                0,
                ft.Text(recommendation, size=18, weight=ft.FontWeight.BOLD, color="#166534"),
            )
            status.value = "Anàlisi completada correctament."
            status.color = "#166534"
        except (ErrorAnalisi, ValueError) as exc:
            results_panel.controls.clear()
            status.value = str(exc)
            status.color = "#b91c1c"
        page.update()

    def save_click(_event):
        try:
            points, threshold, configurations = collect_data()
            guardar_dades(points, threshold, configurations, FITXER_DADES)
            status.value = f"Mesures desades a {FITXER_DADES.name}."
            status.color = "#166534"
        except (ErrorAnalisi, ErrorEmmagatzematge, ValueError) as exc:
            status.value = str(exc)
            status.color = "#b91c1c"
        page.update()

    def load_click(_event):
        try:
            data = carregar_dades(FITXER_DADES)
            if len(data["punts"]) != 5 or len(data["configuracions"]) != 3:
                raise ErrorEmmagatzematge("El fitxer no correspon a l'estructura de cinc punts i tres configuracions.")
            threshold_field.value = str(data["llindar"])
            for index, point in enumerate(data["punts"]):
                name_fields[index].value = str(point)
            for config_index, config in enumerate(data["configuracions"]):
                readings = config.get("mesures", {})
                for point_index, point in enumerate(data["punts"]):
                    measurement_fields[(point_index, config_index)].value = str(readings.get(point, ""))
            results_panel.controls.clear()
            status.value = "Mesures carregades correctament."
            status.color = "#166534"
        except (ErrorEmmagatzematge, KeyError, TypeError) as exc:
            status.value = str(exc)
            status.color = "#b91c1c"
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text("Assistent per triar la ubicació d'un repetidor Wi-Fi", size=25, weight=ft.FontWeight.BOLD),
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
                        ft.FilledButton("Analitzar cobertura", on_click=analyse_click),
                        ft.OutlinedButton("Desar mesures", on_click=save_click),
                        ft.OutlinedButton("Carregar mesures", on_click=load_click),
                    ],
                    wrap=True,
                ),
                status,
                ft.Divider(),
                ft.Text("3. Resultats", size=19, weight=ft.FontWeight.BOLD),
                results_panel,
                ft.Text(
                    "Nota: RSSI més proper a 0 dBm significa un senyal més fort. "
                    "L'aplicació no mesura el Wi-Fi automàticament; les dades s'introdueixen manualment.",
                    size=12,
                    color="#64748b",
                ),
            ],
            spacing=12,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
