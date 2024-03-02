import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class EduAI:
    def __init__(self, content):
        self.content = content
        self.tokenizer = Tokenizer()
        self.max_sequence_len = 100
        self.model = self.create_model()

    def preprocess_data(self):
        self.tokenizer.fit_on_texts(self.content)
        sequences = self.tokenizer.texts_to_sequences(self.content)
        padded_sequences = pad_sequences(sequences, maxlen=self.max_sequence_len, padding='post')
        return padded_sequences

    def create_model(self):
        vocab_size = len(self.tokenizer.word_index) + 1
        model = Sequential([
            Embedding(vocab_size, 100, input_length=self.max_sequence_len),
            LSTM(150, return_sequences=True),
            LSTM(100),
            Dense(vocab_size, activation='softmax')
        ])
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def train(self, epochs=10):
        data = self.preprocess_data()
        X, y = data[:, :-1], data[:, -1]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs)

    def generate_content(self, seed_text, next_words=50):
        for _ in range(next_words):
            token_list = self.tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], maxlen=self.max_sequence_len-1, padding='post')
            predicted = np.argmax(self.model.predict(token_list), axis=-1)
            output_word = ""
            for word, index in self.tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break
            seed_text += " " + output_word
        return seed_text

if __name__ == "__main__":
    sample_content = ["The quick brown fox jumps over the lazy dog", "A stitch in time saves nine", "Actions speak louder than words"]
    eduai = EduAI(sample_content)
    eduai.train(epochs=5)
    print(eduai.generate_content("The quick brown fox", next_words=10))