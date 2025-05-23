# src/models/multimodal_model.py

import tensorflow as tf
from tensorflow.keras import layers, Model
from src.models.image_model import build_image_model
from src.models.text_model  import build_text_model

def build_multimodal_model(
    image_model: Model,
    text_model:  Model,
    metadata_dim: int,
    num_classes:  int,
    dropout:      float = 0.3
) -> Model:
    # image branch
    img_in   = image_model.input
    img_feats= image_model.output

    # text branch
    txt_in   = text_model.input               # [input_ids, attention_mask]
    txt_feats= text_model.output

    # metadata branch
    meta_in = layers.Input((metadata_dim,), name="meta_input")
    m = layers.Dense(64, activation="relu")(meta_in)
    m = layers.Dense(32, activation="relu")(m)

    # fuse
    x = layers.Concatenate()([img_feats, txt_feats, m])
    x = layers.Dropout(dropout)(x)
    out = layers.Dense(num_classes, activation="softmax", name="multimodal_output")(x)

    return Model(inputs=[img_in, *txt_in, meta_in], outputs=out, name="multimodal_model")

# ─── Self-test CLI ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🤖  Building multimodal_model with dummy params…")
    img_m = build_image_model(input_shape=(224,224,3), num_classes=6)
    txt_m = build_text_model(pretrained_name="distilbert-base-uncased", num_labels=23, max_seq_len=128)
    mm   = build_multimodal_model(
        image_model=img_m,
        text_model=txt_m,
        metadata_dim=10,
        num_classes=6
    )
    mm.summary()
