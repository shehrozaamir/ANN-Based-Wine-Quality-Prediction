
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# -------------------------------
# Scikit-Learn (Machine Learning utilities)
# -------------------------------
from sklearn.model_selection import train_test_split
#  Splits the dataset into training and testing sets to evaluate model performance.

from sklearn.preprocessing import LabelEncoder, StandardScaler
# LabelEncoder: Converts categorical labels (e.g., "cat", "dog") into numeric values.
# StandardScaler: Normalizes/standardizes numerical features so they have mean=0 and variance=1.

from sklearn.linear_model import Perceptron
# A simple linear classifier (single-layer neural network). Good for binary classification tasks.

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
# accuracy_score: Measures how many predictions are correct.
# classification_report: Shows precision, recall, and F1-score for each class.
# confusion_matrix: Shows where the model is making correct vs wrong predictions.

# -------------------------------
# TensorFlow / Keras (Deep Learning utilities)
# -------------------------------
import tensorflow as tf

from tensorflow.keras.models import Sequential
# Lets you build a neural network layer-by-layer in a linear fashion.

from tensorflow.keras.layers import Dense
# Fully connected layer (every neuron connects to every neuron in the next layer).

from tensorflow.keras.layers import Dropout
# Randomly drops some neurons during training to prevent overfitting.

from tensorflow.keras.utils import to_categorical
# 👉 Converts class labels (like 0, 1, 2) into one-hot encoded format (e.g., [1,0,0], [0,1,0]).
     

df=  pd.read_csv('wine.csv')
     

print(df.head())
print(df.columns)
print(df.info())
# sns.pairplot(df,hue ='quality')
# plt.show()
X = df.drop('quality', axis=1)
y = (df['quality'] == 'good').astype(int) 
X_train, X_test, y_train, y_test = train_test_split(
     X, y, test_size=0.2, random_state=42,stratify=y)
     

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
     

per = Perceptron(max_iter = 1000,random_state=42)
per.fit(X_train_scaled, y_train)

y_pred_percep = per.predict(X_test_scaled)
     

print(accuracy_score(y_test,y_pred_percep))
print(classification_report(y_test,y_pred_percep))



from tensorflow.keras.layers import Input

model = Sequential([
    Input(shape=(11,)),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train_scaled, y_train,
                    epochs=100, batch_size=32, validation_split=0.2, verbose=1)

loss, acc = model.evaluate(X_test_scaled, y_test, verbose=1)
print(acc)


model.save('wine_model.keras')
import joblib
joblib.dump(scaler, 'scaler.pkl')

