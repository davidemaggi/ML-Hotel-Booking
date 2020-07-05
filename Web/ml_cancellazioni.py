from datetime import datetime
import joblib
import pandas as pd
from pathlib import Path
import numpy as np



# Create a handler for our read (GET) people


def predict(prenotazione):
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        sorted list of people
    """
    modello = joblib.load("../Trained-Models/cancellazioni.pkl")



    dataArrivo = datetime.strptime(prenotazione["DataPrenotazioneArrivo"], '%m/%d/%Y')
    dataPartenza = datetime.strptime(prenotazione["DataPrenotazionePartenza"], '%m/%d/%Y')
    dataOggi = datetime.today()

    delta = dataArrivo - dataOggi
    
    mesi = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    weekdays = np.busday_count( dataArrivo.date(), dataPartenza.date() )
    deltasoggiorno = dataPartenza - dataArrivo
    weekends=deltasoggiorno.days-weekdays

    data = {
        'lead_time': delta.days, #Automatico, DataPrenotazioneArrivo-Oggi
        'arrival_date_week_number': dataArrivo.isocalendar()[1], # Da DataPrenotazioneArrivo
        'arrival_date_day_of_month': dataArrivo.day, # DataPrenotazioneArrivo
        'stays_in_weekend_nights': deltasoggiorno.days-weekdays, # Da DataPrenotazioneArrivo e DataPrenotazionePartenza
        'stays_in_week_nights': weekdays, # Da DataPrenotazioneArrivo e DataPrenotazionePartenza
        'adults': prenotazione["PrenotazioneAdulti"], # Da PrenotazioneAdulti
        'children': prenotazione["PrenotazioneBambini"], # Da PrenotazioneBambini
        'babies': prenotazione["PrenotazioneInfant"], # Da PrenotazioneInfant
        'is_repeated_guest': 0,
        'previous_cancellations': 0,
        'previous_bookings_not_canceled': 0,
        'agent': 0,
        'company': 0,
        'required_car_parking_spaces': prenotazione["PrenotazionePostiAuto"], # Da PrenotazionePostiAuto
        'total_of_special_requests': prenotazione["PrenotazioneSpeciali"], # Da Somma PrenotazioniSpeciali
       
        'adr': 100, # Da PrenotazioneCamera e PrenotazioneHotel

        'hotel': prenotazione["PrenotazioneHotel"], # PrenotazioneHotel
        'arrival_date_month': mesi[dataArrivo.month-1], # Da DataPrenotazioneArrivo
        'meal': prenotazione["PrenotazioneTrattamento"], # Da PrenotazioneTrattamento
        'market_segment': "Online TA",
        'distribution_channel': "TA/TO",
        'reserved_room_type': prenotazione["PrenotazioneCamera"], # Da PrenotazioneCamera
        'deposit_type': "No Deposit",
        'customer_type': "Transient"
    }

    prenotazionedf = pd.DataFrame([data], columns=data.keys())
    
    prenotazionedf.to_csv('c:/tmp/dataOggi.csv')

    prev= modello.predict(prenotazionedf)
    prob= modello.predict_proba(prenotazionedf)

    print(prev[0])
    print(prob[0][prev[0]])
    

    ret = {
        "previsione": bool(prev[0]),
        "certezza": float(prob[0][prev[0]]),

    }

    

    # Create the list of people from our data
    return ret

