import pandas as pd
from django.shortcuts import render
from risk_engine.predict import predict_transaction
import numpy as np

def upload_transactions(request):

    if request.method == "POST":

        file = request.FILES["file"]

        df = pd.read_csv(file)
        features = df.drop(columns=["Class"], errors="ignore")
        results = []
        scores = []
        for _, row in features.iterrows():
            status, score = predict_transaction(row.values)
            results.append(status)
            scores.append(score)
        df["Status"] = results
        df["RiskScore"] = scores
        anomalies = df[df["Status"] == "Anomaly"]
        anomalies = df[df["Status"] == "Anomaly"]

        fraud_probability = round((len(anomalies) / len(df)) * 100, 2)
        df["Entity"] = np.random.randint(1, 50, size=len(df))

        context = {
            "transactions": df.to_dict("records"),
            "total": len(df),
            "anomalies": len(anomalies),
            "total": len(df),
            "anomalies": len(anomalies),
            "fraud_probability": fraud_probability
        }

        return render(request, "dashboard.html", context)

    return render(request, "upload.html")

