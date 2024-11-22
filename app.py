from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import PyPDF2
from dotenv import load_dotenv
import re
import ollama
import logging

load_dotenv()

ollama_host = os.getenv('OLLAMA_HOST', 'http://127.0.0.1:3000')
os.environ['OLLAMA_HOST'] = ollama_host

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def download_pdfs_from_drive():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(q="mimeType='application/pdf'", fields="files(id, name)").execute()
    items = results.get('files', [])

    pdf_files = []

    if not items:
        print('No files found.')
    else:
        for item in items:
            request = service.files().get_media(fileId=item['id'])
            file_name = item['name']
            fh = io.FileIO(file_name, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            pdf_files.append(file_name)
    
    return pdf_files

def extract_text_from_pdfs(pdf_files):
    texts = []
    for pdf_file in pdf_files:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            texts.append(preprocess_text(text))
    return texts

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def answer_question_with_ollama(question, context):
    try:
        response = ollama.chat(
            model='llama3.2:1b',
            messages=[
                {
                    'role': 'user',
                    'content': question,
                    'context': context
                }
            ]
        )
        if 'choices' in response and response['choices']:
            return response['choices'][0]['message']['content']
        else:
            return 'No answer found.'
    except Exception as e:
        logging.error(f"Error communicating with Ollama: {e}")
        return 'Error: Unable to get answer from Ollama.'

pdf_files = download_pdfs_from_drive()
texts = extract_text_from_pdfs(pdf_files)

@app.route('/')
def home():
    return "Welcome to the PDF Question Answering API!"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    context = " ".join(texts)
    answer = answer_question_with_ollama(question, context)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)