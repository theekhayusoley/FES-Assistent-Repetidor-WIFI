import flet as ft

from analisi import comparar_configuracions, convertir_rssi
from models import Configuracio

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

    llindar = ft.TextField(label="Llindar mínim (dBm)", value="-67", width=210)
    camps_punts = []
    camps_mesures = []
    targetes = []

    for i in range(5):
        camps_punts.append(
            ft.TextField(
                label=f"Nom del punt {i + 1}",
                value=PUNTS_PER_DEFECTE[i],
                expand=True
            )
        )

    for i in range(5):
        camps_configuracio = []

        for j in range(3):
            nom_configuracio = NOMS_CONFIGURACIO[j]
            camp = ft.TextField(label=nom_configuracio, hint_text="Ex. -65")
            camps_configuracio.append(camp)

        camps_mesures.append(camps_configuracio)

        targetes.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Punt de mesura {i + 1}", weight=ft.FontWeight.BOLD),
                        camps_punts[i],
                        ft.Column(camps_configuracio)
                    ],
                    spacing=8
                ),
                padding=12,
                border=ft.Border.all(1, "#cbd5e1"),
                border_radius=10
            )
        )

    missatge = ft.Text("Introdueix les 15 mesures per comparar la cobertura.")
    resultats = ft.Column(spacing=8)

    def recollir_dades():
        punts = []

        for camp in camps_punts:
            nom = camp.value.strip()

            if not nom:
                raise ValueError("Cal escriure el nom dels cinc punts.")

            if nom in punts:
                raise ValueError("Els noms dels punts han de ser diferents.")

            punts.append(nom)

        valor_llindar = convertir_rssi(llindar.value, "llindar")
        configuracions = []

        for j in range(3):
            nom_configuracio = NOMS_CONFIGURACIO[j]
            mesures = {}

            for i in range(5):
                punt = punts[i]
                valor = camps_mesures[i][j].value
                mesures[punt] = convertir_rssi(valor, punt)

            configuracions.append(Configuracio(nom_configuracio, mesures))

        return valor_llindar, configuracions

    def analitzar_click(e):
        try:
            valor_llindar, configuracions = recollir_dades()
            comparacio = comparar_configuracions(configuracions, valor_llindar)

            resultats.controls.clear()

            if len(comparacio["guanyadores"]) == 1:
                text_recomanacio = "Configuració recomanada: " + comparacio["guanyadores"][0]
            else:
                text_recomanacio = "Empat entre: " + ", ".join(comparacio["guanyadores"])

            resultats.controls.append(
                ft.Text(text_recomanacio, size=18, weight=ft.FontWeight.BOLD)
            )

            for resultat in comparacio["resultats"]:
                if resultat.punts_febles:
                    febles = ", ".join(resultat.punts_febles)
                else:
                    febles = "Cap"

                resultats.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(resultat.nom, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Cobertura suficient: {resultat.punts_correctes}/5 punts"),
                                ft.Text(f"Senyal del punt més feble: {resultat.senyal_minim:g} dBm"),
                                ft.Text(f"Punts per sota del llindar: {febles}")
                            ],
                            spacing=4
                        ),
                        padding=10,
                        border=ft.Border.all(1, "#cbd5e1"),
                        border_radius=8
                    )
                )

            missatge.value = "Anàlisi completada correctament."
            missatge.color = "#166534"

        except ValueError as error:
            resultats.controls.clear()
            missatge.value = str(error)
            missatge.color = "#b91c1c"

        page.update()

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Assistent per triar la ubicació d'un repetidor Wi-Fi",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Introdueix les mesures RSSI dels mateixos cinc punts "
                    "per a les tres configuracions."
                ),
                ft.Divider(),
                ft.Text("1. Llindar de cobertura", size=18, weight=ft.FontWeight.BOLD),
                llindar,
                ft.Text("2. Mesures de la xarxa", size=18, weight=ft.FontWeight.BOLD),
                *targetes,
                ft.FilledButton("Analitzar cobertura", on_click=analitzar_click),
                missatge,
                ft.Divider(),
                ft.Text("3. Resultats", size=18, weight=ft.FontWeight.BOLD),
                resultats,
                ft.Text(
                    "Les mesures s'introdueixen manualment. "
                    "Un valor RSSI més proper a 0 dBm indica un senyal més fort.",
                    size=12,
                    color="#64748b"
                )
            ],
            spacing=12
        )
    )


if __name__ == "__main__":
    ft.run(main)
