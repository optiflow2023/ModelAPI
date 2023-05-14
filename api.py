import pathlib

import pandas as pd
from fastapi import FastAPI
from joblib import load
from pydantic import BaseModel

model_path = pathlib.Path(__file__).parent / "model.pkl"


class ModelData(BaseModel):
    date: str


app = FastAPI(
    title="HP Inventory Forecasting API",
    description="API for the HP Supply Chain forecasting challenge",
    version="1.0",
)

model = None


@app.on_event("startup")
def load_model():
    global model
    model = load(model_path)


@app.post("/predict", tags=["predictions"])
def get_prediction(model_data: ModelData):

    try:
        date = pd.to_datetime(model_data.date).week

        model_cutoff = pd.to_datetime("2022-05-06").week

        week_diff = abs(model_cutoff - date)

        prediction = model.predict(week_diff)
        print(prediction)

        prediction["date"] = pd.to_datetime(prediction["date"])
        prediction["year"] = prediction["date"].dt.year
        prediction["week"] = prediction["date"].dt.week

        prediction["id"] = (
            prediction["year"].astype(str)
            + prediction["week"].astype(str)
            + "-"
            + prediction["product_number"].astype(str)
        )

        prediction = prediction.rename(columns={"CatBoostRegressor": "prediction"})
        prediction = prediction[["id", "prediction"]]

        prediction = prediction.set_index("id").to_dict()

        return {
            "prediction": prediction,
        }
    except Exception as e:
        print(e)
        return {"prediction": "Invalid date"}
