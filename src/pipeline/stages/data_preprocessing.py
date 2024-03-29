from typing import Dict, Union

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler


def data_preprocessing_main(
    df: pd.DataFrame,
    preprocessors: Dict[
        str,
        Union[StandardScaler, MinMaxScaler, RobustScaler],
    ],
) -> pd.DataFrame:
    """
    preprocess the data.

    :param df: pandas dataframe.
    :param preprocessors: dict with all preprocessors and the name of their corresponding columns.
    :returns pandas dataframe.
    """
    # frequency encoding
    col_frequency = df.groupby("policy_sales_channel").size() / len(df)
    df.loc[:, "policy_sales_channel"] = df.loc[:, "policy_sales_channel"].map(
        col_frequency
    )

    col_frequency = df.groupby("region_code").size() / len(df)
    df.loc[:, "region_code"] = df.loc[:, "region_code"].map(col_frequency)

    # encode
    if ["Yes", "No"] == list(df.loc[:, "vehicle_damage"].unique()):
        df = pd.get_dummies(df, columns=["vehicle_damage"], drop_first=True)
    else:
        df["vehicle_damage"] = df["vehicle_damage"].map({"Yes": 1, "No": 1})
        df.rename(columns={"vehicle_damage": "vehicle_damage_Yes"}, inplace=True)

    # standardize and rescale
    for col, pp in preprocessors.items():
        df.loc[:, [col]] = pp.transform(df.loc[:, [col]])

    # select features
    cols_selected = [
        "age",
        "region_code",
        "policy_sales_channel",
        "previously_insured",
        "vehicle_damage_Yes",
        "annual_premium",
        "annual_premium_per_age",
    ]

    return df.loc[:, cols_selected]
