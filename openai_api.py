import os
import base64
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

openai_api = Blueprint('openai_api', __name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

@openai_api.route('/openai', methods=['POST'])
def analyze_image_with_gpt():
    if 'file' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['file']
    image_bytes = file.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    image_data_url = f"data:{file.content_type};base64,{image_base64}"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": (
                    "너는 식품 영양 분석가야. 이미지 속 첨가물과 영양 정보를 분석해줘. "
                    "설탕이 없으면 대체제로 무엇이 들어갔는지, 그 장단점을 말해줘. "
                    "그리고 이 제품이 무설탕인지, 제로 칼로리인지 판단해줘. "
                    "텍스트 정보가 없으면 분석하지 마. 무조건 한국어로 답해줘."
                )
            },
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": "이 제품을 분석해줘." },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_url
                        }
                    }
                ]
            }
        ],
        "temperature": 0.2,
        "max_tokens": 800
    }

    response = requests.post(OPENAI_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': response.text}), response.status_code