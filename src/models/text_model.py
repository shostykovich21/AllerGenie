import tensorflow as tf
from transformers import TFAutoModel, AutoConfig

def build_text_model(
    pretrained_name: str = "distilbert-base-uncased",
    num_labels: int = 23,
    max_seq_len: int = 256,
    dropout: float = 0.1,
) -> tf.keras.Model:
    config = AutoConfig.from_pretrained(pretrained_name, num_labels=num_labels)
    encoder = TFAutoModel.from_pretrained(pretrained_name, config=config)

    input_ids = tf.keras.Input(shape=(max_seq_len,), dtype=tf.int32, name="input_ids")
    attention_mask = tf.keras.Input(shape=(max_seq_len,), dtype=tf.int32, name="attention_mask")

    def wrap_encoder(inputs):
        ids, mask = inputs
        output = encoder(input_ids=ids, attention_mask=mask)
        return output.pooler_output if hasattr(output, "pooler_output") and output.pooler_output is not None \
               else output.last_hidden_state[:, 0, :]

    pooled_output = tf.keras.layers.Lambda(
        wrap_encoder,
        output_shape=(config.hidden_size,),
        name="bert_pooled_output"
    )([input_ids, attention_mask])

    x = tf.keras.layers.Dropout(dropout)(pooled_output)
    logits = tf.keras.layers.Dense(num_labels, activation=None, name="text_logits")(x)

    return tf.keras.Model(inputs=[input_ids, attention_mask], outputs=logits)

if __name__ == "__main__":
    print("📝 Building text model...")
    model = build_text_model(pretrained_name="distilbert-base-uncased", num_labels=23)
    model.summary()
    print("✅ Text model built successfully.")
