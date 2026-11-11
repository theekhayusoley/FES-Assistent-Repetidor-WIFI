import os
import tempfile
import unittest

from models import Configuracio
from storage import carregar_dades, guardar_dades


class TestStorage(unittest.TestCase):
    def test_desar_i_carregar(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "mesures.json")
            punts = ["Sala", "Dormitori", "Cuina", "Despatx", "Passadis"]
            configuracions = [
                Configuracio("Router", {"Sala": -50, "Dormitori": -60, "Cuina": -70, "Despatx": -80, "Passadis": -65}),
                Configuracio("Endoll A", {"Sala": -51, "Dormitori": -61, "Cuina": -71, "Despatx": -81, "Passadis": -66}),
                Configuracio("Endoll B", {"Sala": -52, "Dormitori": -62, "Cuina": -72, "Despatx": -82, "Passadis": -67})
            ]

            guardar_dades(punts, -67, configuracions, ruta)
            dades = carregar_dades(ruta)

            self.assertEqual(dades["llindar"], -67)
            self.assertEqual(len(dades["configuracions"]), 3)
            self.assertEqual(dades["configuracions"][0]["mesures"]["Sala"], -50)

    def test_fitxer_inexistent(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "no_existeix.json")
            with self.assertRaises(ValueError):
                carregar_dades(ruta)

    def test_json_incorrecte(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "mesures.json")
            with open(ruta, "w", encoding="utf-8") as fitxer:
                fitxer.write("{ no és json")
            with self.assertRaises(ValueError):
                carregar_dades(ruta)

    def test_estructura_incorrecta(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "mesures.json")
            with open(ruta, "w", encoding="utf-8") as fitxer:
                fitxer.write('{"punts": [], "llindar": -67, "configuracions": []}')
            with self.assertRaises(ValueError):
                carregar_dades(ruta)


if __name__ == "__main__":
    unittest.main()
