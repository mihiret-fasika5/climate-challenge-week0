# =========================
# File: app/main.py
# =========================

import streamlit as st
import pandas as pd
from utils import load_data,preprocess_data, filter_data, plot_temperature_trend, plot_precip_boxplot

st.set_page_config(page_title="Climate Dashboard", layout="wide")

st.title("African Climate Trend Analysis")

# Load + preprocess
data = load_data()
data = preprocess_data(data)

# Sidebar controls
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(data["country"].unique()),
    default=sorted(data["country"].unique())
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(data["year"].min()),
    int(data["year"].max()),
    (int(data["year"].min()), int(data["year"].max()))
)

variable = st.sidebar.selectbox(
    "Select Variable",
    ["T2M", "PRECTOTCORR", "RH2M"]
)

# Filter data
filtered_data = filter_data(data, countries, year_range)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Temperature Trend")
    fig1 = plot_temperature_trend(filtered_data)
    st.pyplot(fig1)

with col2:
    st.subheader("Precipitation Distribution")
    fig2 = plot_precip_boxplot(filtered_data)
    st.pyplot(fig2)

# Variable preview
st.subheader(f"{variable} Overview")
st.line_chart(filtered_data.groupby("Date")[variable].mean())


