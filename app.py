# Install Streamlit (if not already installed)
!pip install streamlit

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="PhonePe Transaction Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com/colab/',
        'Report a bug': "https://www.google.com/colab/",
        'About': "# This is a PhonePe Transaction Dashboard created in Google Colab."
    }
)

# Custom CSS for a slightly more professional look
st.markdown("""
<style>
.main-header {
    font-size: 3em;
    text-align: center;
    color: #4CAF50;
    margin-bottom: 20px;
}
.subheader {
    font-size: 2em;
    color: #2E8B57;
    border-bottom: 2px solid #EEE;
    padding-bottom: 5px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)


# Load data with a spinner for better UX
@st.cache_data
def load_data():
    with st.spinner("Loading transaction data... Please wait."):
        return pd.read_csv("data.csv")

df = load_data()

# Title
st.markdown("<h1 class='main-header'>📊 PhonePe Transaction Dashboard</h1>", unsafe_allow_html=True)
st.write("Explore aggregated transaction data across India using various filters below.")

# Sidebar filters
st.sidebar.header("⚙️ Filters")

state = st.sidebar.selectbox("Select State", sorted(df["State"].unique()))
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique(), reverse=True))
quarter = st.sidebar.selectbox("Select Quarter", sorted(df["Quarter"].unique()))

# Filter data
filtered = df[
    (df["State"] == state) &
    (df["Year"] == year) &
    (df["Quarter"] == quarter)
]

# Display Summary Metrics in columns
st.markdown("<h2 class='subheader'>📈 Summary Metrics</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

total_transactions = int(filtered["Count"].sum())
total_amount = int(filtered["Amount"].sum())
average_amount_per_transaction = total_amount / total_transactions if total_transactions > 0 else 0

col1.metric("Total Transactions", f"{total_transactions:,}")
col2.metric("Total Amount (₹)", f"₹ {total_amount:,}")
col3.metric("Avg. Amt. per Transaction (₹)", f"₹ {average_amount_per_transaction:,.2f}")

# Transaction by Type Bar Chart
st.markdown("<h2 class='subheader'>💳 Transaction Distribution by Type</h2>", unsafe_allow_html=True)

type_data = filtered.groupby("Type")["Amount"].sum().reset_index()

fig = px.bar(
    type_data,
    x="Type",
    y="Amount",
    color="Type",
    title=f"Transaction Amount by Type in {state}, {year} Q{quarter}",
    labels={"Type": "Transaction Type", "Amount": "Total Amount (₹)"},
    hover_data={"Amount": ':,2f'}
)
fig.update_layout(showlegend=False) # Legend might be redundant if color is only for type
st.plotly_chart(fig, use_container_width=True)

# Yearly Trend Chart for the selected state
st.markdown("<h2 class='subheader'>📈 Yearly Transaction Trend for " + state + "</h2>", unsafe_allow_html=True)

trend = df[df["State"] == state].groupby("Year")["Amount"].sum().reset_index()

fig2 = px.line(
    trend,
    x="Year",
    y="Amount",
    markers=True,
    title=f"Total Transaction Amount per Year in {state}",
    labels={"Year": "Year", "Amount": "Total Amount (₹)"},
    hover_name="Year",
    hover_data={"Amount": ':,2f'}
)
fig2.update_traces(line_color='#4CAF50') # Example: Change line color
st.plotly_chart(fig2, use_container_width=True)

# Raw Data Section using expander for cleaner UI
st.markdown("<h2 class='subheader'>Raw Data & Export</h2>", unsafe_allow_html=True)

with st.expander("View Raw Filtered Data"):
    st.dataframe(filtered)

# Download Button
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Filtered Data as CSV",
    csv,
    f"{state}_{year}_Q{quarter}_filtered_data.csv",
    "text/csv",
    key='download-csv'
)

# Insights Section
st.markdown("<h2 class='subheader'>💡 Key Insights</h2>", unsafe_allow_html=True)

st.write("• **Digital payments are on a steady rise:** Analyzing the yearly trend often reveals a consistent increase in digital transactions.")
st.write("• **Regional disparities:** Observe how certain states consistently contribute more to the overall transaction volume.")
st.write("• **Peer-to-Peer transactions dominate:** The 'Peer-to-peer payments' type frequently represents a significant portion of the total transaction amount.")
st.write("• **Quarterly fluctuations:** Transaction activity might show seasonal patterns or specific quarterly peaks, influenced by events or holidays.")

st.markdown("---")
st.info("Data provided by PhonePe Pulse. This dashboard is for illustrative purposes.")
