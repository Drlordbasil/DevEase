import tensorflow as tf
import numpy as np
import pandas as pd
import cv2
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator


class VirtualStylist:
    def __init__(self):
        self.model = None
        self.label_encoder = None

    def train_model(self, data_dir):
        images, labels = self.load_data(data_dir)
        images = self.preprocess_data(images)

        X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

        self.label_encoder = LabelEncoder()
        y_train = self.label_encoder.fit_transform(y_train)
        y_val = self.label_encoder.transform(y_val)

        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
        self.model.add(MaxPooling2D((2, 2)))
        self.model.add(Conv2D(64, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D((2, 2)))
        self.model.add(Flatten())
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(10, activation='softmax'))

        self.model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        datagen = ImageDataGenerator(rotation_range=20, width_shift_range=0.1, height_shift_range=0.1,
                                     shear_range=0.1, zoom_range=0.1, horizontal_flip=True, vertical_flip=True)

        checkpoint = ModelCheckpoint('model.h5', save_best_only=True, verbose=1)
        early_stopping = EarlyStopping(patience=5, verbose=1)

        self.model.fit(datagen.flow(X_train, y_train, batch_size=32),
                       steps_per_epoch=len(X_train) // 32,
                       validation_data=(X_val, y_val),
                       epochs=20,
                       callbacks=[checkpoint, early_stopping])

    def load_data(self, data_dir):
        images = []
        labels = []
        for category in os.listdir(data_dir):
            category_dir = os.path.join(data_dir, category)
            for image_file in os.listdir(category_dir):
                image_path = os.path.join(category_dir, image_file)
                image = cv2.imread(image_path)
                image = cv2.resize(image, (64, 64))
                images.append(image)
                labels.append(category)
        return np.array(images), np.array(labels)

    def preprocess_data(self, images):
        images = images.astype('float32') / 255.0
        return images

    def predict_outfit(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, (64, 64))
        image = np.expand_dims(image, axis=0)
        image = self.preprocess_data(image)
        prediction = self.model.predict(image)
        predicted_label = self.label_encoder.inverse_transform(np.argmax(prediction))
        return predicted_label


def main():
    data_dir = 'fashion_dataset'
    image_path = 'test_image.jpg'

    virtual_stylist = VirtualStylist()
    virtual_stylist.train_model(data_dir)

    predicted_label = virtual_stylist.predict_outfit(image_path)
    print(f"The predicted outfit category for the image is: {predicted_label}")


if __name__ == '__main__':
    main()