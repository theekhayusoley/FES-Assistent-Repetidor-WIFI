# Assistent per triar la ubicació d'un repetidor Wi-Fi

## Versió beta L3

Aquesta és una primera versió executable del projecte. Permet provar el funcionament principal: introduir les mesures RSSI, comparar les tres configuracions i veure quina ofereix millor cobertura.

## Què es pot fer en aquesta beta?

- Introduir els noms de cinc punts de mesura.
- Introduir les quinze mesures RSSI en dBm.
- Escollir el llindar mínim de senyal.
- Comparar el router sense repetidor amb dues ubicacions candidates del repetidor.
- Veure quants punts compleixen el llindar i quins punts tenen un senyal més feble.
- Obtenir una recomanació. Si hi ha empat en el nombre de punts correctes, es compara el senyal del punt més feble.

Les mesures s'obtenen amb una eina externa i s'introdueixen manualment. L'aplicació no mesura el Wi-Fi automàticament.

## Requisits

- Python 3.10 o superior.
- Flet 1.1.2.

## Executar amb Visual Studio Code (Windows)

1. Obre aquesta carpeta amb Visual Studio Code.
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

## Proves inicials

Executa les proves amb:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Les proves comproven la selecció de la configuració amb més punts correctes, el desempat pel punt més feble, l'empat final i la detecció de dades incompletes o incorrectes.

## Estructura

- `main.py`: interfície gràfica amb Flet.
- `models.py`: classes per representar les configuracions i els resultats.
- `analisi.py`: validació de les mesures i algoritme de comparació.
- `tests/`: proves inicials de l'algoritme.
- `requirements.txt`: biblioteca necessària per a la interfície.

## Dificultats trobades

La principal dificultat és interpretar correctament els valors RSSI, ja que són negatius i els valors més propers a zero indiquen un senyal més fort. També cal comprovar que totes les configuracions continguin mesures dels mateixos cinc punts i que no falti cap dada.

## Feina pendent després de la beta

- Afegir el desament i la recuperació de mesures amb fitxers JSON.
- Provar el desament i la recuperació des de la interfície.
- Fer proves amb mesures reals d'un habitatge.
- Comprovar l'ús de l'aplicació des del navegador d'un mòbil.
- Revisar possibles errors i millorar la presentació dels resultats.

Aquesta beta només implementa el flux principal de comparació. Les funcions de desament i càrrega formen part de la feina pendent i s'incorporaran en una versió posterior.
