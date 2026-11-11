"""JSON persistence for Wi-Fi measurements."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from models import Configuracio


class ErrorEmmagatzematge(ValueError):
    """Raised when a measurement file cannot be read or written."""


def guardar_dades(
    punts: Iterable[str],
    llindar: float,
    configuracions: Iterable[Configuracio],
    ruta: str | Path,
) -> None:
    """Save a complete measurement session as UTF-8 JSON, atomically."""
    path = Path(ruta)
    dades = {
        "versio": 1,
        "desat_utc": datetime.now(timezone.utc).isoformat(),
        "punts": list(punts),
        "llindar": float(llindar),
        "configuracions": [
            {"nom": c.nom, "mesures": c.mesures} for c in configuracions
        ],
    }

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporal = path.with_suffix(path.suffix + ".tmp")
        with temporal.open("w", encoding="utf-8") as fitxer:
            json.dump(dades, fitxer, ensure_ascii=False, indent=2, allow_nan=False)
            fitxer.write("\n")
        os.replace(temporal, path)
    except (OSError, TypeError, ValueError) as exc:
        raise ErrorEmmagatzematge(f"No s'han pogut desar les dades: {exc}") from exc


def carregar_dades(ruta: str | Path) -> dict[str, Any]:
    """Load a previously saved session and check its top-level structure."""
    path = Path(ruta)
    try:
        with path.open("r", encoding="utf-8") as fitxer:
            dades = json.load(fitxer)
    except FileNotFoundError:
        raise ErrorEmmagatzematge(f"No existeix el fitxer de dades: {path}") from None
    except json.JSONDecodeError as exc:
        raise ErrorEmmagatzematge(
            f"El fitxer JSON està mal format (línia {exc.lineno})."
        ) from exc
    except OSError as exc:
        raise ErrorEmmagatzematge(f"No s'han pogut llegir les dades: {exc}") from exc

    if not isinstance(dades, dict):
        raise ErrorEmmagatzematge("El contingut del fitxer JSON no és vàlid.")
    camps = {"punts", "llindar", "configuracions"}
    if not camps.issubset(dades):
        raise ErrorEmmagatzematge("El fitxer JSON no conté tots els camps necessaris.")
    if not isinstance(dades["punts"], list) or not isinstance(
        dades["configuracions"], list
    ):
        raise ErrorEmmagatzematge("L'estructura de les dades guardades no és vàlida.")
    return dades
