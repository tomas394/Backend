def analyze_risk(metrics):
    # Mock: If any heart_rate > 120, risk is HIGH
    for m in metrics:
        if m.get("type") == "heart_rate" and m.get("value", 0) > 120:
            return "HIGH"
    return "LOW"
