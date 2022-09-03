from src.pipeline.stages.data_cleaning import data_cleaning_main
from src.pipeline.stages.feature_engineering import feature_engineering_main
from src.pipeline.stages.data_preprocessing import data_preprocessing_main
import joblib
import pandas as pd


class Pipeline:
    def __init__(self) -> None:
        # constants
        self.PATH_MODELS = "models"
        self.PATH_PARAMETERS = "src/pipeline/parameters"

        # load serialized model
        self.__model = joblib.load(f"{self.PATH_MODELS}/rf_classifier_tuned.joblib")

        # load parameters
        self.__mms_age = joblib.load(f"{self.PATH_PARAMETERS}/mms_age.joblib")
        self.__mms_annual_premium_per_age = joblib.load(
            f"{self.PATH_PARAMETERS}/mms_annual_premium_per_age.joblib"
        )
        self.__mms_annual_premium = joblib.load(
            f"{self.PATH_PARAMETERS}/mms_annual_premium.joblib"
        )

    def data_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        cleans up the data.

        :param df: pandas dataframe.
        :returns pandas dataframe.
        """
        df = data_cleaning_main(df)

        return df

    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        creates news features.

        :param df: pandas dataframe.
        :returns pandas dataframe.
        """
        df = feature_engineering_main(df)

        return df

    def data_preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        preprocess the data.

        :param df: pandas dataframe.
        :returns pandas dataframe.
        """
        preprocessors = {
            "age": self.__mms_age,
            "annual_premium_per_age": self.__mms_annual_premium_per_age,
            "annual_premium": self.__mms_annual_premium,
        }

        df = data_preprocessing_main(df, preprocessors)

        return df

    def get_prediction(self, df_raw: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
        """
        makes the prediction.

        :param df_raw: original data.
        :param df: test data.
        :returns ok status and a json with the predicted scores.
        """
        # calculate probability
        p_hat = self.__model.predict_proba(df)

        # rank
        df_raw["score"] = p_hat[:, 1].tolist()
        df_raw.sort_values(by="score", ascending=False, inplace=True)
        predicted_data = df_raw.to_dict(orient="records")

        return predicted_data
