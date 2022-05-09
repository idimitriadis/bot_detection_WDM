import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics


df = pd.DataFrame(pickle.load(open('features/data','rb')))
df['label'] = df['label'].map({'human': 0, 'bot': 1})
print (df['label'].value_counts())
X = df.drop(['user_name', 'user_screen_name', 'user_id', 'label'], axis=1)
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,random_state=10)
print(y_train.value_counts())
model = RandomForestClassifier(random_state=14, n_jobs=-1, n_estimators=100, max_depth=10, min_samples_leaf=2)
# model = RandomForestClassifier(random_state=14, n_jobs=-1)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("F1 score:", metrics.f1_score(y_test, y_pred))
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred, target_names=['human', 'bot']))