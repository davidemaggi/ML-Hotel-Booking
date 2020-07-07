# ML-Hotel-Booking
## Panoramica
Di recente per lavoro mi sono trovato a lavorare con un clientedel mondo **Hotel e Hospitality** e parallelamente ho cominciato un po per lavoro un po per passione ad esplorare il mondo del **Machine Learning** e mi sono chiesto come avrei potuto unire i due mondi.

La domanda ha avuto risposta quando mi sono imbattuto in questo dataset https://www.sciencedirect.com/science/article/pii/S2352340918315191

Certo non sono i dati del cliente, non sono tantissimi, ma mi hanno dato la spinta per esplorare.
In particolare mi intrigava la possibilità di poter prevedere le cancellazioni delle prenotazioni, sarebbe figo per un tour operator o un'hotel poterle prevedere...
Quello che segue è il flusso E2E di questo viaggio.

### Raccolta ed esplorazione dei dati
Ogni Dataset va esplorato, conosciuto e capito, quali dati? quanti dati? come sono fatti? Cosa mi dicono? Cosa mi possono dire? queste sono le domande fontamentali a cui bisogna rispondere, un Dataset scarno o peggio incompreso possono far fallire il progetto ancora prima di nascere.

Questo è il passaggio che porta via generalmente l'80% del tempo in un progetto di ML.

### Il Features Engineering
Una volta che abbiamo recuperato ed analizzato i dati possiamo cominciare a lavolarli per renderli perfetti per il nostro progetto.

#### Dati da rimuvere
- Alcuni dati potrebbero essere fuorvianti
- Alcuni dati potrebbero ridurre il grado di generalizzione

#### Dati Da pulire
- Alcuni dati potrebbero essere mancanti, trovare un buon valore di default è fondamentale
- I dati testuali o categorici possono essere usati in un modello di ML, ma richiedono risorse, e potrebbero ridurre la precisione. Possiamo trasformarli in valori numerici
- Anche i dati numerici possono essere migliorati, o scalati, un modello di ML che lavora con numeri piccoli lo farà in maniera piu efficiente e performante

#### Dati obiettivo
- Quale Dato del nostro set è quello che vogliamo predire? 

### La scelta del modello
La scelta del modello può essere dettata dalla nostra conoscenza del settore e dei dati, ma anche non essendo padroni della materia è possibile verificare empiricamente quale modello puo essere il piu performante. Verificare che uno della miriade di modelli disponibili possa fare al caso nostro è un passo fondamentale da intraprendere prima di pensare a scrivere il nostro modello da zero... anzi... nella stragrande maggioranza dei casi un modello esistente sarà la nostra scelta.

### L'allenamento del modello
Una volta definito il Modello da usare bisogna allenarlo, ed è qui che entra in gioco la potenza, la forza bruta, allenare un modello è la parte piu costosa e pesante per l'infrastruttura. Infatti in un progetto business questa parte viene demandata alla scalabilità del Cloud.

Il nostro Dataset andrà diviso in due parti, in modo da poter usare un subset di dati per l'allenamento e un set di dati per la valutazione, a me piace il classico 70-30.

### La valutazione del modello

Una volta allenato il modello bisogna valutarlo, e per farlo usiamo un set di dati che non ha mai visto, il restante 30 nel nostro caso

### Aggiustare il tiro
Il nostro modello puo funzionare, ma sta funzionando al meglio? dopo averlo allenato e valutato possiamo migliorarlo ancora? un fine tuning degli HyperParameter puo cambiare drrasticamente i risultati.

### Il Deploy in produzione
Una volta che il nostro modello è stato allenato bisogna farlo interagire con il mondo, nel mio caso ho creato una piccola API in Python e un piccolo portale web sempre in python che simula la creazione di una prenotazione, fornndo una previsione sulla cancellazione ed il grado di sicurezza che il modello ha.


### L'allenamento continuo

Questo nel mio esempio non c'è, purtroppo il set di dati è "Morto" ma nella vita reale un modello viene allenato continuamente con dati freschi, nuove versioni del modello vengono versionate e deployate continuamente.

# Come sporcarti le mani
Il Progetto è liberamente scaricabile ed usabile
## Pre-Requisiti
Per questo progetto ho utilizzato Python 3.7.7
```bash
$ python --version
Python 3.7.7
```

Le dipendenze necessarie sono elencate nel file requirements.txt
```bash
$ pip install -r requirements.txt
```

La parte di creazione del modello è disponibile in due formati

## Jupiter Notebook
Un classico, è quello che vi consiglio di usare, contiene passo passo quello che è stato fatto.
[AED Prenotazioni e previsione delle cancellazioni.ipynb](https://github.com/davidemaggi/ML-Hotel-Booking/blob/master/Cancellazioni/AED%20Prenotazioni%20e%20previsione%20delle%20cancellazioni.ipynb)

## Script Python
Una volta che avete letto il notebook potrete usare lo script che contiene solo la parte di creazione e allenamento del modello(nella cartella Cancellazioni), ma non partite da qui, fate il viaggio con me nel Notebook

```bash
$ cd Cancellazioni
$ python cancellazioni.py
```


## Web API & Portale
Una volta che il modello è stato allenato e salvato possiamo lanciare il progetto Flask contenuto nella directory Web
```bash
$ cd Web
$ python app.py
```
Questo renderà disponbile:
-  Un portale all'indirizzo http://localhost:5000 
- una comoda pagina swagger all'indirizzo http://localhost:5000/api/ui
- Potrete comunque usare anche PostMan per interrogare durettamente l'API.
