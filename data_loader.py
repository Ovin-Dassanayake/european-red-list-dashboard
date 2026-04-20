import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/european_red_list.csv")
    
    # Clean populationTrend - extract simple values from long text
    def clean_trend(val):
        if pd.isna(val):
            return "Unknown"
        val = str(val).strip()
        if val in ["Stable", "Increasing", "Decreasing", "Unknown"]:
            return val
        val_lower = val.lower()
        if "decreas" in val_lower:
            return "Decreasing"
        elif "increas" in val_lower:
            return "Increasing"
        elif "stable" in val_lower:
            return "Stable"
        elif "extinct" in val_lower:
            return "Extinct"
        else:
            return "Unknown"
    
    df["populationTrend"] = df["populationTrend"].apply(clean_trend)
    df["europeanRegionalRedListCategory"] = df["europeanRegionalRedListCategory"].fillna("Unknown")
    
    return df