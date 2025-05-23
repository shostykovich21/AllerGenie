import tensorflow as tf
from tensorflow.keras import layers, Model
from src.models.image_model import build_image_model

# Safe dummy BERT-like model that connects both inputs
def build_dummy_text_model(seq_len=128, hidden_size=768):
    input_ids = tf.keras.Input(shape=(seq_len,), dtype=tf.int32, name="input_ids")
    attention_mask = tf.keras.Input(shape=(seq_len,), dtype=tf.int32, name="attention_mask")

    x = layers.Embedding(input_dim=30522, output_dim=hidden_size)(input_ids)

    # Wrap all raw TF logic inside a Lambda
    def masked_average(inputs):
        x, mask = inputs
        mask = tf.cast(tf.expand_dims(mask, -1), tf.float32)
        x = x * mask
        return tf.reduce_sum(x, axis=1) / (tf.reduce_sum(mask, axis=1) + 1e-9)

    x = layers.Lambda(masked_average, name="text_masked_avg")([x, attention_mask])

    return tf.keras.Model(inputs=[input_ids, attention_mask], outputs=x, name="dummy_text_model")

def build_multimodal_model(
    image_model: Model,
    text_model:  Model,
    metadata_dim: int,
    num_classes:  int,
    dropout:      float = 0.3
) -> Model:
    # image branch
    img_in    = image_model.input
    img_feats = image_model.output

    # text branch
    txt_inputs = text_model.input               # [input_ids, attention_mask]
    txt_feats  = text_model.output

    # metadata branch
    meta_in = layers.Input((metadata_dim,), name="meta_input")
    m = layers.Dense(64, activation="relu")(meta_in)
    m = layers.Dense(32, activation="relu")(m)

    # fuse
    x = layers.Concatenate()([img_feats, txt_feats, m])
    x = layers.Dropout(dropout)(x)
    out = layers.Dense(num_classes, activation="softmax", name="multimodal_output")(x)

    return Model(inputs=[img_in, *txt_inputs, meta_in], outputs=out, name="multimodal_model")


# ─── Self-test CLI ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🤖 Building multimodal_model with dummy text model…")

    img_m = build_image_model(input_shape=(224, 224, 3), num_classes=6)
    txt_m = build_dummy_text_model(seq_len=128, hidden_size=768)

    mm = build_multimodal_model(
        image_model=img_m,
        text_model=txt_m,
        metadata_dim=10,
        num_classes=6
    )
    mm.summary()
