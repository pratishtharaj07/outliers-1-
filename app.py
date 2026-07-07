import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Airbnb Price Outlier Detection",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("🏠 Airbnb Price Outlier Detection")

st.write("""
This application detects and removes outliers from the **Price** column
using the **Percentile Method**.
""")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("AB_NYC_2019.csv")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("⚙️ Settings")

lower_percentile = st.sidebar.slider(
    "Lower Percentile (%)",
    min_value=0.0,
    max_value=10.0,
    value=1.0
)

upper_percentile = st.sidebar.slider(
    "Upper Percentile (%)",
    min_value=90.0,
    max_value=100.0,
    value=99.9
)

show_data = st.sidebar.checkbox("Show Original Dataset", value=True)

# -----------------------------
# Display Dataset
# -----------------------------
st.header("📋 Original Dataset")

if show_data:
    st.dataframe(df)

st.write("**Dataset Shape:**", df.shape)

# -----------------------------
# Dataset Information
# -----------------------------
st.header("📌 Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Average Price", f"${df['price'].mean():.2f}")

# -----------------------------
# Percentile Thresholds
# -----------------------------
min_threshold = df["price"].quantile(lower_percentile / 100)
max_threshold = df["price"].quantile(upper_percentile / 100)

st.header("📊 Threshold Values")

c1, c2 = st.columns(2)

c1.metric("Minimum Threshold", round(min_threshold, 2))
c2.metric("Maximum Threshold", round(max_threshold, 2))

# -----------------------------
# Detect Outliers
# -----------------------------
lower_outliers = df[df["price"] < min_threshold]
upper_outliers = df[df["price"] > max_threshold]

st.header("🚨 Outlier Summary")

o1, o2, o3 = st.columns(3)

o1.metric("Lower Outliers", lower_outliers.shape[0])
o2.metric("Upper Outliers", upper_outliers.shape[0])
o3.metric(
    "Total Outliers",
    lower_outliers.shape[0] + upper_outliers.shape[0]
)

# -----------------------------
# Display Outliers
# -----------------------------
with st.expander("View Lower Outliers"):
    st.dataframe(lower_outliers)

with st.expander("View Upper Outliers"):
    st.dataframe(upper_outliers)

# -----------------------------
# Remove Outliers
# -----------------------------
df2 = df[
    (df["price"] >= min_threshold) &
    (df["price"] <= max_threshold)
]

# -----------------------------
# Cleaned Dataset
# -----------------------------
st.header("✅ Cleaned Dataset")

st.write("**Shape of Cleaned Dataset:**", df2.shape)

st.dataframe(df2.head(10))

# -----------------------------
# Summary Statistics
# -----------------------------
st.header("📈 Price Summary Statistics")

st.dataframe(df2["price"].describe())

# -----------------------------
# Dataset Comparison
# -----------------------------
st.header("📋 Dataset Comparison")

comparison = pd.DataFrame({
    "Description": [
        "Original Rows",
        "Rows After Cleaning",
        "Rows Removed"
    ],
    "Value": [
        df.shape[0],
        df2.shape[0],
        df.shape[0] - df2.shape[0]
    ]
})

st.table(comparison)

# -----------------------------
# Download Button
# -----------------------------
csv = df2.to_csv(index=False)

st.download_button(
    label="⬇️ Download Cleaned Dataset",
    data=csv,
    file_name="cleaned_airbnb_data.csv",
    mime="text/csv"
)

# -----------------------------
# Success Message
# -----------------------------
st.success("✅ Outliers removed successfully using the Percentile Method!")

st.info(
    "Adjust the percentile values from the sidebar to see how the cleaned dataset changes."
)
