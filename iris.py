# -*- coding: utf-8 -*-
"""IRIS.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LChjzqOdHJLZsE6PdgQ3HQbm1Upjq3sP

ECE 4424 PROJECT Spring 2024
IRIS
By Chenglong Liao.
"""

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

"""Use sklearn repo to get iris dataset. This set has 3 kind iris, 50 for each, total 150."""

# loading data
iris = load_iris()
X = iris.data
y = iris.target

iris_df = pd.DataFrame(data=np.c_[X, y], columns=iris.feature_names + ['target'])
print(iris_df)

"""Instead of manual, using PCA function in sklearn to dimensionality reduction the data from 4 to 2."""

pca = PCA(n_components=2)  # reduce the dimention from 4 to 2
X_reduced = pca.fit_transform(X)

# create the figure after reduce the dimention.
plt.figure(figsize=(8, 6))
colors = ['red', 'green', 'blue']
labels = iris.target_names

for color, i, target_name in zip(colors, [0, 1, 2], labels):
    plt.scatter(X_reduced[y == i, 0], X_reduced[y == i, 1], color=color, label=target_name, edgecolors='k')

plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of Iris Dataset')
plt.legend()
plt.show()

"""For 150 data, 7/10 of them used for trainning and 3/10 used for testing."""

# split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Standardization
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

train_df = pd.DataFrame(X_train, columns=iris.feature_names)
test_df = pd.DataFrame(X_test, columns=iris.feature_names)
train_df['species'] = [iris.target_names[i] for i in y_train]
test_df['species'] = [iris.target_names[i] for i in y_test]
# first 5 lines for training data after splitting
print("Training Set Preview:")
print(train_df.head())

# first 5 lines for testing data after splitting
print("\nTest Set Preview:")
print(test_df.head())

mlp = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1, warm_start=True, random_state=1, learning_rate_init=0.01)

# store the result for each epoch
epochs = 50
# according to the loss output later (use 100 for testing), it levelled of after epoch 42, so epochs set to 40.
train_accuracy = []
test_accuracy = []
loss_values = []

for epoch in range(epochs):
    mlp.fit(X_train_scaled, y_train)
    train_pred = mlp.predict(X_train_scaled)
    test_pred = mlp.predict(X_test_scaled)
    train_acc = accuracy_score(y_train, train_pred)
    test_acc = accuracy_score(y_test, test_pred)
    train_accuracy.append(train_acc)
    test_accuracy.append(test_acc)
    loss_values.append(mlp.loss_)
    print(f"Epoch {epoch+1}/{epochs} - Loss: {mlp.loss_:.4f} - Train Accuracy: {train_acc:.4f} - Test Accuracy: {test_acc:.4f}")

plt.figure(figsize=(10, 5))
plt.plot(loss_values, label='Loss')
plt.title('Loss over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(train_accuracy, label='Train Accuracy')
plt.plot(test_accuracy, label='Test Accuracy')
plt.title('Accuracy over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()