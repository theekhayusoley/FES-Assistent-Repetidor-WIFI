# Assistent per triar la ubicació d'un repetidor Wi-Fi

Versió beta (L3) d'un MVP per comparar tres configuracions Wi-Fi a partir de mesures RSSI introduïdes manualment en cinc punts d'un habitatge.

## Funcionalitat principal

1. L'usuari introdueix cinc punts de mesura i el llindar RSSI en dBm.
2. Introdueix cinc mesures per a cadascuna de les tres configuracions: router sense repetidor, repetidor a l'endoll A i repetidor a l'endoll B.
3. El programa valida les dades i compta quants punts arriben al llindar.
4. En cas d'empat, compara el senyal del punt més feble.
5. Mostra la configuració recomanada o les opcions equivalents i identifica els punts febles.
6. Les dades es poden desar i recuperar en format JSON mitjançant la interfície gràfica.

**Important:** el programa no mesura el Wi-Fi automàticament. Les mesures s'obtenen amb una eina externa i s'introdueixen manualment, tal com es va definir a L1.

## Requisits

- Python 3.10 o superior.
- Flet 1.1.2 per executar la interfície gràfica.

## Instal·lació

Des de la carpeta del projecte:

```bash
python -m venv .venv
```

Activació de l'entorn:

- Windows PowerShell: `\.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Instal·lació de dependències:

```bash
python -m pip install -r requirements.txt
```

## Execució de la versió beta

### Interfície gràfica Flet

```bash
flet run main.py
```

Per executar-la al navegador:

```bash
flet run --web --host 0.0.0.0 --port 8550 main.py
```

Per obrir-la des del mòbil, connecta'l a la mateixa xarxa local que l'ordinador i visita `http://IP_LOCAL_DE_L_ORDINADOR:8550`.

### Flux funcional des del terminal

No necessita Flet. Per executar un exemple amb dades sintètiques:

```bash
python cli.py --demo
```

Per introduir les mesures manualment:

```bash
python cli.py
```

L'exemple és sintètic i no representa mesures reals d'un habitatge.

## Proves automatitzades

```bash
python -m unittest discover -s tests -v
```

Les proves cobreixen la selecció de la configuració amb més punts correctes, el desempat pel punt més feble, l'empat final, les mesures incompletes, els valors RSSI incorrectes, la coma decimal i la lectura/escriptura JSON.

## Estructura

- `main.py`: interfície gràfica Flet.
- `cli.py`: flux funcional des del terminal.
- `models.py`: classes `Configuracio`, `ResultatConfiguracio` i `ResultatComparacio`.
- `analisi.py`: validació i algoritme de comparació.
- `storage.py`: emmagatzematge en JSON.
- `tests/`: proves automatitzades.
- `data/exemple_mesures.json`: dades sintètiques per a la demostració.

## Estat de validació de la beta

- Algoritme de comparació i validació: verificat amb proves automatitzades.
- Emmagatzematge JSON: verificat amb proves automatitzades.
- Flux de terminal: executat amb dades sintètiques i amb entrada manual.
- Interfície gràfica Flet: implementada al codi, però pendent de validació visual i funcional en un ordinador amb Flet instal·lat.
- Mesures reals de l'habitatge: pendents.

## Limitacions actuals

- Es comparen cinc punts i tres configuracions fixes.
- Les mesures s'introdueixen manualment.
- S'utilitza un únic llindar configurable per a totes les configuracions.
- Només s'avalua el nivell RSSI; no es mesuren velocitat, latència, jitter ni interferències.
