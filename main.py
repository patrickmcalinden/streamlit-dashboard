import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Video Game Sales Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("vgsales.csv")
    df = df.dropna(subset=["Year"])  # Drop rows with missing year
    df["Year"] = df["Year"].astype(int)
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", options=["All"] + years)
selected_genre = st.sidebar.multiselect("Select Genre", options=sorted(df["Genre"].unique()), default=df["Genre"].unique())
selected_platform = st.sidebar.multiselect("Select Platform", options=sorted(df["Platform"].unique()), default=df["Platform"].unique())

# Filter data
filtered_df = df[df["Genre"].isin(selected_genre) & df["Platform"].isin(selected_platform)]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

# Dashboard title
st.title("🎮 Video Game Sales Dashboard")
st.markdown("Explore global and regional sales of top video games by genre, platform, and time.")

# Top 10 global sales
st.subheader("Top 10 Games by Global Sales")
top10 = filtered_df.sort_values(by="Global_Sales", ascending=False).head(10)
fig_top10 = px.bar(top10, x="Global_Sales", y="Name", orientation='h', title="Top 10 Games", labels={"Global_Sales": "Global Sales (Millions)", "Name": "Game"})
st.plotly_chart(fig_top10, use_container_width=True)

# Sales by Region
st.subheader("Regional Sales Breakdown")
sales_by_region = filtered_df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum().reset_index()
sales_by_region.columns = ["Region", "Sales"]
fig_region = px.pie(sales_by_region, names="Region", values="Sales", title="Sales by Region")
st.plotly_chart(fig_region, use_container_width=True)

# Genre Trends Over Time
st.subheader("Genre Sales Over Time")
genre_trend = df[df["Genre"].isin(selected_genre)].groupby(["Year", "Genre"])["Global_Sales"].sum().reset_index()
fig_trend = px.line(genre_trend, x="Year", y="Global_Sales", color="Genre", title="Genre Trends Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

# Platform Comparison
st.subheader("Platform Sales Comparison")
platform_sales = filtered_df.groupby("Platform")["Global_Sales"].sum().reset_index().sort_values(by="Global_Sales", ascending=False)
fig_platform = px.bar(platform_sales, x="Platform", y="Global_Sales", title="Sales by Platform")
st.plotly_chart(fig_platform, use_container_width=True)

# About
st.markdown("---")
st.markdown("Created by Patrick – Data Analyst Portfolio Showcase")
