cat > create_dummy_model.py << 'EOF'
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224,224,3)),
    tf.keras.layers.Conv2D(16,(3,3),activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(3,activation='softmax')
])
model.save('model/skin_disease_model.h5')
print("✅ Dummy model saved in model/skin_disease_model.h5")
EOF
