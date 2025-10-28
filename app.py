import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

# Try to import keras/tf; if not available we'll fallback to dummy behaviour
try:
    from tensorflow.keras.models import load_model
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MODEL_PATH = os.path.join('model', 'skin_disease_model.h5')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8 MB max upload


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Load model if exists (and TF is installed)
model = None
class_names = ['Acne', 'Eczema', 'Healthy', 'Psoriasis', 'Unknown']  # update to your classes

if TF_AVAILABLE and os.path.exists(MODEL_PATH):
    try:
        model = load_model(MODEL_PATH)
        print("Model loaded from", MODEL_PATH)
    except Exception as e:
        print("Failed to load model:", e)
        model = None
else:
    if not TF_AVAILABLE:
        print("TensorFlow/Keras not installed - running in dummy mode.")
    else:
        print("Model file not found - running in dummy mode.")


def preprocess_image(img_path, target_size=(224, 224)):
    """Open image, convert to RGB, resize and scale to [0,1]."""
    img = Image.open(img_path).convert('RGB')
    img = img.resize(target_size)
    arr = np.asarray(img).astype('float32') / 255.0
    arr = np.expand_dims(arr, axis=0)  # batch dimension
    return arr


def predict_with_model(img_path):
    """Return (label, confidence). If model missing, produce dummy output."""
    if model is None:
        # dummy deterministic fallback: base on file size / hash
        size = os.path.getsize(img_path)
        idx = size % len(class_names)
        label = class_names[idx]
        conf = 0.60 + ((size % 40) / 100)  # pseudo confidence
        return label, float(round(min(conf, 0.99), 2))
    else:
        x = preprocess_image(img_path)
        preds = model.predict(x)
        if preds.ndim == 2 and preds.shape[1] > 1:
            idx = int(np.argmax(preds[0]))
            conf = float(round(float(np.max(preds[0])), 2))
            label = class_names[idx] if idx < len(class_names) else f"Class {idx}"
            return label, conf
        else:
            # regression or single-output
            val = float(preds.flatten()[0])
            return "Prediction", float(round(val, 2))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part (key "image") in request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # if same name exists, append number
        base, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(save_path):
            filename = f"{base}_{i}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            i += 1

        file.save(save_path)

        # If webp or other format, PIL can open it in the preprocess step
        label, conf = predict_with_model(save_path)

        return jsonify({
            'filename': filename,
            'label': label,
            'confidence': conf,
            'image_url': url_for('uploaded_file', filename=filename)
        })

    return jsonify({'error': f'File type not allowed. Allowed: {ALLOWED_EXTENSIONS}'}), 400


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename=f'../{UPLOAD_FOLDER}/{filename}'), code=302)


if __name__ == '__main__':
    # set host=0.0.0.0 if you want network access; keep debug off in production
    app.run(debug=True)
