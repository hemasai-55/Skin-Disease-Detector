from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import json
from utils.nlp_advice import get_care_tip

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model (placeholder if not trained yet)
MODEL_PATH = 'model/skin_disease_model.h5'
model = load_model(MODEL_PATH)

# Load labels
labels = {
    0: "Acne",
    1: "Eczema",
    2: "Psoriasis",
    3: "Rosacea",
    4: "Normal"
}

def prepare_image(img_path):
    img = Image.open(img_path).convert('RGB')
    img = img.resize((224, 224))  # model input size
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route("/", methods=["GET", "POST"])
def index():
    diagnosis = None
    tip = None
    img_filename = None

    if request.method == "POST":
        file = request.files.get("image")
        if file:
            img_filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(img_filename)
            img_array = prepare_image(img_filename)
            preds = model.predict(img_array)
            class_idx = np.argmax(preds, axis=1)[0]
            diagnosis = labels[class_idx]
            tip = get_care_tip(diagnosis)
    return render_template("index.html", diagnosis=diagnosis, tip=tip, image_path=img_filename)

if __name__ == "__main__":
    app.run(debug=True)
