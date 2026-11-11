import unittest

from analisi import comparar_configuracions, convertir_rssi
from models import Configuracio


class TestAnalisi(unittest.TestCase):
    def setUp(self):
        self.punts = ["Menjador", "Dormitori", "Cuina", "Despatx", "Passadis"]

    def crear_configuracio(self, nom, valors):
        mesures = dict(zip(self.punts, valors))
        return Configuracio(nom, mesures)

    def test_guanya_configuracio_amb_mes_punts_correctes(self):
        configuracions = [
            self.crear_configuracio("Router", [-50, -80, -80, -80, -80]),
            self.crear_configuracio("Endoll A", [-50, -60, -60, -60, -80]),
            self.crear_configuracio("Endoll B", [-50, -80, -80, -80, -80])
        ]
        resultat = comparar_configuracions(configuracions, -67)
        self.assertEqual(resultat["guanyadores"], ["Endoll A"])

    def test_desempat_amb_el_punt_mes_feble(self):
        configuracions = [
            self.crear_configuracio("Router", [-50, -60, -60, -60, -90]),
            self.crear_configuracio("Endoll A", [-50, -60, -60, -60, -75]),
            self.crear_configuracio("Endoll B", [-50, -60, -60, -60, -80])
        ]
        resultat = comparar_configuracions(configuracions, -67)
        self.assertEqual(resultat["guanyadores"], ["Endoll A"])

    def test_empate_final(self):
        mesures = [-50, -60, -60, -60, -80]
        configuracions = [
            self.crear_configuracio("Router", mesures),
            self.crear_configuracio("Endoll A", mesures),
            self.crear_configuracio("Endoll B", [-50, -65, -65, -65, -85])
        ]
        resultat = comparar_configuracions(configuracions, -67)
        self.assertEqual(set(resultat["guanyadores"]), {"Router", "Endoll A"})

    def test_falten_mesures(self):
        configuracions = [
            self.crear_configuracio("Router", [-50, -60, -60, -60, -80]),
            Configuracio("Endoll A", {"Menjador": -50}),
            self.crear_configuracio("Endoll B", [-50, -60, -60, -60, -80])
        ]
        with self.assertRaises(ValueError):
            comparar_configuracions(configuracions, -67)

    def test_valor_rssi_incorrecte(self):
        with self.assertRaises(ValueError):
            convertir_rssi("no és un número")
        with self.assertRaises(ValueError):
            convertir_rssi(-130)

    def test_accepta_coma_decimal(self):
        self.assertEqual(convertir_rssi("-65,5"), -65.5)

    def test_llindar_incorrecte(self):
        configuracions = [
            self.crear_configuracio("Router", [-50, -60, -60, -60, -80]),
            self.crear_configuracio("Endoll A", [-50, -60, -60, -60, -80]),
            self.crear_configuracio("Endoll B", [-50, -60, -60, -60, -80])
        ]
        with self.assertRaises(ValueError):
            comparar_configuracions(configuracions, "")

    def test_punts_diferents(self):
        configuracions = [
            self.crear_configuracio("Router", [-50, -60, -60, -60, -80]),
            Configuracio("Endoll A", {"A": -50, "B": -60, "C": -60, "D": -60, "E": -80}),
            self.crear_configuracio("Endoll B", [-50, -60, -60, -60, -80])
        ]
        with self.assertRaises(ValueError):
            comparar_configuracions(configuracions, -67)


if __name__ == "__main__":
    unittest.main()
