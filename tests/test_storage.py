import tempfile
import unittest
from pathlib import Path

from models import Configuracio
from storage import carregar_dades, guardar_dades


class TestStorage(unittest.TestCase):
    def test_desar_i_carregar(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "mesures.json"
            punts = ["Sala", "Dormitori", "Cuina", "Despatx", "Passadis"]
            configuracions = [
                Configuracio("Router", dict(zip(punts, [-50, -60, -70, -80, -65]))),
                Configuracio("Endoll A", dict(zip(punts, [-50, -60, -70, -80, -65]))),
                Configuracio("Endoll B", dict(zip(punts, [-50, -60, -70, -80, -65])))
            ]

            guardar_dades(punts, -67, configuracions, ruta)
            dades = carregar_dades(ruta)

            self.assertEqual(dades["llindar"], -67)
            self.assertEqual(len(dades["configuracions"]), 3)
            self.assertEqual(dades["configuracions"][0]["mesures"]["Sala"], -50)

    def test_fitxer_inexistent(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "no_existeix.json"
            with self.assertRaises(ValueError):
                carregar_dades(ruta)

    def test_json_incorrecte(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "mesures.json"
            ruta.write_text("{ no és json", encoding="utf-8")
            with self.assertRaises(ValueError):
                carregar_dades(ruta)


if __name__ == "__main__":
    unittest.main()
