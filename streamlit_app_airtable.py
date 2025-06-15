
import streamlit as st
import pandas as pd
import requests
import datetime

# Load Airtable credentials from Streamlit secrets
AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]
BASE_ID = st.secrets["AIRTABLE_BASE_ID"]
TABLE_NAME = st.secrets["AIRTABLE_TABLE_NAME"]

# Fetch data from Airtable
def fetch_airtable_records():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    all_records = []
    offset = None

    while True:
        params = {"offset": offset} if offset else {}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            st.error("Failed to fetch data from Airtable.")
            return pd.DataFrame()

        data = response.json()
        all_records.extend(data["records"])
        offset = data.get("offset")
        if not offset:
            break

    # Flatten records
    rows = []
    for r in all_records:
        fields = r["fields"]
        fields["Submitted At"] = fields.get("Submitted At", r["createdTime"])
        rows.append(fields)

    return pd.DataFrame(rows)

# Streamlit UI
st.set_page_config(page_title="TrueVal Dashboard", layout="wide")
st.title("📊 TrueVal Dashboard")

df = fetch_airtable_records()

# Metrics
st.metric("Total Signups", len(df))
st.metric("Latest AI Accuracy", "92.48%")  # Placeholder

# Charts
if not df.empty and "Submitted At" in df.columns:
    df["Submitted At"] = pd.to_datetime(df["Submitted At"])
    df["Date"] = df["Submitted At"].dt.date
    signups_by_day = df.groupby("Date").size()

    st.subheader("📈 Signups Over Time")
    st.line_chart(signups_by_day)

    st.subheader("🧠 AI Model Accuracy (Simulated)")
    st.line_chart([91.2, 91.5, 92.0, 92.3, 92.48])  # Replace with real data later
else:
    st.warning("No records yet. Try submitting the Airtable form.")
