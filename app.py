# save this as app.py
from flask import Flask, render_template
from flask import request
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

svm_model = pickle.load(open('model.pkl', 'rb'))
rf_model = pickle.load(open('rf_model.pkl', 'rb'))
kmeans_model = pickle.load(open('km_model.pkl', 'rb'))
# symptoms_model = pickle.load(open('symptoms_diabetes.pkl', 'rb'))



# x_test = np.array([[0,	0,	1,	31,	1,	0,	0,	0,	1,	1,	0,	1,	0,	4,	0,	0,	0,	1,	6,	3]])


app = Flask(__name__)

def convert_to_npArray(data):
    modified = [
        np.where(data["high_bp"] == "yes", 1 ,0),
          np.where(data["cholestrol"]== "yes", 1 ,0),
        #   np.where(data["cholestrol_level"]== "yes", 1 ,0),
          int(data["bmi"]),
          # np.where(data["smoker"]== "yes", 1 ,0),
          np.where(data["stroke"]== "yes", 1 ,0),
          np.where(data["heart_condition"]== "yes", 1 ,0),
          # np.where(data["physical_activity"]== "yes", 1 ,0),
          # np.where(data["fruits"]== "yes", 1 ,0),
         # np.where( data["veggies"]== "yes", 1 ,0),
          # np.where(data["alcohol_consumption"]== "yes", 1 ,0),
          # np.where(data["doctor_consultation"]== "yes", 1 ,0),
          np.where(data["general_health"]== "good", 1 ,0),
          # int(data["mental_health"]),
          int(data["physical_health"]),
          np.where(data["walk"]== "yes", 1 ,0),
          np.where(data["sex"]== "female", 1 ,0),
          int(data["age"]),
    ]
    test_value = np.array([modified])
    print("After converting given inputs to np array: \n", test_value)
    return test_value

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def welcome():
    if request.method == 'POST':
        data = request.json
        print("received data",data)
        result = convert_to_npArray(data)
        svm_predicted_value = svm_model.predict(result)
        km_predicted_value = kmeans_model.predict(result)
        rf_predicted_value = rf_model.predict(result)
        all_predictions = {
                                "svm_predicted" : (svm_predicted_value == 0 and {"output" : "No Diabetes"} ) or (svm_predicted_value == 1 and {"output" : "Pre Diabetes"} ) or (svm_predicted_value == 2 and {"output" : "Diabetes"} ),
                                "km_predicted" : (km_predicted_value == 0 and {"output" : "No Diabetes"} ) or (km_predicted_value == 1 and {"output" : "Pre Diabetes"} ) or (km_predicted_value == 2 and {"output" : "Diabetes"} ),
                                "rf_predicted" : (rf_predicted_value == 0 and {"output" : "No Diabetes"} ) or (rf_predicted_value == 1 and {"output" : "Pre Diabetes"} ) or (rf_predicted_value == 2 and {"output" : "Diabetes"} ) }
        print("got output :",all_predictions)
        
        return all_predictions
        # (predicted_value == 0 and {"output" : "No Diabetes"} ) or (predicted_value == 1 and {"output" : "Pre Diabetes"} ) or (predicted_value == 1 and {"output" : "Diabetes"} )

# @app.route("/")
# def hello():
#     get_data = pd.read_excel("predict.xlsx")
#     print(get_data.head())
#     encoding_description_column = pd.get_dummies(get_data["Description"])
#     print("values: \n", encoding_description_column.head())
    
#     x_test = encoding_description_column
#     value = symptoms_model.predict(x_test)
#     print("output: \n")
#     return "it will work"

CORS(app)