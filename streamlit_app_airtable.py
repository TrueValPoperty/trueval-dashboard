
import streamlit as st
from pyairtable import Table
import pandas as pd
import os

# Load Airtable credentials from Streamlit secrets
api_key = st.secrets["airtable"]["api_key"]
base_id = st.secrets["airtable"]["base_id"]
table_name = st.secrets["airtable"]["table_name"]

# Connect to Airtable
table = Table(api_key, base_id, table_name)
records = table.all()
data = pd.DataFrame([record['fields'] for record in records])

# Dashboard layout
st.set_page_config(page_title="TrueVal Dashboard", layout="wide")
st.title("📊 TrueVal Dashboard")

# Metrics
total_signups = len(data)
latest_accuracy = 92.48  # Placeholder – replace with dynamic logic if needed
st.metric("Total Signups", total_signups)
st.metric("Latest AI Accuracy", f"{latest_accuracy}%")

# Charts
st.subheader("📈 Signups Over Time")
if 'Submitted At' in data.columns:
    data["Submitted At"] = pd.to_datetime(data["Submitted At"], errors='coerce')
    st.line_chart(data.groupby(data["Submitted At"].dt.date).size())

st.subheader("🧠 AI Model Accuracy")
# Placeholder data – in production, load real accuracy logs
accuracy_data = pd.DataFrame({
    "Date": pd.date_range(end=pd.Timestamp.today(), periods=7),
    "Accuracy": [91.2, 91.5, 92.0, 91.8, 92.3, 92.1, latest_accuracy]
})
accuracy_data.set_index("Date", inplace=True)
st.line_chart(accuracy_data)
