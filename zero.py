from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://realzero.netlify.app"])

# Import and register blueprints
from ocr_api import ocr_api
from openai_api import openai_api

app.register_blueprint(ocr_api, url_prefix='/api')
app.register_blueprint(openai_api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)