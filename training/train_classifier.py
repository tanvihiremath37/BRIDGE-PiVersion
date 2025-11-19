import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import os

DATA_PICKLE = 'training/data.pickle'

if not os.path.exists(DATA_PICKLE):
    raise FileNotFoundError("❌ data.pickle missing! Run create_dataset.py first.")

data_dict = pickle.load(open(DATA_PICKLE, 'rb'))

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

x_train, x_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, stratify=labels
)

model = RandomForestClassifier()
model.fit(x_train, y_train)

pred = model.predict(x_test)
acc = accuracy_score(pred, y_test)

print(f"✔ Accuracy: {acc * 100:.2f}%")

pickle.dump({'model': model}, open('models/model.p', 'wb'))
print("✔ model.p saved to models/")

# save labels
unique_labels = sorted(set(labels))
with open('models/labels.txt', 'w') as f:
    for lbl in unique_labels:
        f.write(str(lbl) + "\n")

print("✔ labels.txt saved to models/")
