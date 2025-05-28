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
        "model": "o4-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "너는 제로칼로리, 제로설탕 식품 분석가야. 이미지 속 첨가물과 영양 정보를 분석해줘."
                    "제품의 영양 정보와 첨가물 정보를 바탕으로 "
                    "이 제품이 제로 칼로리인지, 제로 설탕인지 판단해줘. "
                    "영양 정보는 제품의 영양 성분표에 있는 정보를 참고해줘. "
                    "첨가물 정보는 제품의 성분표에 있는 첨가물 정보를 참고해줘. "
                    "설탕이 없으면 대체제로 무엇이 들어갔는지, 그 장단점을 말해줘. "
                    "그리고 이 제품이 무설탕인지, 제로 칼로리인지 판단해줘. "
                    "텍스트 정보가 없으면 분석하지 마. 무조건 한국어로 답해줘."
                    "답변은 최대 600자 내외로 작성해줘."
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
    }

    response = requests.post(OPENAI_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': response.text}), response.status_code