import requests
import os
from pdfminer.high_level import extract_text
from clause_extractor import extract_clauses

def download_pdf_from_url(url, local_path="temp.pdf"):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download PDF from {url}")
    
    with open(local_path, 'wb') as f:
        f.write(response.content)
    
    return local_path

def parse_pdf_and_extract_clauses(s3_url):
    local_file = download_pdf_from_url(s3_url)
    raw_text = extract_text(local_file)
    os.remove(local_file)

    clauses = extract_clauses(raw_text)
    return clauses
