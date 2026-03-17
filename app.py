from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.privacy_utils import (
    app_to_dataframe,
    compare_apps,
    compute_privacy_metrics,
    generate_recommendations,
    get_term_help_table,
    load_apps,
    plain_language_summary,
)

st.set_page_config(page_title="LabelClarity Studio", page_icon="🔐", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "sample_apps.json"
apps = load_apps(DATA_PATH)
app_names = [a["app_name"] for a in apps]

st.title("LabelClarity Studio")
st.caption("An interactive privacy label explainer and comparison prototype")

st.markdown(
    """
This prototype is inspired by research on user acceptance of privacy labels.
It extends the idea with **plain-language explanations, lightweight risk scoring,
and decision support** so users can compare apps more confidently.
"""
)

with st.sidebar:
    st.header("Controls")
    selected_name = st.selectbox("Choose an app", app_names)
    compare_mode = st.toggle("Compare all sample apps", value=False)
    show_raw = st.toggle("Show raw label table", value=True)
    show_help = st.toggle("Show term explanations", value=True)

selected_app = next(a for a in apps if a["app_name"] == selected_name)
metrics = compute_privacy_metrics(selected_app)

a, b, c, d = st.columns(4)
a.metric("Risk score", metrics["score"])
b.metric("Risk level", metrics["level"])
c.metric("Data categories", metrics["total_items"])
d.metric("Shared categories", metrics["shared_count"])

left, right = st.columns([1.2, 1])

with left:
    st.subheader(f"{selected_app['app_name']} at a glance")
    st.info(plain_language_summary(selected_app))

    df = app_to_dataframe(selected_app)
    if show_raw:
        st.markdown("### Privacy label details")
        st.dataframe(df, use_container_width=True)

with right:
    st.subheader("Why the score looks this way")
    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=metrics["score"],
            title={"text": "Privacy exposure score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#e4572e"},
                "steps": [
                    {"range": [0, 39], "color": "#e6f4ea"},
                    {"range": [40, 69], "color": "#fff4cc"},
                    {"range": [70, 100], "color": "#fde2e1"},
                ],
                "threshold": {
                    "line": {"color": "#2f2f2f", "width": 3},
                    "thickness": 0.8,
                    "value": metrics["score"],
                },
            },
        )
    )
    gauge.update_layout(height=280, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(gauge, use_container_width=True)

    radar = go.Figure()
    radar.add_trace(
        go.Scatterpolar(
            r=[
                metrics["total_items"],
                metrics["sensitive_count"],
                metrics["shared_count"],
                metrics["linked_count"],
                metrics["advertising_count"],
            ],
            theta=[
                "Data categories",
                "Sensitive data",
                "Shared data",
                "Linked data",
                "Advertising use",
            ],
            fill="toself",
            name=selected_app["app_name"],
        )
    )
    radar.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
    st.plotly_chart(radar, use_container_width=True)

st.subheader("Data collection breakdown")
purpose_df = (
    df.assign(Shared=df["shared"].map({True: "Shared", False: "Not shared"}))
    .groupby(["purpose", "Shared"], as_index=False)
    .size()
    .rename(columns={"size": "Count", "purpose": "Purpose"})
)
purpose_chart = px.bar(
    purpose_df,
    x="Purpose",
    y="Count",
    color="Shared",
    barmode="stack",
    title="What data is collected and whether it is shared",
)
purpose_chart.update_layout(xaxis_title="Purpose", yaxis_title="Items")
st.plotly_chart(purpose_chart, use_container_width=True)

st.markdown("---")

x1, x2 = st.columns([1, 1])
with x1:
    st.subheader("Recommended label enhancements")
    for rec in generate_recommendations(selected_app):
        st.markdown(f"- {rec}")

with x2:
    st.subheader("User-centered interpretation")
    st.markdown(
        f"""
- **Platform:** {selected_app['platform']}
- **Category:** {selected_app['category']}
- **Self reported label:** {'Yes' if selected_app.get('self_reported', True) else 'No'}
- **Sensitive data present:** {'Yes' if metrics['sensitive_count'] > 0 else 'No'}
- **Advertising related collection:** {'Yes' if metrics['advertising_count'] > 0 else 'No'}
        """
    )

if compare_mode:
    st.markdown("---")
    st.subheader("Cross-app comparison")
    cmp_df = compare_apps(apps)
    st.dataframe(cmp_df, use_container_width=True)

    fig = px.bar(
        cmp_df,
        x="App",
        y="Risk score",
        color="Risk level",
        hover_data=["Category", "Platform", "Shared", "Sensitive", "Linked"],
        title="Prototype privacy exposure comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(
        cmp_df,
        x="Data categories",
        y="Risk score",
        size="Shared",
        color="Risk level",
        hover_name="App",
        hover_data=["Sensitive", "Linked"],
        title="How amount of data practice relates to score"
    )
    st.plotly_chart(fig2, use_container_width=True)

if show_help:
    st.markdown("---")
    st.subheader("Plain-language help for common privacy label terms")
    st.dataframe(get_term_help_table(), use_container_width=True)

st.markdown("---")
st.caption(
    "Prototype note: the risk score in this project is a lightweight design aid, not a formal privacy or legal compliance judgment."
)
