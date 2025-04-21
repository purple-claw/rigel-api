from flask import Flask, request, jsonify
from s3_utils import upload_to_s3
from pdf_processor import parse_pdf_and_extract_clauses
import os
import requests
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MODAL_API_URL = "https://iamnoty36--rigel-analyze.modal.run"

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    try:
        s3_url = upload_to_s3(path, filename)
        os.remove(path)
        return jsonify({"url": s3_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process', methods=['POST'])
def process_pdf():
    data = request.get_json()
    if "url" not in data:
        return jsonify({"error": "Missing PDF URL"}), 400

    try:
        clauses = parse_pdf_and_extract_clauses(data["url"])
        payload = {"texts": [{"text": c} for c in clauses]}
        response = requests.post(MODAL_API_URL, json=payload)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
