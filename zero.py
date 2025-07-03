from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://realzero.netlify.app"])

@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"}), 200

from openai_api import openai_api

app.register_blueprint(openai_api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)