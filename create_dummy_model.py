# create_dummy_model.py
import os
os.makedirs('model', exist_ok=True)

# This script requires tensorflow to be installed.
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPooling2D
    import numpy as np
except Exception as e:
    print("TensorFlow not available. Install tensorflow to create a model. Error:", e)
    raise SystemExit(1)

model = Sequential([
    Conv2D(8, (3,3), activation='relu', input_shape=(224,224,3)),
    MaxPooling2D(),
    Conv2D(16, (3,3), activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(32, activation='relu'),
    Dense(5, activation='softmax')  # 5 classes matching class_names in app.py
])

model.compile(optimizer='adam', loss='categorical_crossentropy')

# Save model
model_path = os.path.join('model','skin_disease_model.h5')
model.save(model_path)
print("Dummy model saved to", model_path)
