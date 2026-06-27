import pickle as pkl
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


data_dict = pkl.load(open('data.pkl', 'rb'))

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

f = open('model.p', 'wb')
pkl.dump({'model': model, 'accuracy': accuracy}, f)
f.close()