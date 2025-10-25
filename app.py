from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Placeholder diseases
DISEASES = {
    "Acne": "Wash your face twice daily and avoid oily foods.",
    "Eczema": "Moisturize your skin and avoid harsh soaps.",
    "Psoriasis": "Use medicated creams and avoid skin injuries.",
    "Rosacea": "Avoid spicy foods and alcohol; use gentle skincare."
}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
