import cv2
import os
import numpy as np


def extract_label_from_filename(filename):
    parts = filename.split('_')
    if len(parts) != 5:
        raise ValueError(f"Filename {filename} does not match expected format.")

    # Extract and convert P, V, H values correctly
    p = int(parts[2].replace('P', ''))  # Remove 'P' and convert to int
    v = int(parts[3].replace('V', ''))  # Remove 'V' and convert to int
    h = int(parts[4].replace('H.jpg', ''))  # Remove 'H.jpg' and convert to int

    return np.array([p, v, h])


def load_dataset(dataset_path):
    images = []
    labels = []
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.jpg') and not file.startswith('.'):  # Ignore system files
                try:
                    label = extract_label_from_filename(file)
                    image_path = os.path.join(root, file)
                    image = cv2.imread(image_path)
                    image = cv2.resize(image, (224, 224))  # Resize for consistency
                    images.append(image)
                    labels.append(label)
                except ValueError as e:
                    print(e)  # Handle files that do not match the expected format
    images = np.array(images)
    labels = np.array(labels)
    return images, labels
