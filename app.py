
from flask import Flask, request, render_template, send_from_directory, url_for, redirect
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import numpy as np
import pandas as pd
import requests
import pickle
import json
import os

load_dotenv('.env')

app = Flask(__name__)
API_KEY = os.environ.get('MAPS_API_KEY')
BASE_URL = os.environ.get('BASE_URL')

debug = os.environ.get('DEBUG')
debug = True if debug == 'true' else False
model = None

options = webdriver.ChromeOptions()
# opts = ['--headless']

# for option in opts:
#     options.add_argument(option)

service = Service(ChromeDriverManager().install())

with open('model.pkl', 'rb') as m:

    # Safely loading the model.
    model = pickle.load(m)


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('images', path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    return render_template('analyze.html')

@app.route('/good')
def good():
    return render_template('good.html')

@app.route('/bad', methods=['POST'])
def bad(latlng='33.777252127593584,-84.39540740633934'):

    if 'latlng' in request.args:
        latlng = request.args['latlng']

    gmaps_url = 'https://maps.googleapis.com/maps/api/geocode/json?key=%s&latlng=%s' % (API_KEY, latlng)

    gmap_resp = requests.get(gmaps_url).json()

    loc = gmap_resp['results'][0]['formatted_address'] if len(gmap_resp) > 0 else '349 Ferst Dr NW, Atlanta, GA 30332, USA'

    l = loc.strip().split(',')
    city = l[-3].strip()
    x = l[-2].strip().split(' ')
    zipcode = x[1].strip()
    state = x[0].strip()

    # doctors_list = doctors()
    doctors_list = requests.get('%s/doctors' % (BASE_URL, ), params={'city': city, 'zipcode': zipcode, 'state': state}).json()

    return render_template('bad.html', doctors=doctors_list['doctors'])

@app.route('/predict', methods = ['POST'])
def predict():


    if not model:
        return {'message': 'Sorry an internal server error occurred.'}

    form_vals = list(request.form.values())
    latlng = form_vals[-1].strip()

    if len(latlng) < 3:
        latlng = '33.777252127593584,-84.39540740633934'

    d = {}
    cols =['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']


    for i in range(len(form_vals) - 1):
        if cols[i] not in d:
            d[cols[i]] = []

        d[cols[i]].append(float(form_vals[i]))

    data = pd.DataFrame.from_dict(d)
    prediction = model.predict(data)

    prediction = int(prediction[0])

    if prediction == 0:
        return redirect(url_for('good'))


    return redirect(url_for('bad'), code=307)

@app.route('/doctors')
def doctors():

    args = request.args
    doctors = []

    if not debug:

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

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        content = driver.page_source

        soup = BeautifulSoup(content, 'lxml')

        cards = soup.findAll('div', {'class': 'results-card-wrap'})


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

        driver.close()

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
