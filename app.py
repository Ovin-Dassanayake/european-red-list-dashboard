import streamlit as st
from data_loader import load_data
from charts import (
    bar_conservation_status,
    treemap_species_group,
    heatmap_status_vs_group,
    donut_population_trend,
    data_table,
    bar_threatened_by_group
)

# Page config
st.set_page_config(
    page_title="European Red List Dashboard",
    page_icon="🌿",
    layout="wide"
)

# Load data
df = load_data()

# Title
st.title("🌿 European Red List 2024 Dashboard")
st.markdown("An interactive analysis of biodiversity risk and conservation status across European species.")
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔎 Filters")
st.sidebar.markdown("Use the filters below to explore the data")

species_groups = ["All"] + sorted(df["speciesGroup"].dropna().unique().tolist())
selected_group = st.sidebar.selectbox("Species Group", species_groups)

categories = ["All"] + sorted(df["europeanRegionalRedListCategory"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Conservation Status", categories)

population_trends = ["All"] + sorted(df["populationTrend"].dropna().unique().tolist())
selected_trend = st.sidebar.selectbox("Population Trend", population_trends)

endemic_options = ["All", "Yes", "No"]
selected_endemic = st.sidebar.selectbox("Endemic to Europe", endemic_options)
show_unknown = st.sidebar.checkbox("Include Unknown Classifications", value=True)

# Apply filters
filtered_df = df.copy()
if selected_group != "All":
    filtered_df = filtered_df[filtered_df["speciesGroup"] == selected_group]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["europeanRegionalRedListCategory"] == selected_category]
if selected_trend != "All":
    filtered_df = filtered_df[filtered_df["populationTrend"] == selected_trend]
if selected_endemic != "All":
    filtered_df = filtered_df[filtered_df["endemicToEurope"] == selected_endemic]
if not show_unknown:
    filtered_df = filtered_df[filtered_df["europeanRegionalRedListCategory"] != "Unknown"]
    filtered_df = filtered_df[filtered_df["populationTrend"] != "Unknown"]

# KPI Metrics
st.subheader("📊 Key Statistics")
col1, col2, col3, col4 = st.columns(4)
threatened = filtered_df[filtered_df["europeanRegionalRedListCategory"].isin(["CR", "EN", "VU"])]
pct_threatened = round((len(threatened) / len(filtered_df)) * 100, 1) if len(filtered_df) > 0 else 0
endemic_count = len(filtered_df[filtered_df["endemicToEurope"] == "Yes"])

col1.metric("🌿 Total Species", len(filtered_df))
col2.metric("⚠️ Threatened Species", len(threatened))
col3.metric("📊 % Threatened", f"{pct_threatened}%")
col4.metric("🌍 Endemic Species", endemic_count)
st.markdown("---")

# Row 1 - Bar chart and Treemap
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_conservation_status(filtered_df), use_container_width=True)
with col2:
    st.plotly_chart(treemap_species_group(filtered_df), use_container_width=True)

st.markdown("---")

# Row 2 - Heatmap full width
st.plotly_chart(heatmap_status_vs_group(filtered_df), use_container_width=True)

st.markdown("---")

# Threatened by group - full width
st.plotly_chart(bar_threatened_by_group(filtered_df), use_container_width=True)
st.markdown("---")

# Row 3 - Donut chart
col1, col2 = st.columns([1, 1])
with col1:
    st.plotly_chart(donut_population_trend(filtered_df), use_container_width=True)
with col2:
    st.markdown("### 💡 Key Insights")
    total = len(filtered_df)
    lc_pct = round(len(filtered_df[filtered_df["europeanRegionalRedListCategory"] == "LC"]) / total * 100, 1) if total > 0 else 0
    decreasing = len(filtered_df[filtered_df["populationTrend"] == "Decreasing"])
    unknown_trend = len(filtered_df[filtered_df["populationTrend"] == "Unknown"])
    unknown_pct = round(unknown_trend / total * 100, 1) if total > 0 else 0

    st.markdown(f"""
    - Least Concern species account for **{lc_pct}%** of all assessed species.
    - A total of **{len(threatened)}** species are threatened (CR + EN + VU), representing **{pct_threatened}%** of assessed species.
    - **{decreasing}** species have declining populations, raising significant conservation concern.
    - **{unknown_pct}%** of species have unknown population trends, indicating incomplete monitoring coverage across Europe.
    - **{endemic_count}** species are endemic to Europe — if lost here, they are gone forever.
    - Terrestrial Molluscs and Bees are among the largest represented groups, with Bees showing notable Data Deficient classifications.
    """)

st.markdown("---")

# Data Table
st.subheader("📋 Species Explorer")
st.markdown("Explore individual species data using the filters in the sidebar")
st.dataframe(data_table(filtered_df), use_container_width=True)
