cat > app.py << 'EOF'
import os
import sys
import numpy as np
from PIL import Image
import tensorflow as tf

MODEL_PATH = 'model/skin_disease_model.h5'
if not os.path.exists(MODEL_PATH):
    print("❌ Model not found. Run create_dummy_model.py first.")
    sys.exit(1)

model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model loaded successfully.")

def analyze_skin(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    pred = model.predict(img_array)
    cls = ['Eczema', 'Acne', 'Healthy Skin'][np.argmax(pred)]
    tips = {
        'Eczema': 'Use gentle moisturizer. Avoid hot water.',
        'Acne': 'Wash your face twice daily with mild cleanser.',
        'Healthy Skin': 'Maintain hydration and balanced diet.'
    }
    print(f"\n🩺 Diagnosis: {cls}")
    print(f"💡 Care Tip: {tips[cls]}\n")

if len(sys.argv) < 2:
    print("Usage: python3 app.py <image_path>")
else:
    analyze_skin(sys.argv[1])
EOF
