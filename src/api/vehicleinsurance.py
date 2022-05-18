import os
import joblib
import pandas as pd

class PipelineVehicleInsurance:
    def __init__(self):
        # define home path directory
        self.HOME_PATH = os.getcwd().replace(r'\src\api', '')
        
        # load parameters
        self.ss_annual_premium_per_age = joblib.load(self.HOME_PATH + r'\parameters\ss_annual_premium_per_age.pkl')
        self.ss_annual_premium = joblib.load(self.HOME_PATH + r'\parameters\ss_annual_premium.pkl')
        self.mm_age = joblib.load(self.HOME_PATH + r'\parameters\mm_age.pkl')
        self.mm_annual_premium_per_age = joblib.load(self.HOME_PATH + r'\parameters\mm_annual_premium_per_age.pkl')
        self.mm_annual_premium = joblib.load(self.HOME_PATH + r'\parameters\mm_annual_premium.pkl')
    
    
    def data_cleansing(self, df):
        # convert to integer
        df['region_code'] = df.loc[:, 'region_code'].astype('int64')
        df['policy_sales_channel'] = df.loc[:, 'policy_sales_channel'].astype('int64')

        # convert to category
        df['vehicle_damage'] = df.loc[:, 'vehicle_damage'].astype('category')
        
        return df
    
    
    def feature_engineering(self, df):
        # annual_premium
        df['annual_premium_per_age'] = df['annual_premium'] / df['age']
        
        return df
    
    
    def data_preprocessing(self, df):
        # frequency encoding
        col_frequency = df.groupby('policy_sales_channel').size() / len(df)
        df.loc[:, 'policy_sales_channel'] = df.loc[:, 'policy_sales_channel'].map(col_frequency)

        col_frequency = df.groupby('region_code').size() / len(df)
        df.loc[:, 'region_code'] = df.loc[:, 'region_code'].map(col_frequency)

        # one-hot encoding
        df = pd.get_dummies(df, columns=['vehicle_damage'], drop_first=True)
        
        # standardization
        df.loc[:, ['annual_premium_per_age']] = self.ss_annual_premium_per_age.transform(df.loc[:, ['annual_premium_per_age']])
        df.loc[:, ['annual_premium']] = self.ss_annual_premium.transform(df.loc[:, ['annual_premium']])
        
        # minmax rescaling
        df.loc[:, ['annual_premium_per_age']] = self.mm_annual_premium_per_age.transform(df.loc[:, ['annual_premium_per_age']])
        df.loc[:, ['annual_premium']] = self.mm_annual_premium.transform(df.loc[:, ['annual_premium']])
        
        return df.loc[:, ['age', 'region_code', 'policy_sales_channel', 'previously_insured',
                          'vehicle_damage_Yes', 'annual_premium', 'annual_premium_per_age']]
    
    
    def get_ranking(self, estimator, original_data, test_data):
        # calculate probability
        p_hat = estimator.predict_proba(test_data)
        
        # rank
        original_data['score'] = p_hat[:, 1].tolist()
        original_data.sort_values(by='score', ascending=False, inplace=True)
        
        return original_data.to_json(orient='records', date_format='iso')
