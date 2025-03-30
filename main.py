import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Video Game Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("vgsales.csv")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    return df

df = load_data()

st.sidebar.title("Filters")
years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", options=["All"] + years)
selected_genre = st.sidebar.multiselect("Select Genre", options=sorted(df["Genre"].unique()), default=df["Genre"].unique())
selected_platform = st.sidebar.multiselect("Select Platform", options=sorted(df["Platform"].unique()), default=df["Platform"].unique())
selected_region = st.sidebar.selectbox("Select Region", options=["Global", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"])

filtered_df = df[df["Genre"].isin(selected_genre) & df["Platform"].isin(selected_platform)]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

st.title("🎮 Video Game Sales Dashboard")
st.markdown("Explore global and regional sales of top video games by genre, platform, and time.")

st.subheader("Top 10 Games by Sales")
top10 = filtered_df.sort_values(by=selected_region if selected_region != "Global" else "Global_Sales", ascending=False).head(10)
fig_top10 = px.bar(top10, x=selected_region if selected_region != "Global" else "Global_Sales", y="Name", orientation='h', title="Top 10 Games", labels={selected_region if selected_region != "Global" else "Global_Sales": "Sales (Millions)", "Name": "Game"})
st.plotly_chart(fig_top10, use_container_width=True)

st.subheader("Regional Sales Breakdown")
sales_by_region = filtered_df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum().reset_index()
sales_by_region.columns = ["Region", "Sales"]
fig_region = px.pie(sales_by_region, names="Region", values="Sales", title="Sales by Region")
st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Genre Sales Over Time")
genre_trend = df[df["Genre"].isin(selected_genre)].groupby(["Year", "Genre"])["Global_Sales"].sum().reset_index()
fig_trend = px.line(genre_trend, x="Year", y="Global_Sales", color="Genre", title="Genre Trends Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

st.subheader("Platform Sales Comparison")
platform_sales = filtered_df.groupby("Platform")["Global_Sales"].sum().reset_index().sort_values(by="Global_Sales", ascending=False)
fig_platform = px.bar(platform_sales, x="Platform", y="Global_Sales", title="Sales by Platform")
st.plotly_chart(fig_platform, use_container_width=True)

st.subheader("Publisher Performance Over Time")
pub_trend = df.groupby(["Year", "Publisher"])["Global_Sales"].sum().reset_index()
top_publishers = pub_trend.groupby("Publisher")["Global_Sales"].sum().nlargest(5).index
pub_trend = pub_trend[pub_trend["Publisher"].isin(top_publishers)]
fig_pub = px.line(pub_trend, x="Year", y="Global_Sales", color="Publisher", title="Top Publishers Over Time")
st.plotly_chart(fig_pub, use_container_width=True)

st.subheader("Genre Popularity by Region")
region_genre = df.groupby(["Genre"])[["NA_Sales", "EU_Sales", "JP_Sales"]].sum().reset_index()
region_genre = region_genre.melt(id_vars="Genre", var_name="Region", value_name="Sales")
fig_genre_region = px.bar(region_genre, x="Genre", y="Sales", color="Region", barmode="group", title="Genre Popularity by Region")
st.plotly_chart(fig_genre_region, use_container_width=True)

st.subheader("Platform Lifecycle")
platform_lifecycle = df.groupby(["Year", "Platform"])["Global_Sales"].sum().reset_index()
fig_lifecycle = px.line(platform_lifecycle, x="Year", y="Global_Sales", color="Platform", title="Platform Sales Lifecycle")
st.plotly_chart(fig_lifecycle, use_container_width=True)

st.subheader("Genre Trends per Platform")
genre_platform = df.groupby(["Platform", "Genre"])["Global_Sales"].sum().reset_index()
fig_genre_platform = px.bar(genre_platform, x="Platform", y="Global_Sales", color="Genre", title="Genre Popularity by Platform", barmode="stack")
st.plotly_chart(fig_genre_platform, use_container_width=True)

st.subheader("Publisher Market Share")
publisher_market = df.groupby("Publisher")["Global_Sales"].sum().reset_index().nlargest(5, "Global_Sales")
publisher_market.loc[len(publisher_market.index)] = ["Others", df[~df["Publisher"].isin(publisher_market["Publisher"])] ["Global_Sales"].sum()]
fig_market = px.pie(publisher_market, names="Publisher", values="Global_Sales", title="Top Publisher Market Share")
st.plotly_chart(fig_market, use_container_width=True)

st.subheader("Sales Bubble Chart")
bubble = df.copy()
bubble = bubble[bubble["Year"] >= 2000]
fig_bubble = px.scatter(bubble, x="Year", y="Global_Sales", size="NA_Sales", color="Platform", hover_name="Name", title="Sales vs Year vs Platform")
st.plotly_chart(fig_bubble, use_container_width=True)

st.subheader("Hidden Hits")
hidden_hits = df[(df["JP_Sales"] > 1) & (df["NA_Sales"] < 0.5)].sort_values(by="JP_Sales", ascending=False).head(10)
st.write("Games that were popular in Japan but underperformed in NA:")
st.dataframe(hidden_hits[["Name", "Platform", "Genre", "JP_Sales", "NA_Sales"]])

st.markdown("---")
st.markdown("Created by Patrick – Data Analyst Portfolio Showcase")
