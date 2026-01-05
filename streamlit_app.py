import streamlit as st
import pandas as pd
import json
import hashlib
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="TrustScore AI – Government Procurement",
    layout="wide"
)

DATA_PATH = "data/government-procurement-via-gebiz.csv"
USERS_PATH = "auth/users.json"

# -----------------------------
# AUTHENTICATION
# -----------------------------
def load_users():
    with open(USERS_PATH) as f:
        return json.load(f)

users = load_users()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

st.title("🔐 TrustScore AI – Government Procurement Risk System")

if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Logged in as Government Officer")
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

st.success("Logged in as Government Officer")

# -----------------------------
# LOAD DATASET
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

st.divider()

# -----------------------------
# DATASET OVERVIEW
# -----------------------------
st.header("📊 Procurement Dataset Overview")
st.write(f"**Total records:** {len(df)}")
st.dataframe(df.head(10), use_container_width=True)

st.divider()

# -----------------------------
# TRANSACTION SELECTION
# -----------------------------
st.header("🔍 Transaction Risk Analysis")

selected_tender = st.selectbox(
    "Select Tender Number",
    df["tender_no."].unique()
)

row = df[df["tender_no."] == selected_tender].iloc[0]

st.subheader("📄 Selected Transaction Details")
st.json(row.to_dict())

# -----------------------------
# ANALYZE BUTTON
# -----------------------------
if st.button("Analyze Transaction"):

    # -----------------------------
    # RISK LOGIC (REAL & VARIABLE)
    # -----------------------------
    risk_score = 0
    explanation = []

    awarded_amt = float(row["awarded_amt"])
    supplier = str(row["supplier_name"]).lower()
    status = str(row["tender_detail_status"]).lower()
    agency = str(row["agency"]).lower()

    # Rule 1: High value procurement
    if awarded_amt >= 500_000:
        risk_score += 40
        explanation.append("High awarded amount")

    # Rule 2: Awarded but zero value
    if awarded_amt == 0 and "awarded" in status:
        risk_score += 30
        explanation.append("Awarded tender with zero amount")

    # Rule 3: Unknown supplier
    if supplier == "unknown":
        risk_score += 30
        explanation.append("Supplier identity unknown")

    # Rule 4: Sensitive authority
    if "authority" in agency:
        risk_score += 10
        explanation.append("Sensitive government agency")

    # -----------------------------
    # FINAL DECISION
    # -----------------------------
    if risk_score >= 70:
        risk_level = "High"
        trust_score = 30
    elif risk_score >= 40:
        risk_level = "Medium"
        trust_score = 60
    else:
        risk_level = "Low"
        trust_score = 90

    # -----------------------------
    # BLOCKCHAIN HASH (PROOF)
    # -----------------------------
    ledger_record = {
        "user": st.session_state.user,
        "timestamp": str(datetime.utcnow()),
        "transaction": row.to_dict(),
        "result": {
            "risk_level": risk_level,
            "trust_score": trust_score,
            "explanation": explanation
        }
    }

    record_str = json.dumps(ledger_record, sort_keys=True)
    block_hash = hashlib.sha256(record_str.encode()).hexdigest()
    ledger_record["hash"] = block_hash

    # -----------------------------
    # OUTPUT UI (FIXED)
    # -----------------------------
    st.divider()
    st.header("🧠 AI Risk Decision")

    st.metric("TrustScore", trust_score)
    st.write(f"**Risk Level:** {risk_level}")

    # ✅ CORRECT STREAMLIT RENDERING (NO INLINE LOGIC)
    if risk_level == "Low":
        st.success("✅ Low Risk Procurement")
    elif risk_level == "Medium":
        st.warning("⚠️ Medium Risk Procurement")
    else:
        st.error("🚨 High Risk Procurement")

    st.subheader("📑 Explanation")
    if explanation:
        for e in explanation:
            st.write(f"- {e}")
    else:
        st.write("No major risk indicators detected")

    st.subheader("⛓️ Blockchain Proof (Hash)")
    st.code(block_hash)

    st.subheader("📦 Full Record Stored on Ledger")
    st.json(ledger_record)

    st.divider()
    st.write("✅ Analysis completed successfully")

# -----------------------------
# LOGOUT
# -----------------------------
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()
