# Setup

# Warnings

import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

# Un pò di import generici:
import pandas as pd
import numpy as np


# Importiamo scikit-learn:
from sklearn.model_selection import train_test_split, ShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

import joblib # Per esportare il modello



def main():
    # load data:
    file_path = "../Data/HotelBooking.csv"
    set_intero = pd.read_csv(file_path)
    
    
    # Caratteristiche numeriche
    car_numeriche = ["lead_time","arrival_date_week_number","arrival_date_day_of_month",
                    "stays_in_weekend_nights","stays_in_week_nights","adults","children",
                    "babies","is_repeated_guest", "previous_cancellations",
                    "previous_bookings_not_canceled","agent","company",
                    "required_car_parking_spaces", "total_of_special_requests", "adr"]
    
    # Caratteristiche categoriche
    car_categorie = ["hotel","arrival_date_month","meal","market_segment",
                    "distribution_channel","reserved_room_type","deposit_type","customer_type"]
    
    # Separiamo le caratteristiche e gli obiettivi
    caratteristiche = car_numeriche + car_categorie
    set_caratteristiche = set_intero.drop(["is_canceled"], axis=1)[caratteristiche] # Togliamo is_canceled e teniamo le caratteristiche desiderate
    set_obiettivo = set_intero["is_canceled"] # teniamo solo il nostro obiettibo
    
    # Prima di procedere puliamo i dati(come abbiamo visto nella parte di analisi):
    # Per le caratteristiche numeriche usiamo il valore di Default 0.
    
    
    trans_numeriche = Pipeline(steps=[
        ("scale", StandardScaler()),
        ("impute", SimpleImputer(strategy="constant", fill_value=0)),
        ])
    
    # Per le categoriche, visto che parliamo di stringe useremo il valore di default "Unknown" :
    trans_categorie = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
        ("onehot", OneHotEncoder(handle_unknown='ignore')),
        ])
    
    # Applichiamo le modifiche:
    preprocessor = ColumnTransformer(transformers=[("num", trans_numeriche, car_numeriche),
                                                   ("cat", trans_categorie, car_categorie)])
    
    random_forest = RandomForestClassifier(n_estimators=160,
                                   max_features=0.4,
                                   min_samples_split=2,
                                   n_jobs=-1,
                                   random_state=0)
    
    modello_migliore = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('model', random_forest)])
    
    modello_migliore.fit(set_caratteristiche, set_obiettivo)
    # Salviamo il modello sul disco
    joblib.dump(modello_migliore, '../Trained-Models/cancellazioni.pkl')




if __name__ == "__main__":
    main()