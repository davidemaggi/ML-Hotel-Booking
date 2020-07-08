from datetime import datetime
import joblib
import pandas as pd
from pathlib import Path
import numpy as np
import random





def predict(prenotazione):
    
    #Carichiamo il modello salvato
    modello = joblib.load("../Trained-Models/cancellazioni_final.pkl")


    # Trasformiamo le date da stringhe a Date
    dataArrivo = datetime.strptime(prenotazione["DataPrenotazioneArrivo"], '%d/%m/%Y')
    dataPartenza = datetime.strptime(prenotazione["DataPrenotazionePartenza"], '%d/%m/%Y')
    # Ci serve anche la data di oggi, è l data di prenotazione
    dataOggi = datetime.today()

    # Calcoliamo il leadTime
    delta = dataArrivo - dataOggi
    
    mesi = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Contiamo i Weekdays
    weekdays = np.busday_count( dataArrivo.date(), dataPartenza.date() )
    # Calcoliamo la durata del soggiorno
    deltasoggiorno = dataPartenza - dataArrivo
    # Calcoliamo il numero dei giorni del weekend sottraendo dalla durata il numero di weekdays
    weekends=deltasoggiorno.days-weekdays

    #Costruiamo il pacchetto da passare al nostro modello, se il modello è stato allenato con X caratterstiche, quelle stesse X caratteristiche dovranno essere usate in fase di previsione

    data = {
        'lead_time': delta.days, 
        'arrival_date_week_number': dataArrivo.isocalendar()[1],
        'arrival_date_day_of_month': dataArrivo.day, 
        'stays_in_weekend_nights': weekends, 
        'stays_in_week_nights': weekdays, 
        'adults': prenotazione["PrenotazioneAdulti"],
        'children': prenotazione["PrenotazioneBambini"],
        'babies': prenotazione["PrenotazioneInfant"],
        'is_repeated_guest': 0,
        'previous_cancellations': 0,
        'previous_bookings_not_canceled': 0,
        'agent': 0,
        'company': 0,
        'required_car_parking_spaces': prenotazione["PrenotazionePostiAuto"],
        'total_of_special_requests': prenotazione["PrenotazioneSpeciali"], 
       
        'adr': prenotazione["PrenotazionePrezzo"], 

        'hotel': prenotazione["PrenotazioneHotel"], 
        'arrival_date_month': mesi[dataArrivo.month-1], 
        'meal': prenotazione["PrenotazioneTrattamento"],
        'market_segment': "Online TA",
        'distribution_channel': "TA/TO",
        'reserved_room_type': prenotazione["PrenotazioneCamera"], 
        'customer_type': prenotazione["PrenotazioneTipoCliente"]
    }

    # Trasformo questo oggetto in un Dataframe Pandas
    prenotazionedf = pd.DataFrame([data], columns=data.keys())
    

    # Faccio prima una previsione
    prev= modello.predict(prenotazionedf)

    # e poi chiedo il grado di certezza avrei potuto fare solo questa chiamata, che ritorna il grado di certezza per ogni possibilità, ma volevo fare vedere entrambe le chiamate
    prob= modello.predict_proba(prenotazionedf)

 
    # costruisco il mio oggetto JSON di ritorno

    ret = {
        "previsione": bool(prev[0]),
        "certezza": float(prob[0][prev[0]]),

    }

    
    # Lo ritorno
 
    return ret

