import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)

# Mapping for seasons
season_label = {'Winter': 0, 'Spring': 1, 'Summer': 2, 'Fall': 3}

def categorize_season(day):
    if day <= 80 or day > 355:
        return 0  # Winter (Dec, Jan, Feb)
    elif 80 < day <= 172:
        return 1  # Spring (Mar, Apr, May)
    elif 172 < day <= 265:
        return 2  # Summer (Jun, Jul, Aug)
    else:
        return 3  # Fall (Sep, Oct, Nov)

# Load dataset
df = pd.read_csv('./archive/5yrdata.csv')

# Convert date column to season category
df['Season'] = df['Date time'].apply(lambda x: categorize_season(pd.to_datetime(x).dayofyear))

# Normalize features (DO NOT NORMALIZE target for classification)
X = df[['Temperature', 'Relative Humidity', 'Sea Level Pressure']]
X = (X - X.min()) / (X.max() - X.min())  # Min-Max scaling manually

y = df['Season'].astype(int)  # Ensure labels are integers

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Neural Network Model
model = Sequential([
    Dense(64, input_shape=(X.shape[1],), activation='relu'),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dense(4, activation='softmax')  # 4 categories: Winter, Spring, Summer, Fall
])

from tensorflow.keras.optimizers import Adam
model.compile(optimizer=Adam(learning_rate=0.0005), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.summary()

# Train Model
model.fit(X_train, y_train, epochs=250, batch_size=32, validation_split=0.3)

# Make Predictions
y_pred_probs = model.predict(X_test)  # (num_samples, 4)
y_pred_labels = np.argmax(y_pred_probs, axis=1)  # Convert probabilities to class labels

# Compute Confusion Matrix
cm = confusion_matrix(y_test, y_pred_labels)

# Plot Confusion Matrix
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=season_label.keys(),
            yticklabels=season_label.keys())
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Print Classification Report
print(classification_report(y_test, y_pred_labels, target_names=season_label.keys()))

# Save Model Weights to File
with open("hyper_param.txt", "w") as file:
    weights=str(model.get_weights())
    file.write(weight)

print("Confusion matrix and model weights saved successfully!")
