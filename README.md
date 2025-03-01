# Convertitore di Immagini in SVG

Questo progetto offre uno strumento per convertire immagini raster (JPG, PNG, WEBP, ecc.) in formato vettoriale SVG utilizzando la libreria Potrace. Include sia un'interfaccia a riga di comando che un'interfaccia grafica basata su Streamlit.

## Funzionalità

- Conversione di immagini raster in formato vettoriale SVG
- Interfaccia web interattiva con Streamlit
- Anteprima dell'immagine originale, binaria e del risultato SVG
- Regolazione dei parametri di conversione (soglia e sfocatura)
- Conversione batch di tutte le immagini in una cartella
- Supporto per vari formati di immagine (JPG, PNG, WEBP, BMP, GIF, TIFF)

## Requisiti di Sistema

- Python 3.7 o superiore
- Potrace (prerequisito per pypotrace)
- Librerie Python (installate automaticamente con i comandi di installazione)

## Installazione

### Windows

1. Assicurati di avere Python installato. Puoi scaricarlo da [python.org](https://www.python.org/downloads/)

2. Installa Potrace (prerequisito per pypotrace):
   - Scarica il binario di Potrace per Windows da [potrace.sourceforge.net](http://potrace.sourceforge.net/#downloading)
   - Estrai il file ZIP e aggiungi la cartella bin al PATH di sistema

3. Clona o scarica questo repository:
   ```
   git clone https://github.com/tuonome/SvgConverter.git
   cd SvgConverter
   ```

4. Crea un ambiente virtuale (opzionale ma consigliato):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

5. Installa le dipendenze:
   ```
   pip install -r requirements.txt
   ```

### WSL (Windows Subsystem for Linux)

1. Assicurati di avere WSL installato e configurato con una distribuzione Linux

2. Installa Python, Potrace e le librerie necessarie:
   ```
   sudo apt update
   sudo apt install python3 python3-pip python3-venv libgl1-mesa-glx potrace libpotrace-dev
   ```

3. Clona o scarica questo repository:
   ```
   git clone https://github.com/tuonome/SvgConverter.git
   cd SvgConverter
   ```

4. Crea un ambiente virtuale (opzionale ma consigliato):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

5. Installa le dipendenze:
   ```
   pip install -r requirements.txt
   ```

### macOS

1. Assicurati di avere Python e Potrace installati. Puoi usare Homebrew:
   ```
   brew install python potrace
   ```

2. Clona o scarica questo repository:
   ```
   git clone https://github.com/tuonome/SvgConverter.git
   cd SvgConverter
   ```

3. Crea un ambiente virtuale (opzionale ma consigliato):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Installa le dipendenze:
   ```
   pip install -r requirements.txt
   ```

## Utilizzo

### Interfaccia Web (Streamlit)

1. Avvia l'applicazione Streamlit:
   ```
   python -m streamlit run app.py
   ```

2. Apri il browser all'indirizzo indicato (di solito http://localhost:8501)

3. Utilizza l'interfaccia per:
   - Caricare un'immagine
   - Regolare i parametri di conversione nella barra laterale
   - Visualizzare l'anteprima dell'immagine originale, binaria e SVG
   - Scaricare il file SVG risultante
   - Eseguire la conversione batch di tutte le immagini nella cartella "Images/ToConvert"

### Riga di Comando

Il programma può essere utilizzato anche da riga di comando:

```
python main.py [opzioni]
```

Opzioni disponibili:
- `-i, --input`: Percorso dell'immagine da convertire
- `-o, --output`: Percorso di output per il file SVG
- `-t, --threshold`: Valore soglia per la binarizzazione (0-255, default: 100)
- `-b, --blur`: Dimensione kernel per sfocatura (default: 5)
- `-p, --preview`: Mostra anteprima dell'immagine binarizzata
- `-a, --all`: Converti tutte le immagini da Images/ToConvert a Images/Converted

Esempi:
```
# Converti una singola immagine
python main.py -i immagine.jpg -o risultato.svg

# Converti con parametri personalizzati
python main.py -i immagine.jpg -t 150 -b 3

# Converti tutte le immagini nella cartella Images/ToConvert
python main.py --all
```

## Struttura delle Cartelle

- `main.py`: Script principale per la conversione da riga di comando
- `app.py`: Interfaccia web Streamlit
- `requirements.txt`: Dipendenze Python
- `Images/ToConvert`: Cartella per le immagini da convertire in batch
- `Images/Converted`: Cartella dove vengono salvati i file SVG convertiti
- `temp`: Cartella temporanea per le immagini caricate tramite l'interfaccia web

## Risoluzione dei Problemi

### Errore "libGL.so.1: cannot open shared object file"

Su Linux o WSL, potrebbe essere necessario installare le librerie OpenGL:
```
sudo apt update
sudo apt install libgl1-mesa-glx
```

### Problemi con pypotrace

#### Errore durante l'installazione di pypotrace

Se riscontri problemi con l'installazione di pypotrace, assicurati di avere gli strumenti di sviluppo necessari e il pacchetto potrace installato:

Su Linux/WSL:
```
sudo apt install build-essential python3-dev libpotrace-dev potrace
```

Su macOS:
```
brew install potrace
```

Su Windows:
1. Assicurati che Potrace sia installato e nel PATH di sistema
2. Se l'installazione di pypotrace fallisce, prova a installare le Visual C++ Build Tools:
   - Scarica e installa [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Durante l'installazione, seleziona "C++ build tools"

#### Errore "ImportError: No module named potrace"

Questo errore può verificarsi se pypotrace non è stato installato correttamente. Prova a reinstallare:
```
pip uninstall pypotrace
pip install pypotrace
```

Se il problema persiste, verifica che potrace sia installato correttamente nel sistema.

#### Errore "AttributeError" con pypotrace

Se riscontri errori come "AttributeError" quando usi pypotrace, potrebbe essere dovuto a incompatibilità tra la versione di pypotrace e la versione di potrace installata. Prova a:

1. Aggiornare potrace alla versione più recente
2. Reinstallare pypotrace dopo aver aggiornato potrace
3. Verificare la documentazione di pypotrace per assicurarti di usare l'API correttamente

## Parametri di Conversione

### Soglia di binarizzazione
Determina quali pixel diventano bianchi o neri.
- Valori più bassi: più dettagli ma più rumore
- Valori più alti: meno dettagli ma più pulito

### Dimensione kernel sfocatura
Controlla quanto viene sfocata l'immagine prima della conversione.
- Valori più bassi: mantiene più dettagli fini
- Valori più alti: rimuove più rumore ma può perdere dettagli

## Licenza

MIT License

Copyright (c) 2025 Danilo Zito

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contatti

Per domande o suggerimenti, contattare:
- GitHub: [danilozito](https://github.com/danilozito) 