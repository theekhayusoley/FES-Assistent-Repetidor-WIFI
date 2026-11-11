class Configuracio:
    """Representa una configuració de la xarxa Wi-Fi."""

    def __init__(self, nom, mesures):
        self.nom = nom
        self.mesures = mesures


class ResultatConfiguracio:
    """Guarda el resultat de l'anàlisi d'una configuració."""

    def __init__(self, nom, punts_correctes, senyal_minim, punts_febles):
        self.nom = nom
        self.punts_correctes = punts_correctes
        self.senyal_minim = senyal_minim
        self.punts_febles = punts_febles
