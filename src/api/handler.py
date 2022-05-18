import os
import joblib
from flask import Flask, request, Response
import pandas as pd
from vehicleinsurance import PipelineVehicleInsurance

# load model
HOME_PATH = os.getcwd().replace(r'\src\api', '')
model = joblib.load(HOME_PATH + r'\models\model.pkl')

# initialize API
app = Flask(__name__)

# create endpoint
@app.route('/rank', methods=['POST'])
def vehicle_insurance_ranking():
    test_json = request.get_json()

    # check if there is data
    if test_json:
        # check how much data
        if isinstance(test_json, dict):
            test_raw = pd.DataFrame(test_json, index=[0])
        else:
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
        
        # instantiate pipeline class
        pipeline = PipelineVehicleInsurance()

        # data cleansing
        df = pipeline.data_cleansing(test_raw)

        # feature engineering
        df = pipeline.feature_engineering(df)

        # data preprocessing
        df = pipeline.data_preprocessing(df)

        # get ranking
        df_response = pipeline.get_ranking(model, test_raw, df)

        return df_response
    else:
        return Response('{}', status=200, mimetype='application/json')

if __name__ == '__main__':
    PORT = os.environ.get('PORT', 5000)
    app.run('192.168.0.18', port=PORT, debug=True)
