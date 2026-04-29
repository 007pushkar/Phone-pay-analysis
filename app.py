import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# Title
st.title("📊 PhonePe Transaction Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

state = st.sidebar.selectbox("Select State", df["State"].unique())
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
quarter = st.sidebar.selectbox("Select Quarter", sorted(df["Quarter"].unique()))

# Filter data
filtered = df[
    (df["State"] == state) &
    (df["Year"] == year) &
    (df["Quarter"] == quarter)
]

# Metrics
col1, col2 = st.columns(2)

col1.metric("Total Transactions", int(filtered["Count"].sum()))
col2.metric("Total Amount (₹)", int(filtered["Amount"].sum()))

# Bar Chart
st.subheader("💳 Transaction by Type")

type_data = filtered.groupby("Type")["Amount"].sum().reset_index()

fig = px.bar(type_data, x="Type", y="Amount", color="Type")
st.plotly_chart(fig, use_container_width=True)

# Trend Chart
st.subheader("📈 Yearly Trend")

trend = df[df["State"] == state].groupby("Year")["Amount"].sum().reset_index()

fig2 = px.line(trend, x="Year", y="Amount", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# Raw Data Button
if st.button("Show Raw Data"):
    st.dataframe(filtered)

# Download Button
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download Data", csv, "filtered_data.csv")

# Insights Section
st.subheader("📌 Insights")

st.write("• Digital payments are increasing every year")
st.write("• Some states dominate transaction volume")
st.write("• P2P transactions are widely used")
