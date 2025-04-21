from flask import Flask, request, jsonify
from pdf_processor import parse_pdf_and_extract_clauses
import requests
from werkzeug.utils import secure_filename
from s3_utils import upload_to_s3
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/process', methods=['POST'])
def process_pdf():
    data = request.get_json()
    s3_url = data.get("url")

    if not s3_url:
        return jsonify({'error': 'No S3 URL provided'}), 400

    try:
        clauses = parse_pdf_and_extract_clauses(s3_url)
        payload = {"texts": [{"text": c} for c in clauses]}
        response = requests.post(MODAL_API_URL, json=payload)

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    filename = secure_filename(file.filename)
    local_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(local_path)

    try:
        s3_url = upload_to_s3(local_path, filename)
        os.remove(local_path)
        return jsonify({'message': 'File uploaded successfully', 'url': s3_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
