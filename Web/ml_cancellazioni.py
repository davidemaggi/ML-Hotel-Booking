from datetime import datetime
import joblib
import pandas as pd
from pathlib import Path




# Create a handler for our read (GET) people


def predict(prenotazione):
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        sorted list of people
    """
    modello = joblib.load("../Trained-Models/cancellazioni.pkl")


    data = {
        'lead_time': 0,
        'arrival_date_week_number': 0,
        'arrival_date_day_of_month': 0,
        'stays_in_weekend_nights': 0,
        'stays_in_week_nights': 0,
        'adults': 0,
        'children': 0,
        'babies': 0,
        'is_repeated_guest': 0,
        'previous_cancellations': 0,
        'previous_bookings_not_canceled': 0,
        'agent': 0,
        'required_car_parking_spaces': 0,
        'total_of_special_requests': 0,
        'company': 0,
        'adr': 0,

        'hotel': "",
        'arrival_date_month': "",
        'meal': "",
        'market_segment': "",
        'distribution_channel': "",
        'reserved_room_type': "",
        'deposit_type': "",
        'customer_type': ""
    }

    prenotazione = pd.DataFrame([data], columns=data.keys())

    

    prev= modello.predict(prenotazione)
    prob= modello.predict_proba(prenotazione)

    print(prev[0])
    print(prob[0][prev[0]])
    

    ret = {
        "previsione": bool(prev[0]),
        "certezza": float(prob[0][prev[0]]),

    }

    

    # Create the list of people from our data
    return ret

