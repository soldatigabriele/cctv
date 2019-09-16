import requests
import json

class Model:
    def detect(self, imagePath, threshold):
        url = 'http://localhost:5000/model/predict?threshold=' + str(threshold)
        files = {'image': open(imagePath, 'rb')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            # Predictions will be an empty array if nothing is found
            return json.loads(response.content)['predictions']
        else:
            print("error" + str(response))
