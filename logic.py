import json
import time

import requests
import base64
from PIL import Image
from io import BytesIO

import config

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    def __base64_to_bytes(self, base64_string):
        image_bytes = base64.b64decode(base64_string)
        return image_bytes

    def __create_image_from_bytes(self, image_bytes):
        image_stream = BytesIO(image_bytes)
        image = Image.open(image_stream)
        return image

    def save_image(self, images_base64, file_path):
        image_bytes = self.__base64_to_bytes(images_base64)
        img = self.__create_image_from_bytes(image_bytes)

        img.save(file_path)

def get_image(prompt, api_url, api_key, secret_key):
    api = Text2ImageAPI(api_url, api_key, secret_key)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)
    return images[0]

if __name__ == '__main__':
    prompt = "Пушистый хомяк"
    api_url = "https://api-key.fusionbrain.ai/"
    api_key = config.API_TOKEN
    secret_key = config.SECRET_KEY

    api = Text2ImageAPI(api_url, api_key, secret_key)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)[0]
    
    api.save_image(images, "decoded_image.png")



            

#Не забудьте указать именно ваш YOUR_KEY и YOUR_SECRET.