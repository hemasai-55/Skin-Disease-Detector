from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Dummy disease predictions for demo
DISEASES = {
    'Acne': 'Wash your face twice daily and avoid oily foods.',
    'Eczema': 'Moisturize your skin and avoid harsh soaps.',
    'Psoriasis': 'Use medicated shampoo and avoid skin injuries.',
    'Melanoma': 'Consult a dermatologist immediately for mole changes.',
    'Rosacea': 'Avoid spicy foods and alcohol; use gentle skincare.',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Randomly choose a disease for demonstration
    disease = random.choice(list(DISEASES.keys()))
    suggestion = DISEASES[disease]

    return jsonify({
        'prediction': disease,
        'suggestion': suggestion,
        'image_url': f'/uploads/{filename}'
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return app.send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
