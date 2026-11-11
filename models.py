"""Models for the Wi-Fi repeater placement assistant."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Configuracio:
    """One Wi-Fi setup and the RSSI readings measured at five locations."""

    nom: str
    mesures: Dict[str, float] = field(default_factory=dict)


@dataclass
class ResultatConfiguracio:
    """Coverage analysis for one Wi-Fi setup."""

    nom: str
    punts_correctes: int
    senyal_minim: float
    punts_febles: List[str] = field(default_factory=list)


@dataclass
class ResultatComparacio:
    """Comparison of all candidate setups."""

    llindar: float
    resultats: List[ResultatConfiguracio]
    guanyadores: List[str]

    @property
    def hi_ha_empat(self) -> bool:
        return len(self.guanyadores) > 1
