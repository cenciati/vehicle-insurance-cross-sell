import pandas as pd


def feature_engineering_main(df: pd.DataFrame) -> pd.DataFrame:
    """
    creates news features.

    :param df: pandas dataframe.
    :returns pandas dataframe.
    """
    # age
    df.loc[:, "older_than_36"] = df.loc[:, "age"].apply(lambda x: 1 if x > 36 else 0)

    # vintage
    df.loc[:, "vintage_weeks"] = df.loc[:, "vintage"].apply(lambda x: x / 7)
    df.loc[:, "vintage_months"] = df.loc[:, "vintage"].apply(lambda x: x / 30)

    # annual_premium
    df.loc[:, "annual_premium_per_age"] = df.loc[:, "annual_premium"] / df.loc[:, "age"]
    df.loc[:, "annual_premium_per_vintage"] = (
        df.loc[:, "annual_premium"] / df.loc[:, "vintage"]
    )
    df.loc[:, "annual_premium_per_vintage_weeks"] = (
        df.loc[:, "annual_premium"] / df.loc[:, "vintage_weeks"]
    )
    df.loc[:, "annual_premium_per_vintage_months"] = (
        df.loc[:, "annual_premium"] / df.loc[:, "vintage_months"]
    )

    # customer characteristic
    df.loc[:, "customer_characteristic"] = (
        df.loc[:, "gender"].map({"Male": 0, "Female": 1}).astype(int)
        + df.loc[:, "vehicle_age"]
        .map({"< 1 Year": 0, "1-2 Year": 1, "> 2 Years": 2})
        .astype(int)
        + df.loc[:, "vehicle_damage"].map({"No": 0, "Yes": 1}).astype(int)
        + df.loc[:, "previously_insured"]
        + df.loc[:, "age"].apply(
            lambda x: 2 if x >= 20 and x < 40 else 1 if x >= 40 and x < 60 else 0
        )
    )

    # drop columns that won't be used anymore
    df.drop(
        ["vehicle_age", "gender", "driving_license", "vintage"], axis=1, inplace=True
    )

    return df
