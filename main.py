import flet as ft

from analisi import comparar_configuracions, convertir_rssi
from models import Configuracio
from storage import carregar_dades, guardar_dades

NOMS_CONFIGURACIO = [
    "Router sense repetidor",
    "Repetidor - endoll A",
    "Repetidor - endoll B"
]

PUNTS_PER_DEFECTE = ["Menjador", "Dormitori", "Cuina", "Despatx", "Passadís"]
FITXER_DADES = "mesures.json"


def main(page):
    page.title = "Assistent Wi-Fi"
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    camp_llindar = ft.TextField(label="Llindar mínim (dBm)", value="-67", width=210)
    camps_punts = []
    camps_mesures = []
    targetes = []

    for i in range(5):
        camp = ft.TextField(
            label="Nom del punt " + str(i + 1),
            value=PUNTS_PER_DEFECTE[i],
            expand=True
        )
        camps_punts.append(camp)

    for i in range(5):
        camps_configuracio = []

        for j in range(3):
            camp = ft.TextField(
                label=NOMS_CONFIGURACIO[j],
                hint_text="Ex. -65",
                width=220
            )
            camps_configuracio.append(camp)

        camps_mesures.append(camps_configuracio)

        targetes.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Punt de mesura " + str(i + 1), weight=ft.FontWeight.BOLD),
                        camps_punts[i],
                        ft.Column(camps_configuracio, spacing=6)
                    ],
                    spacing=8
                ),
                padding=12,
                border=ft.Border.all(1, "#cbd5e1"),
                border_radius=10
            )
        )

    missatge = ft.Text("Introdueix els noms dels punts, les 15 mesures i el llindar.")
    resultats = ft.Column(spacing=8)

    def recollir_dades():
        punts = []

        for i in range(5):
            nom = camps_punts[i].value.strip()

            if nom == "":
                raise ValueError("Cal escriure el nom dels cinc punts.")

            if nom in punts:
                raise ValueError("Els noms dels punts han de ser diferents.")

            punts.append(nom)

        llindar = convertir_rssi(camp_llindar.value, "llindar")
        configuracions = []

        for j in range(3):
            mesures = {}

            for i in range(5):
                valor = camps_mesures[i][j].value
                nom_camp = NOMS_CONFIGURACIO[j] + " / " + punts[i]
                mesures[punts[i]] = convertir_rssi(valor, nom_camp)

            configuracions.append(Configuracio(NOMS_CONFIGURACIO[j], mesures))

        return punts, llindar, configuracions

    def analitzar_click(e):
        try:
            punts, llindar, configuracions = recollir_dades()
            comparacio = comparar_configuracions(configuracions, llindar)
            resultats.controls.clear()

            if len(comparacio["guanyadores"]) == 1:
                recomanacio = "Configuració recomanada: " + comparacio["guanyadores"][0]
            else:
                recomanacio = "Empat entre: " + ", ".join(comparacio["guanyadores"])

            resultats.controls.append(
                ft.Text(recomanacio, size=18, weight=ft.FontWeight.BOLD)
            )

            for resultat in comparacio["resultats"]:
                if len(resultat.punts_febles) > 0:
                    febles = ", ".join(resultat.punts_febles)
                else:
                    febles = "Cap"

                resultats.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(resultat.nom, weight=ft.FontWeight.BOLD, size=16),
                                ft.Text("Cobertura suficient: " + str(resultat.punts_correctes) + "/5 punts"),
                                ft.Text("Senyal del punt més feble: " + str(resultat.senyal_minim) + " dBm"),
                                ft.Text("Punts per sota del llindar: " + febles)
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

    def desar_click(e):
        try:
            punts, llindar, configuracions = recollir_dades()
            guardar_dades(punts, llindar, configuracions, FITXER_DADES)
            missatge.value = "Mesures desades correctament a " + FITXER_DADES + "."
            missatge.color = "#166534"
        except (ValueError, OSError) as error:
            missatge.value = str(error)
            missatge.color = "#b91c1c"

        page.update()

    def carregar_click(e):
        try:
            dades = carregar_dades(FITXER_DADES)
            punts = []

            for i in range(5):
                nom = dades["punts"][i]
                if not isinstance(nom, str) or nom.strip() == "":
                    raise ValueError("El nom d'un punt del fitxer no és correcte.")
                if nom in punts:
                    raise ValueError("El fitxer conté noms de punts repetits.")
                punts.append(nom)

            llindar = convertir_rssi(dades["llindar"], "llindar")
            configuracions = []

            for j in range(3):
                dades_configuracio = dades["configuracions"][j]
                mesures = {}

                for i in range(5):
                    punt = punts[i]
                    if punt not in dades_configuracio["mesures"]:
                        raise ValueError("Al fitxer falta una mesura del punt " + punt + ".")
                    valor = convertir_rssi(
                        dades_configuracio["mesures"][punt],
                        NOMS_CONFIGURACIO[j] + " / " + punt
                    )
                    mesures[punt] = valor

                configuracions.append(Configuracio(NOMS_CONFIGURACIO[j], mesures))

            camp_llindar.value = str(llindar)

            for i in range(5):
                camps_punts[i].value = punts[i]

            for j in range(3):
                for i in range(5):
                    camps_mesures[i][j].value = str(configuracions[j].mesures[punts[i]])

            resultats.controls.clear()
            missatge.value = "Mesures carregades correctament."
            missatge.color = "#166534"

        except (ValueError, OSError, KeyError, TypeError, IndexError) as error:
            missatge.value = str(error)
            missatge.color = "#b91c1c"

        page.update()

    elements = [
        ft.Text(
            "Assistent per triar la ubicació d'un repetidor Wi-Fi",
            size=24,
            weight=ft.FontWeight.BOLD
        ),
        ft.Text(
            "Compara el router sol amb dues ubicacions candidates del repetidor. "
            "Introdueix les mesures RSSI en dBm als mateixos cinc punts i amb el mateix dispositiu."
        ),
        ft.Divider(),
        ft.Text("1. Llindar de cobertura", size=18, weight=ft.FontWeight.BOLD),
        camp_llindar,
        ft.Text("2. Mesures de la xarxa", size=18, weight=ft.FontWeight.BOLD)
    ]

    for targeta in targetes:
        elements.append(targeta)

    elements.append(
        ft.Row(
            [
                ft.FilledButton("Analitzar cobertura", on_click=analitzar_click),
                ft.OutlinedButton("Desar mesures", on_click=desar_click),
                ft.OutlinedButton("Carregar mesures", on_click=carregar_click)
            ],
            wrap=True
        )
    )
    elements.append(missatge)
    elements.append(ft.Divider())
    elements.append(ft.Text("3. Resultats", size=18, weight=ft.FontWeight.BOLD))
    elements.append(resultats)
    elements.append(
        ft.Text(
            "Les mesures s'introdueixen manualment. Un valor RSSI més proper a 0 dBm indica un senyal més fort.",
            size=12,
            color="#64748b"
        )
    )

    page.add(ft.Column(elements, spacing=12))


if __name__ == "__main__":
    ft.run(main)
