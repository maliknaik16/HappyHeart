# HappyHeart -- HackGT 9 ML Submission

## Inspiration
We wanted to build an application that solved a widespread problem. Heart disease is something that makes one person die every 34 seconds, according to a source. Heart disease can be prevented and treated if screening is done properly. So we built a Machine Learning based web application that predicts whether a person is at risk of heart disease and also provide the list of nearest hospitals and doctors. This will help people of all ages since sometimes searching for hospitals and doctors and doing their own research can take time. Every second is important, so our application makes it more convenient and efficient for the user to predict of they are at risk for heart conditions and also gives then resources to help them.

## What it does
Happy Heart is a Machine Learning based web application that predicts if a person has a heart disease from the provided symptoms and connects the potential patients to the doctors. The front-end provides the interactive interface for the users to provide their symptoms. It asks the user various questions like age, gender, chest pain, etc. It then performs Machine Learning prediction on the provided input and returns if a user is at a risk of heart disease. If yes, then it provides the list of nearby doctors by scraping in real-time from webmd.com.

## How we built it
One of our main goal was to develop the application that helps the users to see if they are at a risk of any heart disease and get them treated at the earliest thereby optimizing their time so they can stay healthy. We built this app in Python, JavaScript, scikit-learn, Flask, Jinja, BeautifulSoup and Selenium.

The Machine Learning model was trained and tested on various different algorithms. The Support Vector Machine achieved the accuracy of 86%. We then exported the trained model (exported trained weights) to the pickle file, so that we don't have to retrain the model and can reuse the model once deployed.

The location component of this app requests the users location (latitude, and longitude) and then sends the users location to the scraping component. The location component uses the Google Maps Geocoding API to resolve the latitude and longitude to the formatted address that is used by the scraping component.

The scraping components launches the Selenium Chrome Web-driver and generates the URL from the location of the user and opens up the page and retrieves all the relevant information and returns the result to on an API endpoint in JSON format.

Finally, the UI was built using the Bootstrap, Jinja, and JavaScript that makes the UI clean and dynamic.

## Challenges we ran into
We initially had issues figuring out how we can integrate all the components like the Machine Learning, Web UI, Scraping, and Location into the single application. We sometimes faced issue while scraping as we were not getting the right data, so that's why we choose Selenium with BeautifulSoup to get the right data without getting blocked. We had to do a lot of analysis on the dataset to train the model on various Machine Learning algorithms like Logistic Regression, Decision Tree, Random Forest, Gradient Boosting Classifier, and Support Vector Machine. Our analysis can be found here.

## Accomplishments that we're proud of
We're very proud that we were able to wrap up this project and integrate all the components without breaking the system. We used the Machine Learning and combined it with various other components that makes our project very unique.

## What we learned
Overall, we improved our data analysis, UI/UX design, and back-end development skills through this project. We also learned to deploy the Machine Learning model to production environment and tie different functionalities. We were even able to scrape website to find the nearest doctors and return the result as an API endpoint.

## What's next for Happy Heart
In the future, we’ll try to focus on to getting more data samples and improve the accuracy and deploy our ML-based Web Application to the production and make it accessible for everyone. This app was developed with the Mobile Application in mind and exposes all the data endpoints that can be utilized to build the Mobile Application.

## Built With
`beautiful-soup`, `bootstrap`, `css`, `flask`, `html`, `javascript`, `jinja`, `jupyter-notebook`, `machine-learning`, `python`, `scikit-learn`, `selenium`
