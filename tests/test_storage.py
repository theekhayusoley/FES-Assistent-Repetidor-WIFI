import json
import tempfile
import unittest
from pathlib import Path

from models import Configuracio
from storage import ErrorEmmagatzematge, carregar_dades, guardar_dades


class TestStorage(unittest.TestCase):
    def test_desar_i_carregar(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "subdir" / "mesures.json"
            configuracions = [
                Configuracio("Router", {"Sala": -50, "Dormitori": -60, "Cuina": -70, "Despatx": -80, "Passadis": -65}),
                Configuracio("Endoll A", {"Sala": -50, "Dormitori": -60, "Cuina": -70, "Despatx": -80, "Passadis": -65}),
                Configuracio("Endoll B", {"Sala": -50, "Dormitori": -60, "Cuina": -70, "Despatx": -80, "Passadis": -65}),
            ]
            guardar_dades(["Sala", "Dormitori", "Cuina", "Despatx", "Passadis"], -67, configuracions, path)
            dades = carregar_dades(path)
            self.assertEqual(dades["llindar"], -67.0)
            self.assertEqual(len(dades["configuracions"]), 3)
            self.assertEqual(dades["configuracions"][0]["mesures"]["Sala"], -50)

    def test_fitxer_inexistent(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ErrorEmmagatzematge):
                carregar_dades(Path(tmp) / "no_existeix.json")

    def test_json_corromput(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dades.json"
            path.write_text("{ no és json", encoding="utf-8")
            with self.assertRaises(ErrorEmmagatzematge):
                carregar_dades(path)


if __name__ == "__main__":
    unittest.main()
