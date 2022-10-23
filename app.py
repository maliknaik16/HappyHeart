
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

model = None

with open('model.pkl', 'rb') as m:

    # Safely loading the model.
    model = pickle.load(m)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():

    if not model:
        return {'message': 'Sorry an internal server error occurred.'}

    d = {}
    cols =['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']

    form_vals = list(request.form.values())

    for i in range(len(form_vals)):
        if cols[i] not in d:
            d[cols[i]] = []

        d[cols[i]].append(float(form_vals[i]))

    data = pd.DataFrame.from_dict(d)
    prediction = model.predict(data)

    output = prediction

    if output == 0:
        return render_template('index.html',
                               result = 'The patient is not likely to have heart disease!')
    else:
        return render_template('index.html',
                               result = 'The patient is likely to have heart disease!')

if __name__ == "__main__":
    app.run(debug=True)
