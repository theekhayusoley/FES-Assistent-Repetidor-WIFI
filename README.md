# Assistent per triar la ubicació d'un repetidor Wi-Fi

Aplicació en Python amb Flet per comparar tres configuracions Wi-Fi a partir de mesures RSSI introduïdes manualment en cinc punts d'un habitatge.

## Funcionament

1. Escriu un llindar mínim de cobertura en dBm.
2. Introdueix els noms dels cinc punts de mesura.
3. Introdueix les quinze mesures RSSI: cinc per al router sense repetidor, cinc per al repetidor a l'endoll A i cinc per al repetidor a l'endoll B.
4. Prem **Analitzar cobertura** per veure els resultats i la configuració recomanada.
5. Fes servir **Desar mesures** i **Carregar mesures** per guardar o recuperar les dades en un fitxer JSON.

Les mesures s'obtenen amb una eina externa d'anàlisi Wi-Fi i s'introdueixen manualment. Cal utilitzar el mateix dispositiu als mateixos cinc punts per comparar les configuracions. L'aplicació no mesura el Wi-Fi automàticament.

## Criteris de comparació

- Primer es compten els punts que igualen o superen el llindar RSSI.
- Guanya la configuració que compleix el llindar en més punts.
- Si hi ha un empat, es compara el valor RSSI del punt més feble. Guanya el valor més alt, és a dir, el més proper a zero.
- Si continua l'empat, es mostren totes les configuracions empatades.

Els valors RSSI vàlids per a l'aplicació van de -120 a 0 dBm.

## Requisits

- Python 3.10 o superior.
- Flet 1.1.2.

## Executar amb Visual Studio Code (Windows)

1. Obre la carpeta del projecte amb Visual Studio Code.
2. Obre el terminal: **Terminal > New Terminal**.
3. Crea l'entorn virtual:

```powershell
python -m venv .venv
```

4. Instal·la Flet:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

5. Executa l'aplicació:

```powershell
.\.venv\Scripts\flet.exe run main.py
```

Quan desis les mesures, es crearà el fitxer `mesures.json` a la carpeta del projecte.

## Proves

Executa les proves automatitzades amb:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Les proves comproven els dos criteris de comparació, els empats, les dades incorrectes i el desament i la càrrega JSON.

## Estructura del projecte

- `main.py`: interfície gràfica i accions dels botons.
- `models.py`: classes per representar les configuracions i els resultats.
- `analisi.py`: validació de les mesures i algoritme de comparació.
- `storage.py`: desament i càrrega de dades JSON.
- `tests/`: proves automatitzades amb `unittest`.
- `requirements.txt`: biblioteca necessària per a la interfície.

## Limitacions

- Es comparen cinc punts i tres configuracions fixes.
- Les mesures s'introdueixen manualment.
- S'utilitza un únic llindar per a les tres configuracions.
- Només s'avalua el nivell RSSI; no es mesuren velocitat, latència ni interferències.
