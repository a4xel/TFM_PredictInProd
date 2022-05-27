from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime
import pytz
import os
from google.cloud import storage
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

model = joblib.load("my_new_model")


@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(pickup_datetime,pickup_longitude,pickup_latitude,
            dropoff_longitude, dropoff_latitude,passenger_count):

    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

    key=str("2013-07-06 17:18:00.000000119")
    longitude = float(pickup_longitude)
    latitude = float(pickup_latitude)
    drop_long = float(dropoff_longitude)
    drop_lat = float(dropoff_latitude)
    count = int(passenger_count)

    X_pred = {
        "key": key,
        "pickup_datetime": formatted_pickup_datetime,
        "pickup_longitude": longitude,
        "pickup_latitude": latitude,
        "dropoff_longitude": drop_long,
        "dropoff_latitude": drop_lat,
        "passenger_count": count
    }

    X_pred_df = pd.DataFrame(X_pred,index=[0])

    #client = storage.Client()

    #bucket = client.bucket("wagon-data-864-lechanteur")

    #blob = bucket.blob("models/taxifare/v2/model.joblib")

    #blob.download_to_filename("my_new_model")

    #model = joblib.load("my_new_model")

    model = joblib.load("my_new_model")

    fare = model.predict(X_pred_df)

    return {"predicted_fare": fare[0]}
