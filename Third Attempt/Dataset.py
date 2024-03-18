import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

#Will rotate, shift, scale, and flip the data, really only useful if we think that our dataset isn't robust enough
# from tensorflow.keras.preprocessing.image import ImageDataGenerator


def create_gaze_estimation_model():
    model = Sequential([
        Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(224, 224, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(128, kernel_size=(3, 3), activation='relu'),  # Additional Conv layer
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(256, activation='relu'),  # Increased capacity
        Dropout(0.5),  # Dropout to prevent overfitting
        Dense(3)  # Predicting 3 continuous values for P, V, H
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def extract_label_from_filename(filename):
    parts = filename.rstrip('.jpg').split('_')
    p = int(parts[2].strip('P'))
    v = int(parts[3].strip('V'))
    h = int(parts[4].strip('H'))
    return np.array([p, v, h])


def load_dataset(dataset_path):
    images = []
    labels = []
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.jpg') and not file.startswith('.'):
                file_path: str = os.path.join(root, file)
                image = cv2.imread(file_path)
                if image is not None:
                    image = cv2.resize(image, (224, 224))
                    image = image / 255.0  # Normalize pixel values
                    images.append(image)
                    label = extract_label_from_filename(file)
                    labels.append(label)
                else:
                    print(f"Warning: Unable to load image at {file_path}")
    return np.array(images), np.array(labels)


def main():
    dataset_path = '../columbia_gaze_data_set'
    images, labels = load_dataset(dataset_path)

    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

    model = create_gaze_estimation_model()
    # If we want to add data augmentation, define an ImageDataGenerator here and use .fit_generator() method
    model.fit(X_train, y_train, batch_size=28, epochs=20, validation_split=0.2)

    test_loss = model.evaluate(X_test, y_test, verbose=1)
    print(f'Test Loss: {test_loss}')

    # Displaying a subset of predictions
    num_samples_to_display = 5
    predictions = model.predict(X_test[:num_samples_to_display])
    for i in range(num_samples_to_display):
        print(f'Prediction: {predictions[i]}, Actual: {y_test[i]}')

    model.save('gaze_estimation_model.keras')


if __name__ == "__main__":
    main()
