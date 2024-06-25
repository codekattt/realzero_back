from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import uuid
import time
import json

load_dotenv()

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 오는 요청을 허용

api_url = 'https://sz8h5pxrg0.apigw.ntruss.com/custom/v1/31692/e0549b16f2ad13b9cb308654cfa5548115dd73f42285837baef730fb80531d36/general'
secret_key = os.getenv('OCR_SECRET_KEY')
if not secret_key:
    raise ValueError("No secret key provided in .env file.")

@app.route('/ocr', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
