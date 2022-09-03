# imports
from typing import List, Type
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pandas as pd
from src.pipeline.main import Pipeline


# initialize fastapi class object
predict = APIRouter()

# initialize pipeline object class
pipeline = Pipeline()


# record structure input
class Item(BaseModel):
    id: int
    Gender: str
    Age: int
    Driving_License: int
    Region_Code: float
    Previously_Insured: int
    Vehicle_Age: str
    Vehicle_Damage: str
    Annual_Premium: float
    Policy_Sales_Channel: float
    Vintage: int


# create predict endpoint
@predict.post("/")
async def get_prediction(item: Item | List[Item]) -> Type[JSONResponse]:
    """
    makes a prediction of a certain item.

    :param item: informations to be predicted.
    :returns ok status and a json with the predicted data.
    """
    # check data format
    if isinstance(item, list):
        df_raw = pd.DataFrame()
        for i in range(0, len(item)):
            new_item = pd.DataFrame(jsonable_encoder(item[i].dict()), index=[0])
            df_raw = pd.concat([df_raw, new_item])
    else:
        df_raw = pd.DataFrame(item.dict(), columns=item.dict().keys(), index=[0])

    # data pipeline
    df = pipeline.data_preprocessing(
        pipeline.feature_engineering(pipeline.data_cleaning(df_raw))
    )

    # predict
    predicted_data = pipeline.get_prediction(df_raw, df)

    content = {}
    if isinstance(predicted_data, list):
        for i in predicted_data:
            content[i["id"]] = i["score"]

        return JSONResponse(status_code=200, content=content)
    else:
        return JSONResponse(
            status_code=200, content={predicted_data["id"]: predicted_data["score"]}
        )
