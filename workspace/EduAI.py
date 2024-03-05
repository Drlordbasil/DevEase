import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class EduAI:
    def __init__(self):
        self.user_data = pd.DataFrame()
        self.tokenizer = Tokenizer()
        self.model = None

    def collect_user_data(self, data):
        self.user_data = pd.concat([self.user_data, pd.DataFrame(data)], ignore_index=True)

    def analyze_user_data(self):
        preferences = self.user_data.groupby('userID').agg({'learningStyle': lambda x: x.mode()[0]})
        return preferences

    def generate_content_model(self, text_samples):
        self.tokenizer.fit_on_texts(text_samples)
        sequences = self.tokenizer.texts_to_sequences(text_samples)
        padded_sequences = pad_sequences(sequences, padding='post')
        vocab_size = len(self.tokenizer.word_index) + 1

        self.model = Sequential([
            Embedding(vocab_size, 64, input_length=padded_sequences.shape[1]),
            LSTM(64),
            Dense(64, activation='relu'),
            Dense(vocab_size, activation='softmax')
        ])
        self.model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return padded_sequences, vocab_size

    def train_content_model(self, text_samples, epochs=10):
        padded_sequences, vocab_size = self.generate_content_model(text_samples)
        X, y = padded_sequences[:, :-1], padded_sequences[:, -1]
        y = y.reshape(-1, 1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs)

    def generate_personalized_content(self, seed_text, next_words=50):
        for _ in range(next_words):
            token_list = self.tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], maxlen=self.model.input_shape[1]-1, padding='pre')
            predicted = np.argmax(self.model.predict(token_list), axis=-1)
            output_word = ""
            for word, index in self.tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break
            seed_text += " " + output_word
        return seed_text

def main():
    edu_ai = EduAI()
    user_data = [{'userID': 1, 'learningStyle': 'visual'}, {'userID': 2, 'learningStyle': 'auditory'}]
    edu_ai.collect_user_data(user_data)
    preferences = edu_ai.analyze_user_data()
    print(preferences)

    text_samples = ["Python is an interpreted, high-level and general-purpose programming language.",
                    "Python's design philosophy emphasizes code readability with its notable use of significant whitespace."]
    edu_ai.train_content_model(text_samples, epochs=1)
    personalized_content = edu_ai.generate_personalized_content("Python is", next_words=10)
    print(personalized_content)

if __name__ == "__main__":
    main()