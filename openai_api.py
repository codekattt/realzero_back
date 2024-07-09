import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

openai_api = Blueprint('openai_api', __name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

@openai_api.route('/openai', methods=['POST'])
def get_chatgpt_response():
    data = request.json
    prompt = data.get('prompt')

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'gpt-4o',
        'messages': [
            {
                'role': 'system',
                'content': (
                    'You are a food and nutrition analyst'
                    'Analyze the food additives and nutritional information in the given text.'
                    'Only if the text additive does not contain sugar, give the ingredient used in place of sugar and the advantages and disadvantages of that ingredient.'
                    'If text does not include any nutritional information or additives, say "분석할 수 있는 영양 정보와 첨가물 정보가 없습니다. 올바른 사진을 다시 제출해 주세요."'
                    'As a result, evaluate whether the product is sugar-free or zero-calorie or else.'
                    'Answer in only Korean.'
                )
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0,
        'max_tokens': 565,
        'top_p': 1,
        'frequency_penalty': 0.8,
        'presence_penalty':0.5
    }

    response = requests.post(OPENAI_ENDPOINT, headers=headers, json=payload)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error processing request'}), response.status_code