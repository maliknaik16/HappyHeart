
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from flask import Flask, request, render_template
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import requests
import pickle
import json

app = Flask(__name__)

model = None

options = webdriver.ChromeOptions()
# opts = ['--headless']

# for option in opts:
#     options.add_argument(option)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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


@app.route('/doctors')
def doctors():

    args = request.args

    if 'city' not in args:
        return {'message': 'City not found.'}

    if 'zipcode' not in args:
        return {'message': 'Zipcode not found.'}


    if 'state' not in args:
        return {'message': 'State not found.'}

    city = args['city']
    zipcode = args['zipcode']
    state = args['state']

    url = 'https://doctor.webmd.com/results?q=Heart%20Doctor&d=40&pagenumber=1' + '&zc=%s&city=%s&state=%s' % (zipcode, city, state)

    driver.get(url)

    content = driver.page_source

    soup = BeautifulSoup(content, 'lxml')

    cards = soup.findAll('div', {'class': 'results-card-wrap'})

    doctors = []

    for card in cards:

        doctor = {}

        anchor = card.find('a', {'class': 'prov-name'})

        link = anchor['href'] if anchor else ''

        image = ''

        img = card.find('div', {'class': 'card-img with-url'})
        img = img.find('img') if img else None
        image = img['src'] if img else ''

        doctor['url'] = link
        doctor['img_url'] = image

        name = ''

        speciality = card.find('p', {'class': 'prov-specialty'}).get_text().strip()
        speciality = speciality.split(',')
        speciality = list(map(lambda x: x.strip(), speciality))
        doctor['speciality'] = speciality

        if anchor:
            name = anchor.get_text().strip()

        doctor['name'] = name
        desc = card.find('div', {'class': 'prov-bio'})
        desc = desc.get_text().strip()

        doctor['description'] = desc

        phone = card.find('button', {'data-metrics-link': 'ph'})
        phone = phone.get_text().strip() if phone else ''

        doctor['phone'] = phone

        address = card.find('span', {'class': 'addr-text'})
        address = address.get_text().strip() if address else ''
        doctor['address'] = address

        rating = card.find('span', {'class': 'webmd-rate--number'})
        rating = rating.get_text().strip() if rating else ''
        doctor['ratings'] = rating

        doctors.append(doctor)

    if len(doctors) == 0:

        resp = None
        with open('doctors.json', 'r') as f:
            print('Loading json from file')
            resp = json.load(f)

        if resp:
            return resp

    return {'doctors': doctors}


if __name__ == "__main__":
    app.run(debug=True)
