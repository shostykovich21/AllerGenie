# src/models/image_model.py

import tensorflow as tf
from tensorflow.keras import layers, models

def build_image_model(input_shape=(224,224,3), num_classes=6, dropout=0.3):
    base = tf.keras.applications.EfficientNetB0(
        input_shape=input_shape, include_top=False, weights="imagenet"
    )
    base.trainable = True

    inp = layers.Input(shape=input_shape, name="img_input")
    x   = tf.keras.applications.efficientnet.preprocess_input(inp)
    x   = base(x, training=True)
    x   = layers.GlobalAveragePooling2D()(x)
    x   = layers.Dropout(dropout)(x)
    out = layers.Dense(num_classes, activation="softmax", name="img_output")(x)

    return models.Model(inputs=inp, outputs=out, name="image_model")

