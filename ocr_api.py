import os
import requests
import uuid
import time
import json
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

ocr_api = Blueprint('ocr_api', __name__)

api_url = 'https://sz8h5pxrg0.apigw.ntruss.com/custom/v1/31692/e0549b16f2ad13b9cb308654cfa5548115dd73f42285837baef730fb80531d36/general'
secret_key = os.getenv('OCR_SECRET_KEY')

@ocr_api.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    image_data = file.read()

    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    headers = {
        'X-OCR-SECRET': secret_key
    }

    response = requests.post(api_url, headers=headers, files={'file': image_data}, data={'message': json.dumps(request_json).encode('UTF-8')})

    if response.status_code == 200:
        ocr_result = response.json()
        infer_texts = []

        for image in ocr_result.get('images', []):
            for field in image.get('fields', []):
                infer_texts.append(field.get('inferText', ''))

        return jsonify({'inferText': infer_texts})
    else:
        return jsonify({'error': response.text}), response.status_code
