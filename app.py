import logging
from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Define the Azure ML endpoint
ENDPOINT_URL = 'http://fd9f5216-e839-46fc-9230-a4349e84e804.centralindia.azurecontainer.io/score'  # Replace with your Azure ML endpoint URL
API_KEY = 'kF4tvezrxN1ZX0DvLYN6z17nYNJib7GM'  # Replace with your Azure API Key

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the form in the UI
        data = {
            'Customer ID': request.form['customer_id'],
            'Sales Volume': 0,
            'Pricing Tier': request.form['pricing_tier'],
            'Region': request.form['region'],
            'Season': request.form['season'],
            'Promotion Applied': request.form['promotion'],
            'Delivery Time (Days)': int(request.form['delivery_time']),
        }
  

        # Prepare data for the request
        payload = json.dumps({
            "Inputs": {
                "input1": [data]
            }
        })


        # Log the payload
        app.logger.debug(f"Payload being sent: {payload}")

        # Set headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }

        # Send POST request to Azure ML endpoint
        response = requests.post(ENDPOINT_URL, headers=headers, data=payload)

        # Log response details
        app.logger.debug(f"Response status code: {response.status_code}")
        app.logger.debug(f"Response text: {response.text}")

        # Handle response
        if response.status_code == 200:
            output_label = response.json()["Results"]["WebServiceOutput0"][0]["Scored Labels"]
            result = round(output_label)
            return render_template('results.html', result=result)
        else:
            error_message = f"Error {response.status_code}: {response.text}"
            return render_template('results.html', result={"error": error_message})

    except Exception as e:
        # Log exceptions
        app.logger.error(f"Exception occurred: {e}")
        return render_template('results.html', result={"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)



''' 
 

'''        