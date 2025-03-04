import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Kaggle dataset
df = pd.read_csv("../dataset/network_data.csv")

# Select important columns (Modify based on your dataset)
df = df[['duration', 'protocol_type', 'dst_bytes']]
 

# Rename columns
df.columns = ['length', 'protocol', 'label']

# Convert protocol to numeric (TCP=1, UDP=2, ICMP=3)
df['protocol'] = df['protocol'].map({'tcp': 1, 'udp': 2, 'icmp': 3})

# Convert 'dst_bytes' into an intrusion label (Example: Large packets are intrusions)
df['label'] = df['label'].apply(lambda x: 1 if x > 1000 else 0)  


# Split features and labels
X = df[['length', 'protocol']]
y = df['label']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# Save Model
joblib.dump(clf, "ids_model.pkl")
print("✅ Model trained & saved as 'ids_model.pkl'")

# Evaluate
y_pred = clf.predict(X_test)
print(f"✅ Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
