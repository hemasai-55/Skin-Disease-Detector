from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.applications import MobileNetV2
import os

os.makedirs('model', exist_ok=True)

print("Creating dummy model...")

base_model = MobileNetV2(weights=None, include_top=False, input_shape=(224,224,3))
model = Sequential([
    base_model,
    Flatten(),
    Dense(5, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.save('model/skin_disease_model.h5')

print("✅ Dummy model saved successfully at model/skin_disease_model.h5")

