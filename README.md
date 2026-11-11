# Assistent per triar la ubicació d'un repetidor Wi-Fi

Versió beta (L3) d'una aplicació en Python per comparar tres configuracions Wi-Fi a partir de mesures RSSI introduïdes manualment en cinc punts d'un habitatge.

## Funcionalitat principal

1. L'usuari introdueix els noms de cinc punts de mesura i el llindar RSSI en dBm.
2. Introdueix les cinc mesures de cadascuna de les tres configuracions: router sense repetidor, repetidor a l'endoll A i repetidor a l'endoll B.
3. L'aplicació valida les dades i compta quants punts arriben al llindar.
4. En cas d'empat, compara el senyal del punt més feble.
5. Mostra la configuració recomanada i identifica els punts amb cobertura insuficient.
6. Permet desar i recuperar les mesures en format JSON.

Les mesures s'obtenen amb una eina externa d'anàlisi Wi-Fi i s'introdueixen manualment. L'aplicació no mesura el senyal automàticament.

## Requisits

- Python 3.10 o superior.
- Flet 1.1.2.

## Obrir el projecte amb Visual Studio Code

Obre a Visual Studio Code la carpeta que conté aquest README i els fitxers `main.py`, `models.py` i `analisi.py`.

Obre el terminal integrat de Visual Studio Code (Terminal > New Terminal) i executa les ordres següents des de la carpeta del projecte.

### Instal·lació (Windows / PowerShell)

Crear l'entorn virtual:

```powershell
python -m venv .venv
```

Instal·lar les dependències sense necessitat d'activar l'entorn virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Executar l'aplicació

```powershell
.\.venv\Scripts\flet.exe run main.py
```

### Executar les proves

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Estructura del projecte

- `main.py`: interfície gràfica de l'aplicació amb Flet.
- `models.py`: classes per representar les configuracions i els resultats.
- `analisi.py`: validació de mesures i algoritme de comparació.
- `storage.py`: desar i recuperar dades amb JSON.
- `data/exemple_mesures.json`: dades d'exemple per fer una demostració.
- `tests/`: proves automatitzades.

## Estat de la versió beta

La interfície gràfica s'ha executat correctament i s'ha comprovat el flux principal d'introducció de mesures i comparació de les tres configuracions amb dades d'exemple. Les proves automatitzades de l'algoritme i de l'emmagatzematge també s'han executat correctament.

Queda pendent provar el desament i la recuperació des de la interfície amb una sessió completa i fer mesures reals en un habitatge.

## Limitacions

- Es comparen cinc punts i tres configuracions fixes.
- Les mesures s'introdueixen manualment.
- S'utilitza un únic llindar configurable per a les tres configuracions.
- Només s'avalua el nivell RSSI; no es mesuren la velocitat, la latència ni les interferències.
