# flask, pandas, scikit-learn, pickle-mixin
from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("LinearRegressionModel.pkl", 'rb'))

car = pd.read_csv("Cleaned Car.csv")


@app.route('/')
def index():
    companies = sorted(car['company'].unique())
    car_models = car[['company', 'name']]  # Get both company and model

    # Prepare a dictionary for each company with corresponding models
    company_models = {}
    for company in companies:
        company_models[company] = sorted(car_models[car_models['company'] == company]['name'].unique())

    year = sorted(car['year'].unique(), reverse=True)
    fuel_types = car['fuel_type'].unique()

    # Pass company_models to the template
    return render_template('index.html', companies=companies, company_models=company_models, years=year,
                           fuel_types=fuel_types)

@app.route('/predict', methods=['POST'])
def predict():
    company= request.form.get('company')
    car_model= request.form.get('car_model')
    year= int(request.form.get('year'))
    fuel_type= request.form.get('fuel_type')
    kms_driven= int(request.form.get('kilo_driven'))
    #print(company, car_model, year, fuel_type, kms_driven)

    prediction = model.predict(pd.DataFrame([[car_model, company, year, kms_driven, fuel_type]], columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']))
    #print(prediction[0])
    return str(np.round(prediction[0], 2))



if __name__=="__main__":
    app.run(debug=True)