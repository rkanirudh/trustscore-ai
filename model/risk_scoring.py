import pandas as pd

def calculate_procurement_risk(row, df):
    score = 0
    reasons = []

    # Supplier statistics
    supplier_df = df[df["supplier_name"] == row["supplier_name"]]
    supplier_award_total = supplier_df["awarded_amt"].sum()
    supplier_count = len(supplier_df)

    # Agency statistics
    agency_df = df[df["agency"] == row["agency"]]
    agency_median = agency_df["awarded_amt"].median()

    # Rule 1: High award compared to agency median
    if row["awarded_amt"] > 2 * agency_median:
        score += 40
        reasons.append("Award amount significantly higher than agency median")

    # Rule 2: Supplier repeatedly winning tenders
    if supplier_count > agency_df["supplier_name"].value_counts().mean():
        score += 30
        reasons.append("Supplier frequently wins tenders from same agency")

    # Rule 3: Supplier total exposure risk
    if supplier_award_total > df["awarded_amt"].quantile(0.90):
        score += 20
        reasons.append("Supplier has very high total awarded value")

    trust_score = max(0, 100 - score)

    if score >= 60:
        risk = "High"
    elif score >= 30:
        risk = "Medium"
    else:
        risk = "Low"

    return risk, trust_score, reasons
