from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.applications import MobileNetV2

# Create a lightweight CNN model
base_model = MobileNetV2(weights=None, include_top=False, input_shape=(224,224,3))
model = Sequential([
    base_model,
    Flatten(),
    Dense(5, activation='softmax')  # 5 classes: Acne, Eczema, Psoriasis, Rosacea, Normal
])

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Save model
model.save('model/skin_disease_model.h5')
print("Dummy model created successfully!")
