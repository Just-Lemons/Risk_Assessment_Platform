import numpy as np
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "isolation_forest_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

def predict_transaction(transaction_features):

    data = np.array(transaction_features).reshape(1, -1)

    # scale
    data_scaled = scaler.transform(data)

    # prediction
    prediction = model.predict(data_scaled)

    # anomaly score
    score = model.decision_function(data_scaled)[0]

    risk_score = round(1 - score, 3)

    if prediction[0] == -1:
        status = "Anomaly"
    else:
        status = "Normal"

    return status, risk_score