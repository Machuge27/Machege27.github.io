import tensorflow as tf
import numpy as np

# Define your model architecture
class TranslationModel(tf.keras.Model):
    def __init__(self, input_vocab_size, output_vocab_size, embedding_dim, units):
        super(TranslationModel, self).__init__()
        self.encoder_embedding = tf.keras.layers.Embedding(input_vocab_size, embedding_dim)
        self.encoder_lstm = tf.keras.layers.LSTM(units, return_state=True)
        self.decoder_embedding = tf.keras.layers.Embedding(output_vocab_size, embedding_dim)
        self.decoder_lstm = tf.keras.layers.LSTM(units, return_sequences=True, return_state=True)
        self.decoder_dense = tf.keras.layers.Dense(output_vocab_size, activation='softmax')

    def call(self, inputs):
        encoder_inputs, decoder_inputs = inputs
        encoder_embedding = self.encoder_embedding(encoder_inputs)
        encoder_outputs, state_h, state_c = self.encoder_lstm(encoder_embedding)
        encoder_states = [state_h, state_c]

        decoder_embedding = self.decoder_embedding(decoder_inputs)
        decoder_outputs, _, _ = self.decoder_lstm(decoder_embedding, initial_state=encoder_states)
        decoder_logits = self.decoder_dense(decoder_outputs)
        return decoder_logits

# Load and preprocess your own dataset (dummy example)
# For demonstration purposes, let's assume we have a small dataset of English and French sentences
english_sentences = ["hello", "how are you", "goodbye"]
french_sentences = ["Iomunee", "ichomegee?", "siketuyen"]

# Add start and end tokens to sentences
french_sentences = ['<start> ' + text + ' <end>' for text in french_sentences]

# Tokenize the sentences and convert them into numerical sequences
tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
tokenizer.fit_on_texts(english_sentences + french_sentences)
english_sequences = tokenizer.texts_to_sequences(english_sentences)
french_sequences = tokenizer.texts_to_sequences(french_sentences)

# Pad sequences to have the same length
english_sequences = tf.keras.preprocessing.sequence.pad_sequences(english_sequences, padding='post')
french_sequences = tf.keras.preprocessing.sequence.pad_sequences(french_sequences, padding='post')

# Define model parameters
input_vocab_size = len(tokenizer.word_index) + 1
output_vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 256
units = 512

# Initialize and compile the model
model = TranslationModel(input_vocab_size, output_vocab_size, embedding_dim, units)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

# Train the model (dummy example - replace with your actual training code)
model.fit([english_sequences, french_sequences[:, :-1]], french_sequences[:, 1:], batch_size=1, epochs=10)

# Deploy the trained model for inference
def translate_text(input_text):
    # Preprocess input text
    input_sequence = tokenizer.texts_to_sequences([input_text])
    input_sequence = tf.keras.preprocessing.sequence.pad_sequences(input_sequence, maxlen=english_sequences.shape[1], padding='post')

    # Initialize empty target sequence for translation
    max_output_length = french_sequences.shape[1] * 2  # Double the maximum length of the French sequences
    target_sequence = np.zeros((1, max_output_length))

    # Initialize first word of target sequence as the start token
    target_sequence[0, 0] = tokenizer.word_index['<start>']

    # Perform translation without progress updates
    with tf.device('/cpu:0'):  # Ensure prediction runs on CPU to avoid progress updates
        for i in range(1, max_output_length):
            output_sequence = model.predict([input_sequence, target_sequence], verbose=0)
            predicted_id = np.argmax(output_sequence[:, i-1, :])
            if predicted_id == tokenizer.word_index['<end>'] or i >= french_sequences.shape[1] - 1:
                break
            target_sequence[0, i] = predicted_id

    # Convert numerical sequence back to text
    translated_text = ' '.join([tokenizer.index_word.get(idx, '') for idx in target_sequence[0] if idx != 0])
    return translated_text


def main():
    while True:
        user_input = input("Enter text in English: ")
        if user_input.lower() == 'exit':
            break
        translated_text = translate_text(user_input)
        print("Translated text in French:", translated_text)

if __name__ == "__main__":
    main()
