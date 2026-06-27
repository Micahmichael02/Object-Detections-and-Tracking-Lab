import os
import numpy as np
import pickle
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# preparing the dataset 
input_dir = r'C:\Users\user\OneDrive\Documents\Computer Vision\Beginner_projects\image-classifier\clf-data'
categories = ['empty', 'not_empty']

data = []
labels = []

for category in categories:
    category_path = os.path.join(input_dir, category)  # Path to the category directory
    for file in os.listdir(category_path):
        img_path = os.path.join(category_path, file)  # Construct the image file path
        print(f"Processing file: {img_path}")  # Debugging step to confirm paths
        if not os.path.isfile(img_path):  # Skip if it's not a file
            continue
        try:
            img = imread(img_path)  # Read the image
            img = resize(img, (15, 15))  # Resize the image
            data.append(img.flatten())  # Flatten and append to data
            labels.append(categories.index(category))  # Append the label
        except Exception as e:
            print(f"Error processing file {img_path}: {e}")  # Handle and debug errors

data = np.asarray(data)
labels = np.asarray(labels)

# Debugging the dataset shapes
print(f"Data shape: {data.shape}")
print(f"Labels shape: {labels.shape}")

# training / testing split
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# train classifier
classifier = SVC()

parameters = [{'gamma': [0.01, 0.001, 0.0001], 'C': [1, 10, 100, 1000]}]

grid_search = GridSearchCV(classifier, parameters)

grid_search.fit(x_train, y_train)

# test performance
best_estimator = grid_search.best_estimator_

y_prediction = best_estimator.predict(x_test)

score = accuracy_score(y_test, y_prediction)

print(f"Accuracy: {score}")

# save model
with open('model.pkl', 'wb') as f:
    pickle.dump(best_estimator, f)
    print("Model saved to model.pkl")