import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="eThekwini 2026 Election Analytics",
    layout="wide"
)

st.title("2026 South African Local Government Election Analytics")
st.subheader("eThekwini Metropolitan Municipality")

st.warning(
    "All 2026 values displayed below are model estimates, "
    "not actual election results."
)

# Load outputs
metro = pd.read_csv("ethekwini_2026_metro_forecast.csv")
wards = pd.read_csv("ethekwini_2026_ward_forecast.csv")
ward_leaders = pd.read_csv("ethekwini_2026_ward_leaders.csv")
turnout = pd.read_csv("ethekwini_2026_turnout_estimate.csv")

# -------------------------
# Metro section
# -------------------------

st.header("Metro-Level Party Estimates")

metro_display = metro.sort_values(
    "estimated_vote_share_2026",
    ascending=False
)

st.dataframe(
    metro_display,
    use_container_width=True
)

top_metro = metro_display.iloc[0]

st.metric(
    "Largest Numerical Model Estimate",
    f"{top_metro['estimated_vote_share_2026']:.2f}%"
)

st.caption(
    f"Associated party: {top_metro['party']}. "
    "This is a model output and not a statement about who will govern."
)

# Chart
chart_data = (
    metro_display[
        metro_display["estimated_vote_share_2026"] >= 1
    ][["party", "estimated_vote_share_2026"]]
    .set_index("party")
)

st.bar_chart(chart_data)

# -------------------------
# Ward section
# -------------------------

st.header("Selected Ward Estimates")

selected_ward = st.selectbox(
    "Select Ward",
    sorted(wards["ward"].astype(str).unique())
)

ward_data = wards[
    wards["ward"].astype(str) == str(selected_ward)
].sort_values(
    "estimated_share_2026",
    ascending=False
)

st.dataframe(
    ward_data,
    use_container_width=True
)

st.bar_chart(
    ward_data[
        ["party", "estimated_share_2026"]
    ].set_index("party")
)

st.subheader("Largest Numerical Estimate by Ward")

st.dataframe(
    ward_leaders,
    use_container_width=True
)

# -------------------------
# Turnout section
# -------------------------

st.header("2026 Turnout Estimates")

st.dataframe(
    turnout,
    use_container_width=True
)

# -------------------------
# Model information
# -------------------------

st.header("Methodology")

st.write("""
Historical IEC Local Government Election data for 2011, 2016 and 2021
was cleaned and analysed.

A persistence baseline, Linear Regression and Random Forest Regression
were evaluated for metro-level party vote share.

The persistence baseline produced the strongest performance on the
historical 2021 test data and was retained for the metro estimate.

A separate regression model was used for turnout.

Ward-level estimates use historical ward-level IEC observations.
""")

st.header("Limitations")

st.write("""
- Only a small number of historical election cycles are available.
- Political conditions can change between elections.
- Parties may enter, leave or change between election years.
- Ward boundaries may change.
- Historical relationships may not remain stable in 2026.
- Model estimates are not actual election results.
- Coalition formation is not predicted by this application.
""")