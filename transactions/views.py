import pandas as pd
import numpy as np
from django.shortcuts import render
from risk_engine.predict import predict_transaction


def upload_transactions(request):

    if request.method == "POST":

        file = request.FILES["file"]

        df = pd.read_csv(file)

        # Drop label column if present
        features = df.drop(columns=["Class"], errors="ignore")

        results = []
        scores = []

        # Run predictions
        for _, row in features.iterrows():

            status, score = predict_transaction(row.values)

            results.append(status)
            scores.append(score)

        df["Status"] = results
        df["RiskScore"] = scores

        # Generate transaction IDs
        df["TX_ID"] = ["TX-" + str(i) for i in range(len(df))]

        # Assign entities randomly
        df["Entity"] = np.random.randint(1, 50, size=len(df))

        # Identify anomalies
        anomalies = df[df["Status"] == "Anomaly"]

        # Active alerts (high risk)
        alerts = df[df["RiskScore"] > 0.85]

        # Systemic risk calculation
        total_transactions = len(df)
        total_anomalies = len(anomalies)

        fraud_probability = round(
            (total_anomalies / total_transactions) * 100, 2
        )

        # Risk classification
        if fraud_probability < 3:
            risk_level = "LOW"
        elif fraud_probability < 7:
            risk_level = "MODERATE"
        else:
            risk_level = "HIGH"

        # Live transaction stream (limit to 50 for performance)
        live_stream = df.sample(min(50, len(df)))

        # Entity risk analysis
        entity_risk = (
            df.groupby("Entity")["RiskScore"]
            .mean()
            .reset_index()
        )

        def classify_entity(score):
            if score > 0.85:
                return "HIGH RISK"
            elif score > 0.6:
                return "MEDIUM RISK"
            else:
                return "LOW RISK"

        entity_risk["risk_level"] = entity_risk["RiskScore"].apply(classify_entity)

        context = {

            "transactions": live_stream.to_dict("records"),

            "alerts": alerts.to_dict("records"),

            "total": total_transactions,

            "anomalies": total_anomalies,

            "fraud_probability": fraud_probability,

            "risk_level": risk_level,

            "entities": entity_risk.to_dict("records"),
        }

        return render(request, "dashboard.html", context)

    return render(request, "dashboard.html")


def dashboard(request):
    return render(request,'dashboard1.html')