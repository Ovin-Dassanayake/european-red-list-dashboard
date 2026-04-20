import plotly.express as px
import pandas as pd

# Chart 1 - Bar Chart: Species by Conservation Status
def bar_conservation_status(df):
    status_order = ["EX", "EW", "CR", "CR (PE)", "EN", "VU", "NT", "LC", "DD", "NE", "RE", "Unknown"]
    
    status_labels = {
        "EX": "EX — Extinct",
        "EW": "EW — Extinct in the Wild",
        "CR": "CR — Critically Endangered",
        "CR (PE)": "CR (PE) — Possibly Extinct",
        "EN": "EN — Endangered",
        "VU": "VU — Vulnerable",
        "NT": "NT — Near Threatened",
        "LC": "LC — Least Concern",
        "DD": "DD — Data Deficient",
        "NE": "NE — Not Evaluated",
        "RE": "RE — Regionally Extinct",
        "Unknown": "Unknown"
    }
    
    status_counts = df["europeanRegionalRedListCategory"].value_counts().reset_index()
    status_counts.columns = ["Category", "Count"]
    status_counts["Label"] = status_counts["Category"].map(status_labels)
    
    status_counts["Category"] = pd.Categorical(
        status_counts["Category"],
        categories=[s for s in status_order if s in status_counts["Category"].values],
        ordered=True
    )
    status_counts = status_counts.sort_values("Category")
    
    fig = px.bar(
        status_counts,
        x="Category",
        y="Count",
        color="Label",
        title="Species Count by Conservation Status",
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"Category": "Conservation Status", "Count": "Number of Species", "Label": "Status"},
        category_orders={"Category": status_order}
    )
    fig.update_layout(
        legend=dict(
            title="Conservation Status",
            orientation="v",
            x=1.02,
            y=1
        )
    )
    return fig

# Chart 2 - Treemap: Species by Group
def treemap_species_group(df):
    group_counts = df["speciesGroup"].value_counts().reset_index()
    group_counts.columns = ["Group", "Count"]
    group_counts["Group"] = group_counts["Group"].str.replace("_", " ")

    fig = px.treemap(
        group_counts,
        path=["Group"],
        values="Count",
        title="Species Distribution by Group",
        color="Count",
        color_continuous_scale="Greens"
    )
    fig.update_traces(textinfo="label+value+percent root")
    return fig

# Chart 3 - Heatmap: Conservation Status vs Species Group
def heatmap_status_vs_group(df):
    df = df.copy()
    df["speciesGroup"] = df["speciesGroup"].str.replace("_", " ")
    heat_data = df.groupby(
        ["speciesGroup", "europeanRegionalRedListCategory"]
    ).size().reset_index(name="Count")
    
    heat_pivot = heat_data.pivot(
        index="speciesGroup",
        columns="europeanRegionalRedListCategory",
        values="Count"
    ).fillna(0)
    
    fig = px.imshow(
        heat_pivot,
        title="Conservation Status vs Species Group",
        color_continuous_scale="Cividis",
        labels={"x": "Conservation Status", "y": "Species Group", "color": "Count"},
        aspect="auto"
    )
    return fig

# Chart 4 - Donut Chart: Population Trends
def donut_population_trend(df):
    trend_counts = df["populationTrend"].value_counts().reset_index()
    trend_counts.columns = ["Trend", "Count"]
    
    fig = px.pie(
        trend_counts,
        names="Trend",
        values="Count",
        title="Population Trends of European Species",
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(
        textposition="outside",
        textinfo="percent+label"
    )
    return fig

# Chart 5 - Threatened Species by Group
def bar_threatened_by_group(df):
    threatened_df = df[df["europeanRegionalRedListCategory"].isin(["CR", "EN", "VU"])]
    
    group_counts = threatened_df["speciesGroup"].value_counts().reset_index()
    group_counts.columns = ["Group", "Threatened Count"]
    group_counts["Group"] = group_counts["Group"].str.replace("_", " ")
    group_counts = group_counts.sort_values("Threatened Count", ascending=True)
    
    fig = px.bar(
        group_counts,
        x="Threatened Count",
        y="Group",
        orientation="h",
        title="Threatened Species by Group (CR + EN + VU)",
        color="Threatened Count",
        color_continuous_scale="YlOrRd",
        labels={"Threatened Count": "Number of Threatened Species", "Group": "Species Group"}
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    return fig

# Chart 6 - Data Table: Species Explorer
def data_table(df):
    table_df = df[[
        "scientificName",
        "speciesGroup", 
        "europeanRegionalRedListCategory",
        "populationTrend",
        "endemicToEurope"
    ]].reset_index(drop=True)
    
    table_df.columns = [
        "Scientific Name",
        "Species Group",
        "Conservation Status",
        "Population Trend",
        "Endemic to Europe"
    ]
   
    # Clean underscores
    table_df["Species Group"] = table_df["Species Group"].str.replace("_", " ")
    
    return table_df
