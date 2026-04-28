# =========================
# File: app/utils.py
# =========================

import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns


def load_data():
    files =(glob.glob("C:\\Climate_data\\data\\ethiopia_clean.csv") 
+ glob.glob("C:\\Climate_data\\data\\kenya_clean.csv")
+ glob.glob("C:\\Climate_data\\data\\nigeria_clean.csv") 
+ glob.glob("C:\\Climate_data\\data\\sudan_clean.csv")
+ glob.glob("C:\\Climate_data\\data\\tanzania_clean.csv"))

    dfs = []

    for file in files:
        df = pd.read_csv(file)
        country = os.path.basename(file).replace("_clean.csv", "")
        df["country"] = country
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def preprocess_data(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df["year"] = df["Date"].dt.year
    return df


def filter_data(df, countries, year_range):
    return df[
        (df["country"].isin(countries)) &
        (df["year"] >= year_range[0]) &
        (df["year"] <= year_range[1])
    ]


def plot_temperature_trend(df):
    fig, ax = plt.subplots(figsize=(6,4))

    monthly = (
        df.groupby(["country", "year", df["Date"].dt.month])["T2M"]
        .mean()
        .reset_index()
    )

    monthly["date"] = pd.to_datetime(
        monthly["year"].astype(str) + "-" + monthly["Date"].astype(str) + "-01",
        errors="coerce"
    )

    for c in monthly["country"].unique():
        subset = monthly[monthly["country"] == c]
        ax.plot(subset["Date"], subset["T2M"], label=c)

    ax.set_title("Monthly Avg Temperature")
    ax.legend()
    return fig


def plot_precip_boxplot(df):
    fig, ax = plt.subplots(figsize=(6,4))
    sns.boxplot(data=df, x="country", y="PRECTOTCORR", ax=ax)
    ax.set_title("Precipitation Distribution")
    return fig


# =========================
# File: scripts/README.md
# =========================

# Climate Dashboard (Streamlit)

## Setup

