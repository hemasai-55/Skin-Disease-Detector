from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input
import numpy as np
import tensorflow as tf
import os

os.makedirs('model', exist_ok=True)

# Simple dummy model for testing
model = Sequential([
    Input(shape=(224, 224, 3)),
    Flatten(),
    Dense(5, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.save('model/skin_disease_model.h5')
print("✅ Dummy model saved successfully.")
