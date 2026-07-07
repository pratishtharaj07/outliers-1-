import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    "Lower Percentile",
    0.0,
    10.0,
    1.0
)

upper_percentile = st.sidebar.slider(
    "Upper Percentile",
    90.0,
    100.0,
    99.9
)

show_data = st.sidebar.checkbox("Show Dataset", True)

# -----------------------------
# Dataset
# -----------------------------
st.header("📋 Original Dataset")

if show_data:
    st.dataframe(df)

st.write("Dataset Shape:", df.shape)

# -----------------------------
# Basic Information
# -----------------------------
st.header("📌 Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Average Price", f"${df['price'].mean():.2f}")

# -----------------------------
# Price Distribution Before Cleaning
# -----------------------------
st.header("📈 Price Distribution Before Cleaning")

fig, ax = plt.subplots(figsize=(8,4))
ax.hist(df["price"], bins=50)
ax.set_xlabel("Price")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# -----------------------------
# Box Plot Before Cleaning
# -----------------------------
st.header("📦 Box Plot Before Cleaning")

fig, ax = plt.subplots(figsize=(8,2))
ax.boxplot(df["price"], vert=False)
ax.set_xlabel("Price")
st.pyplot(fig)

# -----------------------------
# Percentile Calculation
# -----------------------------
min_threshold = df["price"].quantile(lower_percentile/100)
max_threshold = df["price"].quantile(upper_percentile/100)

st.header("📊 Threshold Values")

col1, col2 = st.columns(2)

col1.metric("Minimum Threshold", round(min_threshold,2))
col2.metric("Maximum Threshold", round(max_threshold,2))

# -----------------------------
# Outliers
# -----------------------------
lower_outliers = df[df["price"] < min_threshold]
upper_outliers = df[df["price"] > max_threshold]

st.header("🚨 Outlier Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Lower Outliers", lower_outliers.shape[0])
col2.metric("Upper Outliers", upper_outliers.shape[0])
col3.metric(
    "Total Outliers",
    lower_outliers.shape[0] + upper_outliers.shape[0]
)

# -----------------------------
# Clean Dataset
# -----------------------------
df2 = df[
    (df["price"] >= min_threshold) &
    (df["price"] <= max_threshold)
]

# -----------------------------
# Clean Dataset Preview
# -----------------------------
st.header("✅ Dataset After Removing Outliers")

st.write("Shape:", df2.shape)

st.dataframe(df2.head(10))

# -----------------------------
# Summary Statistics
# -----------------------------
st.header("📊 Summary Statistics")

st.dataframe(df2["price"].describe())

# -----------------------------
# Histogram After Cleaning
# -----------------------------
st.header("📈 Price Distribution After Cleaning")

fig, ax = plt.subplots(figsize=(8,4))
ax.hist(df2["price"], bins=50)
ax.set_xlabel("Price")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# -----------------------------
# Box Plot After Cleaning
# -----------------------------
st.header("📦 Box Plot After Cleaning")

fig, ax = plt.subplots(figsize=(8,2))
ax.boxplot(df2["price"], vert=False)
ax.set_xlabel("Price")
st.pyplot(fig)

# -----------------------------
# Dataset Comparison
# -----------------------------
st.header("📋 Dataset Comparison")

comparison = pd.DataFrame({
    "Description":[
        "Original Rows",
        "Rows After Cleaning",
        "Rows Removed"
    ],
    "Value":[
        df.shape[0],
        df2.shape[0],
        df.shape[0]-df2.shape[0]
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
    "Use the sidebar sliders to change percentile values and observe how the cleaned dataset changes."
)
