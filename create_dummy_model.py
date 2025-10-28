# create_dummy_model.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input
import os

os.makedirs("model", exist_ok=True)

model = Sequential([
    Input(shape=(224, 224, 3)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(5, activation='softmax')
])

model.save("model/skin_disease_model.h5")
print("✅ Dummy model saved successfully at model/skin_disease_model.h5")
