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
    data = request.get_json(silent=True)
    
    if not data or 'image_url' not in data:
        print("❌ image_url 누락 또는 잘못된 요청:", data)
        return jsonify({'error': 'No image URL provided'}), 400

    image_url = data['image_url']

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini-vision",
        "messages": [
            {
                "role": "system",
                "content": (
                    "너는 전문 식품 영양 분석가야. 사용자가 업로드한 이미지를 보고, 먼저 아래를 판단해줘:\n"
                    "- 이 이미지는 실제 식품 성분표 또는 식품 라벨로 보이는가?\n"
                    "- 텍스트가 존재하며, 성분명이나 영양정보 같은 식품 관련 텍스트가 포함되어 있는가?\n\n"
                    "✅ 위 조건이 모두 만족되면 분석을 계속해.\n"
                    "❌ 그렇지 않으면 '해당 이미지는 식품 성분 이미지가 아니므로 분석할 수 없습니다.'라고 답변해줘.\n\n"
                    "조건이 만족될 경우, 아래 항목을 분석해줘:\n"
                    "1. **원재료 및 첨가물**: ...\n"
                    "2. **설탕 여부**: ...\n"
                    "3. **제로 칼로리 여부**: ...\n"
                    "4. **장점과 단점**: ...\n\n"
                    "※ 반드시 한국어로 답변해줘."
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
        "max_tokens": 1200,
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
                        yield f"data: {chunk}\n\n"
                end = time.time()
                print(f"응답 완료 (총 {end - start:.2f}초)")
        except requests.exceptions.RequestException as e:
            yield f'data: {{"error": "{str(e)}"}}\n'

    return Response(stream_openai_response(), content_type='text/event-stream')
