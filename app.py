from flask import Flask, render_template, request
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the model (dummy or trained)
MODEL_PATH = 'model/skin_disease_model.h5'
model = load_model(MODEL_PATH)

# Example class names
classes = ['Acne', 'Eczema', 'Melanoma', 'Psoriasis', 'Healthy']

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('index.html', prediction="No file uploaded.")

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', prediction="No file selected.")

    # Sanitize filename to avoid spaces and unsafe characters
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Load and preprocess image
    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict
    preds = model.predict(img_array)
    result_index = np.argmax(preds)
    prediction = classes[result_index]

    # Simple care tips
    care_tips = {
        'Acne': 'Wash face twice daily with mild cleanser; avoid oily cosmetics.',
        'Eczema': 'Apply moisturizer regularly; avoid harsh soaps.',
        'Melanoma': 'Seek immediate dermatologist advice for mole changes.',
        'Psoriasis': 'Use medicated creams and manage stress.',
        'Healthy': 'Your skin looks healthy! Maintain hydration and sunscreen.'
    }

    return render_template('index.html',
                           prediction=prediction,
                           tip=care_tips[prediction],
                           image_path=filepath)

if __name__ == '__main__':
    app.run(debug=True)
