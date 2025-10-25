from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

# fake model predictions for demo
diseases = ["Eczema", "Psoriasis", "Acne", "Rosacea", "Healthy Skin"]
care_tips = {
    "Eczema": "Keep skin moisturized and avoid harsh soaps.",
    "Psoriasis": "Use medicated creams and limit stress.",
    "Acne": "Wash face twice daily and avoid oily foods.",
    "Rosacea": "Avoid spicy foods and use sunscreen.",
    "Healthy Skin": "Maintain hydration and a balanced diet."
}

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # fake random prediction
    disease = random.choice(diseases)
    advice = care_tips[disease]

    return jsonify({'prediction': disease, 'advice': advice})

if __name__ == '__main__':
    app.run(debug=True)

