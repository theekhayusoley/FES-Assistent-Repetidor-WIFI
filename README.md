# Assistent per triar la ubicació d'un repetidor Wi-Fi

Aplicació en Python amb Flet per comparar tres configuracions Wi-Fi a partir de mesures RSSI introduïdes manualment en cinc punts d'un habitatge.

## Què fa l'aplicació?

1. Permet introduir cinc punts de mesura i un llindar RSSI.
2. Recull cinc mesures per a cadascuna de les tres configuracions: router sol, repetidor a l'endoll A i repetidor a l'endoll B.
3. Compta quants punts arriben al llindar.
4. En cas d'empat, compara el senyal del punt més feble.
5. Mostra la configuració recomanada i els punts amb cobertura insuficient.
6. Permet desar i carregar les mesures en un fitxer JSON.

Les mesures s'obtenen amb una eina externa d'anàlisi Wi-Fi i s'introdueixen manualment. L'aplicació no mesura el senyal automàticament.

## Requisits

- Python 3.10 o superior.
- Flet 1.1.2.

## Obrir i executar amb Visual Studio Code (Windows)

1. Obre la carpeta del projecte amb Visual Studio Code.
2. Obre el terminal integrat: **Terminal > New Terminal**.
3. Crea l'entorn virtual:

```powershell
python -m venv .venv
```

4. Instal·la Flet dins de l'entorn virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

5. Executa l'aplicació:

```powershell
.\.venv\Scripts\flet.exe run main.py
```

## Proves

Per executar les proves automatitzades:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Estructura del projecte

- `main.py`: interfície gràfica amb Flet.
- `models.py`: classes de les configuracions i dels resultats.
- `analisi.py`: validació de les mesures i comparació de cobertura.
- `storage.py`: desament i càrrega de dades JSON.
- `data/`: fitxer amb mesures d'exemple.
- `tests/`: proves de l'algoritme i de l'emmagatzematge.

## Estat de la versió beta

La interfície gràfica s'ha executat correctament i s'ha comprovat el flux principal d'introducció de mesures i comparació de les tres configuracions amb dades d'exemple. Les proves automatitzades de l'algoritme i de l'emmagatzematge també s'han executat correctament.

Queda pendent provar el desament i la recuperació des de la interfície amb una sessió completa i fer mesures reals en un habitatge.

## Limitacions

- Es comparen cinc punts i tres configuracions fixes.
- Les mesures s'introdueixen manualment.
- S'utilitza un únic llindar per a les tres configuracions.
- Només s'avalua el nivell RSSI; no es mesuren velocitat, latència ni interferències.
