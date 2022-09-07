import json

from fastapi import status
from fastapi.testclient import TestClient

from src.api.mocks.mock_predict import mock_predict
from src.api.routes.predict import predict

# initialize testclient object class
client = TestClient(predict)

# create mocked test data
SIZE = 10
data_mocked = mock_predict(size=SIZE)

# create manual test data
data_manual = [
    {
        "id": 381110,
        "Gender": "Male",
        "Age": 25,
        "Driving_License": 1,
        "Region_Code": 11.0,
        "Previously_Insured": 1,
        "Vehicle_Age": "< 1 Year",
        "Vehicle_Damage": "Yes",
        "Annual_Premium": 35786.0,
        "Policy_Sales_Channel": 152.0,
        "Vintage": 53,
    },
    {
        "id": 293843,
        "Gender": "Female",
        "Age": 61,
        "Driving_License": 0,
        "Region_Code": 13.0,
        "Previously_Insured": 0,
        "Vehicle_Age": "> 2 Years",
        "Vehicle_Damage": "No",
        "Annual_Premium": 94386.0,
        "Policy_Sales_Channel": 244.0,
        "Vintage": 101,
    },
]


# testing status code
def test_if_status_code_is_equal_200_with_a_single_item() -> None:
    """checks if the response status code is equal to 200 with a single item"""
    response = client.post(url="/", data=json.dumps(data_manual[0]))
    assert response.status_code == status.HTTP_200_OK

    return None


def test_if_status_code_is_equal_200_with_multiple_items() -> None:
    """checks if the response status code is equal to 200 with multiple tems"""
    response = client.post(url="/", data=json.dumps(data_manual))
    assert response.status_code == status.HTTP_200_OK

    return None


def test_if_status_code_is_equal_200_with_multiple_mocked_items() -> None:
    """checks if the response status code is equal to 200 with multiple random items"""
    response = client.post(url="/", data=json.dumps(data_mocked))
    assert response.status_code == status.HTTP_200_OK

    return None


# testing predicted scores
def test_predict_with_a_single_item() -> None:
    """checks the predicted score to a single item"""
    response = client.post(url="/", data=json.dumps(data_manual[0]))
    assert response.json()["381110"] == 0.058194444444444444

    return None


def test_predict_with_multiple_items() -> None:
    """checks the predicted score to multiple items"""
    response = client.post(url="/", data=json.dumps(data_manual))
    assert response.json()["293843"] == 0.26901463886990207
    assert response.json()["381110"] == 0.058194444444444444

    return None


# test response data format
def test_if_json_format_is_equal_to_json() -> None:
    """checks if the response type is a json object"""
    response = client.post(url="/", data=json.dumps(data_mocked))
    assert response.headers["Content-Type"] == "application/json"

    return None
