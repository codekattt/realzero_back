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
        'model': 'gpt-4',
        'messages': [
            {
                'role': 'system',
                'content': (
                    'Your task is to analyze the additives in a food and evaluate whether it contains sugar, '
                    'and if not, what substitute sugar is used in its place, and whether this food has no sugar at all. '
                    'First, tell us what the most commonly used substitute sugar is in this food, and briefly describe the advantages and disadvantages of that additive. '
                    'If you do not include any nutritional information or additives, we will see a message saying "We are unable to analyze the nutritional content, please resubmit with the correct photo". '
                    'Answer in Korean'
                )
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
    }

    response = requests.post(OPENAI_ENDPOINT, headers=headers, json=payload)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error processing request'}), response.status_code