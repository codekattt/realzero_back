import os
import requests
from flask import Blueprint, request, Response, jsonify
from dotenv import load_dotenv
import time

load_dotenv()

openai_api = Blueprint('openai_api', __name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

@openai_api.route('/openai', methods=['POST'])
def analyze_image_with_gpt():
    data = request.get_json()

    if 'image_url' not in data:
        return jsonify({'error': 'No image URL provided'}), 400

    image_url = data['image_url']

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
                        "image_url": { "url": image_url }
                    }
                ]
            }
        ],
        "temperature": 0.2,
        "max_tokens": 800,
        "stream": True
    }

    def stream_openai_response():
        try:
            start = time.time()
            with requests.post(OPENAI_ENDPOINT, headers=headers, json=payload, stream=True, timeout=60) as response:
                for line in response.iter_lines(decode_unicode=True):
                    if line and line.startswith('data: '):
                        chunk = line.replace('data: ', '')
                        if chunk.strip() == '[DONE]':
                            break
                        yield f"{chunk}\n"
                end = time.time()
                print(f"응답 완료 (총 {end - start:.2f}초)")
        except requests.exceptions.RequestException as e:
            yield jsonify({'error': str(e)})

    return Response(stream_openai_response(), content_type='text/event-stream')
