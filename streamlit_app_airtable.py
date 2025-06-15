
import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Airtable config
AIRTABLE_TOKEN = "patHLA4PvSixJ9CEp.cbab0060adf7d6d38659f931c3ca4aca25023ec18232f364310a57343356f9cc"
BASE_ID = "appuM5JsPEWW9INWp"
TABLE_NAME = "Imported table"
API_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}"
}

# Fetch records from Airtable
def fetch_airtable_records():
    records = []
    offset = None
    while True:
        params = {"offset": offset} if offset else {}
        response = requests.get(API_URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            st.error("Failed to fetch data from Airtable.")
            return []
        data = response.json()
        records.extend(data["records"])
        offset = data.get("offset")
        if not offset:
            break
    return records

# Convert to DataFrame
def records_to_df(records):
    rows = []
    for rec in records:
        fields = rec["fields"]
        submitted = fields.get("Submitted At")
        if submitted:
            fields["Submitted At"] = datetime.fromisoformat(submitted.replace("Z", "+00:00"))
        rows.append(fields)
    return pd.DataFrame(rows)

# Streamlit UI
st.set_page_config(page_title="TrueVal Dashboard", layout="wide")

st.title("📊 TrueVal Dashboard")

records = fetch_airtable_records()
df = records_to_df(records)

col1, col2 = st.columns(2)
col1.metric("Total Signups", len(df))
col2.metric("Latest AI Accuracy", "92.48%")

st.subheader("📈 Signups Over Time")
if not df.empty and "Submitted At" in df.columns:
    df['Date'] = df['Submitted At'].dt.date
    signups_per_day = df.groupby('Date').size()
    st.line_chart(signups_per_day)

st.subheader("🧠 AI Model Accuracy")
# Placeholder logic
accuracy_data = pd.DataFrame({
    "Date": pd.date_range(end=datetime.today(), periods=10),
    "Accuracy": [90.1, 91.2, 91.8, 92.0, 92.3, 92.6, 92.7, 92.4, 92.5, 92.48]
})
accuracy_data.set_index("Date", inplace=True)
st.line_chart(accuracy_data)
