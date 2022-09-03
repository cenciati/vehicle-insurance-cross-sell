import pandas as pd
from inflection import underscore


def data_cleaning_main(df: pd.DataFrame) -> pd.DataFrame:
    """
    cleans up the data.

    :param df: pandas dataframe.
    :returns pandas dataframe.
    """
    # rename columns
    df.columns = [underscore(col) for col in df.columns]

    # convert data types
    for col in ["region_code", "policy_sales_channel"]:
        df.loc[:, col] = df.loc[:, col].astype(int)

    for col in ["gender", "vehicle_damage"]:
        df.loc[:, col] = df.loc[:, col].astype("category")

    return df
