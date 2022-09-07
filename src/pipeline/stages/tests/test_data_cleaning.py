import pandas as pd
import pytest

from src.api.mocks.mock_predict import mock_predict
from src.pipeline.stages.data_cleaning import data_cleaning_main

# generate fake data
SIZE = 10
data_mocked = mock_predict(size=SIZE)


def test_rename_columns() -> None:
    """test if columns are being converted correctly to snake case"""
    response = data_cleaning_main(df=pd.DataFrame(data_mocked))
    snake_case_columns = [
        "id",
        "gender",
        "age",
        "driving_license",
        "region_code",
        "previously_insured",
        "vehicle_age",
        "vehicle_damage",
        "annual_premium",
        "policy_sales_channel",
        "vintage",
    ]
    assert list(response.columns) == snake_case_columns

    return None


@pytest.mark.parametrize(
    ("column", "data_type"),
    (
        ("region_code", "int"),
        ("policy_sales_channel", "int"),
        ("gender", "category"),
        ("vehicle_damage", "category"),
    ),
)
def test_convert_data_types(column: str, data_type: str) -> None:
    """test if columns' data types are being converted correctly"""
    response = data_cleaning_main(df=pd.DataFrame(data_mocked))
    assert response.dtypes[column] == data_type

    return None
