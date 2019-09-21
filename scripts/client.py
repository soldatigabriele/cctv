import os
import json
import requests
from dotenv import load_dotenv

def get_predictions(imagePath, threshold):
    load_dotenv() 
    url = os.getenv("MODEL_LOCATION") + '/model/predict?threshold=' + str(threshold)
    files = {'image': open(imagePath, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        # Predictions will be an empty array if nothing is found
        return json.loads(response.content)['predictions']
    else:
        print("error" + str(response))
