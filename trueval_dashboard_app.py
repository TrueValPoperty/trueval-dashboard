import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Simulated signup data
dates = pd.date_range(start="2025-06-01", end="2025-06-15")
signups = np.random.poisson(lam=3, size=len(dates))
ai_accuracy = np.clip(np.linspace(0.7, 0.92, len(dates)) + np.random.normal(0, 0.01, len(dates)), 0.7, 1.0)

df = pd.DataFrame({
    "Date": dates,
    "New Signups": signups,
    "AI Accuracy": ai_accuracy
})

st.title("📊 TrueVal Dashboard")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Signups", int(df["New Signups"].sum()))
with col2:
    st.metric("Latest AI Accuracy", f"{df["AI Accuracy"].iloc[-1]*100:.2f}%")

st.subheader("📈 Signups Over Time")
st.line_chart(df.set_index("Date")[["New Signups"]])

st.subheader("🧠 AI Model Accuracy")
st.line_chart(df.set_index("Date")[["AI Accuracy"]])
