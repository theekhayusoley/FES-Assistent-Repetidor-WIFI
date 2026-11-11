import unittest

from analisi import ErrorAnalisi, comparar_configuracions, convertir_rssi
from models import Configuracio


class TestAnalisi(unittest.TestCase):
    def setUp(self):
        self.punts = ["Menjador", "Dormitori", "Cuina", "Despatx", "Passadis"]

    def crear_config(self, nom, valors):
        return Configuracio(nom, dict(zip(self.punts, valors)))

    def test_guanya_configuracio_amb_mes_punts_correctes(self):
        configuracions = [
            self.crear_config("Router", [-50, -80, -80, -80, -80]),
            self.crear_config("Endoll A", [-50, -60, -60, -60, -80]),
            self.crear_config("Endoll B", [-50, -80, -80, -80, -80]),
        ]
        resultat = comparar_configuracions(configuracions, -67)
        self.assertEqual(resultat.guanyadores, ["Endoll A"])
        self.assertEqual(resultat.resultats[1].punts_correctes, 4)

    def test_desempat_amb_senyal_mes_feble(self):
        configuracions = [
            self.crear_config("Router", [-50, -60, -60, -60, -90]),
            self.crear_config("Endoll A", [-50, -60, -60, -60, -75]),
            self.crear_config("Endoll B", [-50, -60, -60, -60, -80]),
        ]
        resultat = comparar_configuracions(configuracions, -67)
        self.assertEqual(resultat.guanyadores, ["Endoll A"])
        self.assertFalse(resultat.hi_ha_empat)

    def test_empate_final_mostra_dues_configuracions(self):
        mesures = [-50, -60, -60, -60, -80]
        configuracions = [
            self.crear_config("Router", mesures),
            self.crear_config("Endoll A", mesures),
            self.crear_config("Endoll B", [-50, -65, -65, -65, -85]),
        ]
        resultat = comparar_configuracions(configuracions, -67)
        self.assertEqual(set(resultat.guanyadores), {"Router", "Endoll A"})
        self.assertTrue(resultat.hi_ha_empat)

    def test_falten_mesures(self):
        configuracions = [
            self.crear_config("Router", [-50, -60, -60, -60, -80]),
            Configuracio("Endoll A", {"Menjador": -50}),
            self.crear_config("Endoll B", [-50, -60, -60, -60, -80]),
        ]
        with self.assertRaises(ErrorAnalisi):
            comparar_configuracions(configuracions, -67)

    def test_valor_rssi_incorrecte(self):
        with self.assertRaises(ErrorAnalisi):
            convertir_rssi("no és un número")
        with self.assertRaises(ErrorAnalisi):
            convertir_rssi(-130)

    def test_accepta_coma_decimal(self):
        self.assertEqual(convertir_rssi("-65,5"), -65.5)

    def test_llindar_incorrecte(self):
        configuracions = [
            self.crear_config("Router", [-50, -60, -60, -60, -80]),
            self.crear_config("Endoll A", [-50, -60, -60, -60, -80]),
            self.crear_config("Endoll B", [-50, -60, -60, -60, -80]),
        ]
        with self.assertRaises(ErrorAnalisi):
            comparar_configuracions(configuracions, "")

    def test_punts_no_coincidents(self):
        configuracions = [
            self.crear_config("Router", [-50, -60, -60, -60, -80]),
            Configuracio("Endoll A", {"A": -50, "B": -60, "C": -60, "D": -60, "E": -80}),
            self.crear_config("Endoll B", [-50, -60, -60, -60, -80]),
        ]
        with self.assertRaises(ErrorAnalisi):
            comparar_configuracions(configuracions, -67)


if __name__ == "__main__":
    unittest.main()
