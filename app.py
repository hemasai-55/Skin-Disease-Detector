from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model
MODEL_PATH = 'model/skin_disease_model.h5'
model = load_model(MODEL_PATH)

# Label names
labels = {0: "Acne", 1: "Eczema", 2: "Psoriasis", 3: "Rosacea", 4: "Normal"}

def prepare_image(img_path):
    img = Image.open(img_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/', methods=['GET', 'POST'])
def index():
    diagnosis = None
    image_path = None

    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            img_array = prepare_image(image_path)
            preds = model.predict(img_array)
            class_idx = int(np.argmax(preds, axis=1)[0])
            diagnosis = labels.get(class_idx, "Unknown")

    return render_template('index.html', diagnosis=diagnosis, image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True)
