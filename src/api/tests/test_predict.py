from fastapi.testclient import TestClient
from src.api.mocks import mock_predict
from src.api.routes.predict import predict
import json

# initialize testclient object class
client = TestClient(predict)

# create mocked test data
size = 10
data_mocked = mock_predict(size=size)

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


def test_predict_with_single_item() -> None:
    """makes a request with a single item"""
    response = client.post(url="/", data=json.dumps(data_manual[0]))

    assert response.status_code == 200
    assert response.json()["293843"] == 0.26901463886990207

    return None


def test_predict_with_list_of_items() -> None:
    """makes a request with multiple items"""
    response = client.post(url="/", data=json.dumps(data_manual))

    assert response.status_code == 200
    assert response.json()["293843"] == 0.26901463886990207
    assert response.json()["381110"] == 0.058194444444444444

    return None


def test_predict_random_mock_data() -> None:
    """makes a request with random items"""
    response = client.post(url="/", data=json.dumps(data_mocked))

    assert response.status_code == 200
    assert len(response.json()) == size
    assert list(response.json().keys())[0] == data_mocked[0]["id"]

    return None
