import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

class VirtualMakeupTryOn:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.lipstick_colors = {
            'red': (0, 0, 255),
            'pink': (255, 105, 180),
            'nude': (255, 228, 196)
        }

    def apply_makeup(self, image_path, lipstick_color):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_roi = image[y:y+h, x:x+w]
            face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
            face_roi = cv2.resize(face_roi, (224, 224))
            face_roi = face_roi / 255.0
            face_roi = np.expand_dims(face_roi, axis=0)

            predicted_lipstick_color = self.model.predict(face_roi)
            predicted_lipstick_color = np.argmax(predicted_lipstick_color)

            if predicted_lipstick_color == 0:
                color = self.lipstick_colors['red']
            elif predicted_lipstick_color == 1:
                color = self.lipstick_colors['pink']
            else:
                color = self.lipstick_colors['nude']

            cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)

        cv2.imshow('Virtual Makeup Try-On', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    
    model_path = 'lipstick_color_model.h5'
    image_path = 'face_image.jpg'
    lipstick_color = 'red'

    try_on = VirtualMakeupTryOn(model_path)
    try_on.apply_makeup(image_path, lipstick_color)