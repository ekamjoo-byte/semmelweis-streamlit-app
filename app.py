# code snippet assisted by ChatGPT

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Semmelweis Hand-Washing Case",
    layout="wide"
)

# code snippet assisted by ChatGPT
@st.cache_data
def load_data():
    df = pd.read_csv("yearly_deaths_by_clinic-1.csv")

    df["Clinic"] = df["Clinic"].replace({
        "clinic 1": "Doctors (Clinic 1)",
        "clinic 2": "Midwives (Clinic 2)"
    })

    df["Mortality Rate (%)"] = (df["Deaths"] / df["Birth"]) * 100
    return df


df = load_data()

st.title("Doctors’ Clinic Had Significantly Higher Mortality Rates Than Midwives’ Clinic")
st.write("""
This app visualizes mortality rates in two maternity clinics studied by Dr. Ignaz Semmelweis. 
The data shows that the Doctors’ clinic consistently had higher death rates than the Midwives’ clinic, 
highlighting how differences in medical practice contributed to mortality and supporting the importance of hand-washing.
""")

# Summary metrics
overall_avg = df.groupby("Clinic")["Mortality Rate (%)"].mean().round(2)

m1, m2 = st.columns(2)

with m1:
    st.metric(
        "Doctors (Clinic 1)",
        f"{overall_avg['Doctors (Clinic 1)']:.2f}%"
    )

with m2:
    st.metric(
        "Midwives (Clinic 2)",
        f"{overall_avg['Midwives (Clinic 2)']:.2f}%"
    )

# ✅ Move this OUTSIDE columns
st.markdown("**Clinic 1 mortality is more than double Clinic 2, revealing a critical difference in medical practice.**")

st.markdown("### Explore the data")

min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

year_range = st.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Mortality Rate by Year and Clinic")

    mortality_chart = (
        alt.Chart(filtered_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("Mortality Rate (%):Q", title="Mortality Rate (%)"),
            color=alt.Color("Clinic:N", title="Clinic"),
            tooltip=[
                "Year",
                "Clinic",
                "Birth",
                "Deaths",
                alt.Tooltip("Mortality Rate (%):Q", format=".2f")
            ]
        )
        .properties(height=400)
    )

    st.altair_chart(mortality_chart, use_container_width=True)

with col2:
    st.subheader("Deaths by Year and Clinic")

    deaths_chart = (
        alt.Chart(filtered_df)
        .mark_bar()
        .encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("Deaths:Q", title="Deaths"),
            color=alt.Color("Clinic:N", title="Clinic"),
            xOffset="Clinic:N",
            tooltip=[
                "Year",
                "Clinic",
                "Birth",
                "Deaths",
                alt.Tooltip("Mortality Rate (%):Q", format=".2f")
            ]
        )
        .properties(height=400)
    )

    st.altair_chart(deaths_chart, use_container_width=True)

st.markdown("### Key findings")

avg_rates = (
    filtered_df.groupby("Clinic")["Mortality Rate (%)"]
    .mean()
    .round(2)
    .reset_index()
)

clinic1_rate = avg_rates.loc[
    avg_rates["Clinic"] == "Doctors (Clinic 1)",
    "Mortality Rate (%)"
].values

clinic2_rate = avg_rates.loc[
    avg_rates["Clinic"] == "Midwives (Clinic 2)",
    "Mortality Rate (%)"
].values

if len(clinic1_rate) > 0 and len(clinic2_rate) > 0:
    st.write(
        f"""
        Across the selected years, the average mortality rate was **{clinic1_rate[0]:.2f}%**
        in **Doctors (Clinic 1)** and **{clinic2_rate[0]:.2f}%** in **Midwives (Clinic 2)**.
        Clinic 1 consistently showed higher mortality, especially in the earlier years, which
        suggests that differences in medical practice played an important role. This pattern
        supports Semmelweis's argument that better hygiene, including hand-washing, could help
        reduce deaths.
        """
    )

st.markdown("### Data table")

display_df = filtered_df.copy()
display_df["Mortality Rate (%)"] = display_df["Mortality Rate (%)"].round(2)

st.dataframe(display_df, use_container_width=True)
