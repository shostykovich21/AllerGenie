


# src/models/multimodal_model.py

import tensorflow as tf
from tensorflow.keras import layers, Model
from src.models.image_model import build_image_model
from src.models.text_model  import build_text_model

def build_multimodal_model(
    image_input_shape: tuple = (224,224,3),
    num_image_classes:  int   = 6,
    text_pretrained:    str   = "distilbert-base-uncased",
    num_text_labels:    int   = 23,
    max_seq_len:        int   = 256,
    metadata_dim:       int   = 10,
    num_classes:        int   = 6,
    dropout:            float = 0.3,
) -> tf.keras.Model:
    """
    Builds a fusion of:
      • EfficientNet-B0 image_model
      • DistilBERT text_model
      • Dense metadata branch
    """
    # 1) sub-models
    img_model = build_image_model(
        input_shape=image_input_shape,
        num_classes=num_image_classes,
        dropout=dropout
    )
    txt_model = build_text_model(
        pretrained_name=text_pretrained,
        num_labels=num_text_labels,
        max_seq_len=max_seq_len,
        dropout=dropout
    )

    # 2) inputs & embeddings
    img_in, img_feats   = img_model.input,  img_model.output
    txt_in_ids, txt_in_mask = txt_model.input
    txt_feats           = txt_model.output

    meta_in = layers.Input((metadata_dim,), name="meta_input")
    m = layers.Dense(64, activation="relu")(meta_in)
    m = layers.Dense(32, activation="relu")(m)

    # 3) fuse & head
    x = layers.Concatenate()([img_feats, txt_feats, m])
    x = layers.Dropout(dropout)(x)
    out = layers.Dense(num_classes, activation="softmax", name="multimodal_output")(x)

    return Model(
        inputs=[img_in, txt_in_ids, txt_in_mask, meta_in],
        outputs=out,
        name="multimodal_model"
    )

if __name__ == "__main__":
    # quick self-test
    mm = build_multimodal_model(
        image_input_shape=(224,224,3),
        num_image_classes=6,
        text_pretrained="distilbert-base-uncased",
        num_text_labels=23,
        max_seq_len=128,
        metadata_dim=10,
        num_classes=6,
        dropout=0.3
    )
    mm.summary()
