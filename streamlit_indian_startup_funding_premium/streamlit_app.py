
# ============================================================
# Indian Startup Funding Analysis
# Premium Streamlit Dashboard
# ============================================================

from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# Page Config
# ============================================================

st.set_page_config(
    page_title="Indian Startup Funding Analysis",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Styling
# ============================================================

CUSTOM_CSS = """
<style>
:root {
    --bg: #f8fafc;
    --card: #ffffff;
    --ink: #0f172a;
    --muted: #64748b;
    --line: #e2e8f0;
    --blue: #2563eb;
    --cyan: #0891b2;
    --green: #16a34a;
    --orange: #ea580c;
    --red: #dc2626;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #eef6ff 0%, #f8fafc 35%, #ffffff 100%);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

[data-testid="stSidebar"] {
    background: #0f172a;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

section[data-testid="stSidebar"] div.stSelectbox label,
section[data-testid="stSidebar"] div.stMultiSelect label,
section[data-testid="stSidebar"] div.stSlider label {
    color: #e2e8f0 !important;
    font-weight: 700;
}

h1, h2, h3 {
    color: #0f172a;
    letter-spacing: -0.03em;
}

p, li, span, div {
    color: #334155;
}

.hero {
    background:
        radial-gradient(circle at top right, rgba(37,99,235,.28), transparent 30%),
        linear-gradient(135deg, #0f172a 0%, #172554 55%, #0e7490 100%);
    border-radius: 30px;
    padding: 34px 38px;
    color: white;
    margin-bottom: 22px;
    box-shadow: 0 20px 55px rgba(15,23,42,.20);
    position: relative;
    overflow: hidden;
}

.hero:after {
    content: "";
    position: absolute;
    right: -70px;
    bottom: -90px;
    width: 360px;
    height: 360px;
    background: rgba(255,255,255,.08);
    border-radius: 50%;
}

.hero-eyebrow {
    color: #bae6fd;
    text-transform: uppercase;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: .14em;
    margin-bottom: 12px;
}

.hero-title {
    color: #ffffff;
    font-size: 48px;
    font-weight: 950;
    line-height: 1.05;
    letter-spacing: -0.055em;
    margin-bottom: 14px;
}

.hero-subtitle {
    color: #dbeafe;
    max-width: 860px;
    font-size: 18px;
    line-height: 1.55;
    margin-bottom: 18px;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 12px;
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.22);
    border-radius: 999px;
    color: #ffffff;
    font-size: 13px;
    font-weight: 750;
    margin-right: 8px;
    margin-top: 6px;
}

.metric-card {
    background: rgba(255,255,255,.92);
    border: 1px solid #e2e8f0;
    border-radius: 22px;
    padding: 20px 20px 18px 20px;
    min-height: 135px;
    box-shadow: 0 14px 35px rgba(15,23,42,.08);
}

.metric-label {
    color: #64748b;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: .10em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.metric-value {
    color: #0f172a;
    font-size: 32px;
    line-height: 1.05;
    font-weight: 950;
    letter-spacing: -0.05em;
}

.metric-note {
    color: #64748b;
    font-size: 13px;
    line-height: 1.4;
    margin-top: 9px;
}

.story-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 14px 35px rgba(15,23,42,.07);
    margin-bottom: 16px;
}

.story-title {
    color: #0f172a;
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 10px;
    letter-spacing: -0.03em;
}

.story-body {
    color: #475569;
    font-size: 15.5px;
    line-height: 1.65;
}

.insight {
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    border: 1px solid #e2e8f0;
    border-left: 5px solid #2563eb;
    border-radius: 18px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 8px 22px rgba(15,23,42,.06);
}

.insight-green {
    border-left-color: #16a34a;
}

.insight-orange {
    border-left-color: #ea580c;
}

.insight-red {
    border-left-color: #dc2626;
}

.insight b {
    color: #0f172a;
}

.question-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 18px 20px;
    height: 100%;
    box-shadow: 0 10px 30px rgba(15,23,42,.06);
}

.question {
    color: #1e293b;
    font-size: 15px;
    font-weight: 900;
    margin-bottom: 8px;
}

.answer {
    color: #475569;
    font-size: 14px;
    line-height: 1.55;
}

.answer strong {
    color: #2563eb;
}

.section-label {
    display: inline-flex;
    background: #dbeafe;
    color: #1d4ed8;
    padding: 6px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.divider {
    height: 1px;
    background: #e2e8f0;
    margin: 18px 0;
}

.footer {
    color: #64748b;
    text-align: center;
    padding: 18px 0;
    border-top: 1px solid #e2e8f0;
    margin-top: 30px;
    font-size: 13px;
}

[data-testid="stTabs"] [role="tablist"] {
    gap: 8px;
}

[data-testid="stTabs"] [role="tab"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 999px;
    padding: 10px 18px;
    color: #334155;
    font-weight: 800;
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: #0f172a;
    color: white;
}

[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 10px 30px rgba(15,23,42,.06);
}

div[data-testid="stMetric"] label {
    color: #64748b !important;
}

div[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-weight: 950;
}

@media (max-width: 768px) {
    .hero-title { font-size: 34px; }
    .hero { padding: 26px 22px; }
    .metric-value { font-size: 26px; }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================
# Utility Functions
# ============================================================

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

PLOTLY_TEMPLATE = "plotly_white"
COLOR_BLUE = "#2563eb"
COLOR_CYAN = "#0891b2"
COLOR_GREEN = "#16a34a"
COLOR_ORANGE = "#ea580c"
COLOR_RED = "#dc2626"
COLOR_GRAY = "#64748b"


def format_count(value: float | int) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f}"


def format_money_million(value: float) -> str:
    """Input is in million USD."""
    if pd.isna(value):
        return "N/A"
    if abs(value) >= 1000:
        return f"${value / 1000:,.2f}B"
    return f"${value:,.2f}M"


def render_metric_card(label: str, value: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight(text: str, color: str = "blue") -> None:
    cls = {
        "blue": "insight",
        "green": "insight insight-green",
        "orange": "insight insight-orange",
        "red": "insight insight-red",
    }.get(color, "insight")

    st.markdown(f"""<div class="{cls}">{text}</div>""", unsafe_allow_html=True)


def render_question(question: str, answer: str) -> None:
    st.markdown(
        f"""
        <div class="question-card">
            <div class="question">{question}</div>
            <div class="answer">{answer}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def fig_layout(fig, height: int = 430):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        font=dict(color="#334155", family="Arial"),
        title=dict(font=dict(size=20, color="#0f172a"), x=0.02, xanchor="left"),
        margin=dict(l=20, r=20, t=70, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e2e8f0", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#e2e8f0", zeroline=False)
    return fig


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    labels: dict | None = None,
    orientation: str = "v",
    height: int = 430,
    color: str = COLOR_BLUE,
    text: str | None = None,
):
    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation=orientation,
        title=title,
        labels=labels or {},
        text=text,
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(marker_color=color, textposition="outside", cliponaxis=False)
    return fig_layout(fig, height)


def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    labels: dict | None = None,
    height: int = 430,
    color: str = COLOR_BLUE,
):
    fig = px.line(
        df,
        x=x,
        y=y,
        title=title,
        markers=True,
        labels=labels or {},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(line=dict(color=color, width=3), marker=dict(size=8, color=color))
    return fig_layout(fig, height)


def donut_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
    height: int = 430,
    colors: list[str] | None = None,
):
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        hole=0.62,
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=colors or [COLOR_BLUE, COLOR_ORANGE, COLOR_GREEN, COLOR_CYAN],
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig_layout(fig, height)


def treemap_chart(df: pd.DataFrame, path: list[str], values: str, title: str, height: int = 500):
    fig = px.treemap(
        df,
        path=path,
        values=values,
        title=title,
        template=PLOTLY_TEMPLATE,
        color=values,
        color_continuous_scale="Blues",
    )
    return fig_layout(fig, height)


def clean_investor_name(name: str) -> str:
    if pd.isna(name):
        return np.nan

    name = str(name).strip()
    name = re.sub(r"\s+", " ", name)
    lower = name.lower()

    mapping = {
        "sequoia india": "Sequoia Capital",
        "sequoia capital india": "Sequoia Capital",
        "sequoia capital india advisors": "Sequoia Capital",
        "accel": "Accel Partners",
        "accel india": "Accel Partners",
        "softbank": "SoftBank",
        "softbank group": "SoftBank",
        "softbank group corp": "SoftBank",
        "softbank vision fund": "SoftBank",
        "softbank corp": "SoftBank",
        "tiger global management": "Tiger Global",
        "saif partners india": "SAIF Partners",
        "idg ventures india": "IDG Ventures",
        "indian angel network (ian)": "Indian Angel Network",
        "nexus ventures": "Nexus Venture Partners",
        "kalaari": "Kalaari Capital",
        "kalaari capital partners": "Kalaari Capital",
        "blume": "Blume Ventures",
        "westbridge capital": "WestBridge Capital",
        "westbridge": "WestBridge Capital",
    }

    return mapping.get(lower, name)


@st.cache_data
def load_data() -> pd.DataFrame:
    possible_paths = [
        Path("data/startup_funding_cleaned.csv"),
        Path("startup_funding_cleaned.csv"),
        Path("./data/startup_funding_cleaned.csv"),
    ]

    data_path = None
    for path in possible_paths:
        if path.exists():
            data_path = path
            break

    if data_path is None:
        st.error(
            "Dataset tidak ditemukan. Pastikan `startup_funding_cleaned.csv` berada di folder `data/`."
        )
        st.stop()

    df = pd.read_csv(data_path)

    # Date
    if "date_clean" in df.columns:
        df["date_clean"] = pd.to_datetime(df["date_clean"], errors="coerce")
    elif "date" in df.columns:
        df["date_clean"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    else:
        df["date_clean"] = pd.NaT

    # Amount
    if "amount_million_usd" not in df.columns:
        if "amount_clean" in df.columns:
            df["amount_million_usd"] = pd.to_numeric(df["amount_clean"], errors="coerce") / 1_000_000
        else:
            df["amount_million_usd"] = np.nan
    else:
        df["amount_million_usd"] = pd.to_numeric(df["amount_million_usd"], errors="coerce")

    # Date features
    if "year" not in df.columns:
        df["year"] = df["date_clean"].dt.year
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    if "month" not in df.columns:
        df["month"] = df["date_clean"].dt.month
    df["month"] = pd.to_numeric(df["month"], errors="coerce").astype("Int64")

    if "month_name" not in df.columns:
        df["month_name"] = df["date_clean"].dt.month_name()

    # Required clean columns
    fallbacks = {
        "startup_name_clean": "startup_name",
        "city_clean": "city",
        "industry_group": "industry",
        "investment_type_clean": "investment_type",
    }

    for col, fallback in fallbacks.items():
        if col not in df.columns:
            if fallback in df.columns:
                df[col] = df[fallback]
            else:
                df[col] = "Unknown"

    for col in ["startup_name_clean", "city_clean", "industry_group", "investment_type_clean"]:
        df[col] = df[col].fillna("Unknown").astype(str)

    return df


# ============================================================
# Load Dataset
# ============================================================

df_all = load_data()


# ============================================================
# Sidebar Filters
# ============================================================

st.sidebar.markdown("## 🚀 Dashboard Filters")
st.sidebar.markdown("Gunakan filter untuk mengeksplorasi data secara interaktif.")

years = sorted([int(y) for y in df_all["year"].dropna().unique()])
if years:
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=min(years),
        max_value=max(years),
        value=(min(years), max(years)),
    )
else:
    year_range = (None, None)

city_options = sorted(df_all.loc[df_all["city_clean"] != "Unknown", "city_clean"].dropna().unique())
industry_options = sorted(df_all.loc[df_all["industry_group"] != "Unknown", "industry_group"].dropna().unique())
investment_options = sorted(df_all.loc[df_all["investment_type_clean"] != "Unknown", "investment_type_clean"].dropna().unique())

selected_cities = st.sidebar.multiselect("Cities", city_options)
selected_industries = st.sidebar.multiselect("Industries", industry_options)
selected_investments = st.sidebar.multiselect("Investment Types", investment_options)

show_unknown = st.sidebar.checkbox("Include Unknown Labels", value=False)

df = df_all.copy()

if year_range[0] is not None:
    df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

if selected_cities:
    df = df[df["city_clean"].isin(selected_cities)]

if selected_industries:
    df = df[df["industry_group"].isin(selected_industries)]

if selected_investments:
    df = df[df["investment_type_clean"].isin(selected_investments)]

if not show_unknown:
    for col in ["city_clean", "industry_group", "investment_type_clean"]:
        df = df[df[col] != "Unknown"]

if df.empty:
    st.warning("Tidak ada data sesuai filter. Silakan ubah pilihan filter.")
    st.stop()


# ============================================================
# Core Aggregations
# ============================================================

funding_df = df[df["amount_million_usd"].notna()].copy()

total_records = len(df)
unique_startups = df["startup_name_clean"].nunique()
valid_amount = len(funding_df)
total_funding = funding_df["amount_million_usd"].sum()
avg_funding = funding_df["amount_million_usd"].mean()
median_funding = funding_df["amount_million_usd"].median()
max_funding = funding_df["amount_million_usd"].max()

if not funding_df.empty:
    q1 = funding_df["amount_million_usd"].quantile(0.25)
    q3 = funding_df["amount_million_usd"].quantile(0.75)
    iqr = q3 - q1
    outlier_upper = q3 + 1.5 * iqr
    outlier_df = funding_df[funding_df["amount_million_usd"] > outlier_upper].copy()
    no_outlier_df = funding_df[funding_df["amount_million_usd"] <= outlier_upper].copy()
    outlier_contribution = outlier_df["amount_million_usd"].sum() / total_funding * 100 if total_funding else 0
else:
    q1 = q3 = iqr = outlier_upper = np.nan
    outlier_df = funding_df
    no_outlier_df = funding_df
    outlier_contribution = 0


# ============================================================
# Header
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">Data Analytics Portfolio Project</div>
        <div class="hero-title">Indian Startup Funding Analysis</div>
        <div class="hero-subtitle">
            Explore how startup funding in India flows across time, cities, industries,
            investment types, investors, and repeat-funded startups — with special attention
            to how outliers can shape the overall funding story.
        </div>
        <span class="badge">Python</span>
        <span class="badge">Pandas</span>
        <span class="badge">Plotly</span>
        <span class="badge">Streamlit</span>
        <span class="badge">EDA</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI Cards
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    render_metric_card("Funding Records", format_count(total_records), f"{format_count(unique_startups)} unique startups")
with kpi2:
    render_metric_card("Total Funding", format_money_million(total_funding), f"{format_count(valid_amount)} valid funding amount records")
with kpi3:
    render_metric_card("Median Funding", format_money_million(median_funding), f"Average: {format_money_million(avg_funding)}")
with kpi4:
    render_metric_card("Outlier Impact", f"{outlier_contribution:.2f}%", f"Threshold: {format_money_million(outlier_upper)}")


# ============================================================
# Tabs
# ============================================================

tabs = st.tabs([
    "🏠 Overview",
    "📈 Trends",
    "🏙️ Cities & Industries",
    "💸 Investment & Investors",
    "🚀 Repeat Funding",
    "⚠️ Outliers",
    "🔎 Data Explorer",
])


# ============================================================
# Overview Tab
# ============================================================

with tabs[0]:
    st.markdown("## Executive Summary")

    left, right = st.columns([1.1, 0.9])

    with left:
        st.markdown(
            """
            <div class="story-card">
                <div class="section-label">Story</div>
                <div class="story-title">Funding volume and funding value tell different stories.</div>
                <div class="story-body">
                This dashboard summarizes the Indian startup funding ecosystem by combining
                frequency-based analysis and value-based analysis. The goal is to avoid misleading
                conclusions from total funding alone, because a small number of very large deals can
                dominate the overall funding value.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_insight(
            "<b>Bengaluru</b> is the strongest startup funding hub, leading both funding count and total funding.",
            "blue",
        )
        render_insight(
            "<b>E-commerce</b> is the leading sector by both number of funding deals and total funding amount.",
            "green",
        )
        render_insight(
            "<b>Seed Funding</b> drives deal volume, while <b>Private Equity</b> drives funding value.",
            "orange",
        )
        render_insight(
            f"<b>Outliers contribute {outlier_contribution:.2f}%</b> of total funding in the selected data.",
            "red",
        )

    with right:
        st.markdown("### Key Questions Answered")

        q1_col, q2_col = st.columns(2)
        with q1_col:
            top_city = df["city_clean"].value_counts().idxmax()
            top_industry = df["industry_group"].value_counts().idxmax()
            render_question("Which city dominates?", f"<strong>{top_city}</strong> leads the startup funding ecosystem.")
            render_question("Which industry leads?", f"<strong>{top_industry}</strong> has the strongest funding activity.")

        with q2_col:
            top_investment_count = df["investment_type_clean"].value_counts().idxmax()
            top_investment_amount = df.groupby("investment_type_clean")["amount_million_usd"].sum().idxmax()
            render_question("Most frequent funding type?", f"<strong>{top_investment_count}</strong> appears most often.")
            render_question("Highest-value funding type?", f"<strong>{top_investment_amount}</strong> contributes the most value.")

    st.markdown("## Dashboard Snapshot")

    yearly = df.groupby("year").agg(
        funding_deals=("startup_name_clean", "count"),
        total_funding=("amount_million_usd", "sum"),
    ).reset_index().sort_values("year")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            line_chart(
                yearly,
                "year",
                "funding_deals",
                "Funding Deal Count by Year",
                {"year": "Year", "funding_deals": "Funding Deals"},
                color=COLOR_BLUE,
            ),
            use_container_width=True,
        )

    with col2:
        st.plotly_chart(
            line_chart(
                yearly,
                "year",
                "total_funding",
                "Total Funding by Year",
                {"year": "Year", "total_funding": "Total Funding, Million USD"},
                color=COLOR_GREEN,
            ),
            use_container_width=True,
        )


# ============================================================
# Trends Tab
# ============================================================

with tabs[1]:
    st.markdown("## Funding Trends Over Time")

    yearly_summary = df.groupby("year").agg(
        funding_deals=("startup_name_clean", "count"),
        unique_startups=("startup_name_clean", "nunique"),
        total_funding=("amount_million_usd", "sum"),
        average_funding=("amount_million_usd", "mean"),
        median_funding=("amount_million_usd", "median"),
    ).reset_index().sort_values("year")

    top_year_deals = yearly_summary.loc[yearly_summary["funding_deals"].idxmax(), "year"]
    top_year_value = yearly_summary.loc[yearly_summary["total_funding"].idxmax(), "year"]

    render_insight(
        f"<b>{top_year_deals}</b> has the highest funding deal count, while <b>{top_year_value}</b> has the highest total funding value. This shows why frequency and value should be analyzed separately.",
        "blue",
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            bar_chart(
                yearly_summary,
                "year",
                "funding_deals",
                "Funding Deals by Year",
                {"year": "Year", "funding_deals": "Funding Deals"},
                color=COLOR_BLUE,
            ),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            bar_chart(
                yearly_summary,
                "year",
                "total_funding",
                "Total Funding by Year",
                {"year": "Year", "total_funding": "Total Funding, Million USD"},
                color=COLOR_GREEN,
            ),
            use_container_width=True,
        )

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(
            line_chart(
                yearly_summary,
                "year",
                "average_funding",
                "Average Funding by Year",
                {"year": "Year", "average_funding": "Average Funding, Million USD"},
                color=COLOR_ORANGE,
            ),
            use_container_width=True,
        )
    with col4:
        st.plotly_chart(
            line_chart(
                yearly_summary,
                "year",
                "median_funding",
                "Median Funding by Year",
                {"year": "Year", "median_funding": "Median Funding, Million USD"},
                color=COLOR_CYAN,
            ),
            use_container_width=True,
        )

    st.markdown("### Monthly Pattern")

    monthly = df.groupby("month_name").agg(
        funding_deals=("startup_name_clean", "count"),
        total_funding=("amount_million_usd", "sum"),
        median_funding=("amount_million_usd", "median"),
    ).reindex(MONTH_ORDER).reset_index()

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(
            bar_chart(
                monthly,
                "month_name",
                "funding_deals",
                "Funding Deals by Month",
                {"month_name": "Month", "funding_deals": "Funding Deals"},
                color=COLOR_BLUE,
            ),
            use_container_width=True,
        )
    with col6:
        st.plotly_chart(
            bar_chart(
                monthly,
                "month_name",
                "total_funding",
                "Total Funding by Month",
                {"month_name": "Month", "total_funding": "Total Funding, Million USD"},
                color=COLOR_GREEN,
            ),
            use_container_width=True,
        )

    st.dataframe(yearly_summary, use_container_width=True, hide_index=True)


# ============================================================
# City & Industry Tab
# ============================================================

with tabs[2]:
    st.markdown("## Cities & Industries")

    city_summary = df.groupby("city_clean").agg(
        funding_deals=("startup_name_clean", "count"),
        unique_startups=("startup_name_clean", "nunique"),
        total_funding=("amount_million_usd", "sum"),
        median_funding=("amount_million_usd", "median"),
    ).reset_index()

    industry_summary = df.groupby("industry_group").agg(
        funding_deals=("startup_name_clean", "count"),
        unique_startups=("startup_name_clean", "nunique"),
        total_funding=("amount_million_usd", "sum"),
        median_funding=("amount_million_usd", "median"),
    ).reset_index()

    render_insight(
        "City and industry analysis reveals concentration: certain cities specialize in specific sectors, and Bengaluru dominates multiple categories.",
        "green",
    )

    col1, col2 = st.columns(2)
    with col1:
        top_city_value = city_summary.sort_values("total_funding", ascending=False).head(12)
        st.plotly_chart(
            bar_chart(
                top_city_value.sort_values("total_funding"),
                "total_funding",
                "city_clean",
                "Top Cities by Total Funding",
                {"city_clean": "City", "total_funding": "Total Funding, Million USD"},
                orientation="h",
                color=COLOR_BLUE,
                height=520,
            ),
            use_container_width=True,
        )

    with col2:
        top_city_count = city_summary.sort_values("funding_deals", ascending=False).head(12)
        st.plotly_chart(
            bar_chart(
                top_city_count.sort_values("funding_deals"),
                "funding_deals",
                "city_clean",
                "Top Cities by Funding Deals",
                {"city_clean": "City", "funding_deals": "Funding Deals"},
                orientation="h",
                color=COLOR_CYAN,
                height=520,
            ),
            use_container_width=True,
        )

    col3, col4 = st.columns(2)
    with col3:
        top_industry_value = industry_summary.sort_values("total_funding", ascending=False).head(12)
        st.plotly_chart(
            bar_chart(
                top_industry_value.sort_values("total_funding"),
                "total_funding",
                "industry_group",
                "Top Industries by Total Funding",
                {"industry_group": "Industry", "total_funding": "Total Funding, Million USD"},
                orientation="h",
                color=COLOR_GREEN,
                height=520,
            ),
            use_container_width=True,
        )

    with col4:
        top_industry_count = industry_summary.sort_values("funding_deals", ascending=False).head(12)
        st.plotly_chart(
            bar_chart(
                top_industry_count.sort_values("funding_deals"),
                "funding_deals",
                "industry_group",
                "Top Industries by Funding Deals",
                {"industry_group": "Industry", "funding_deals": "Funding Deals"},
                orientation="h",
                color=COLOR_ORANGE,
                height=520,
            ),
            use_container_width=True,
        )

    st.markdown("### City × Industry Concentration")

    combo = df.groupby(["city_clean", "industry_group"]).agg(
        funding_deals=("startup_name_clean", "count"),
        unique_startups=("startup_name_clean", "nunique"),
        total_funding=("amount_million_usd", "sum"),
        median_funding=("amount_million_usd", "median"),
    ).reset_index()

    combo_top = combo.sort_values("total_funding", ascending=False).head(15).copy()
    combo_top["city_industry"] = combo_top["city_clean"] + " — " + combo_top["industry_group"]

    st.plotly_chart(
        bar_chart(
            combo_top.sort_values("total_funding"),
            "total_funding",
            "city_industry",
            "Top City–Industry Combinations by Total Funding",
            {"city_industry": "City — Industry", "total_funding": "Total Funding, Million USD"},
            orientation="h",
            color=COLOR_BLUE,
            height=620,
        ),
        use_container_width=True,
    )

    treemap_data = combo.sort_values("total_funding", ascending=False).head(40)
    st.plotly_chart(
        treemap_chart(
            treemap_data,
            ["city_clean", "industry_group"],
            "total_funding",
            "Funding Concentration Treemap",
            height=560,
        ),
        use_container_width=True,
    )


# ============================================================
# Investment & Investors Tab
# ============================================================

with tabs[3]:
    st.markdown("## Investment Type & Investor Analysis")

    investment_summary = df.groupby("investment_type_clean").agg(
        funding_deals=("startup_name_clean", "count"),
        unique_startups=("startup_name_clean", "nunique"),
        total_funding=("amount_million_usd", "sum"),
        average_funding=("amount_million_usd", "mean"),
        median_funding=("amount_million_usd", "median"),
    ).reset_index()

    render_insight(
        "<b>Seed Funding</b> dominates by frequency, while <b>Private Equity</b> dominates by funding value. This shows the difference between early-stage activity and large-scale capital flow.",
        "orange",
    )

    col1, col2 = st.columns(2)
    with col1:
        top_inv_count = investment_summary.sort_values("funding_deals", ascending=False).head(12)
        st.plotly_chart(
            bar_chart(
                top_inv_count.sort_values("funding_deals"),
                "funding_deals",
                "investment_type_clean",
                "Investment Types by Funding Deals",
                {"investment_type_clean": "Investment Type", "funding_deals": "Funding Deals"},
                orientation="h",
                color=COLOR_BLUE,
                height=500,
            ),
            use_container_width=True,
        )

    with col2:
        top_inv_value = investment_summary.sort_values("total_funding", ascending=False).head(12)
        st.plotly_chart(
            bar_chart(
                top_inv_value.sort_values("total_funding"),
                "total_funding",
                "investment_type_clean",
                "Investment Types by Total Funding",
                {"investment_type_clean": "Investment Type", "total_funding": "Total Funding, Million USD"},
                orientation="h",
                color=COLOR_GREEN,
                height=500,
            ),
            use_container_width=True,
        )

    st.markdown("### Investor Analysis")

    investor_base = df[["startup_name_clean", "investors", "amount_million_usd"]].dropna(subset=["investors"]).copy()
    investor_base["investor_name"] = investor_base["investors"].astype(str).str.split(",")
    investor_base = investor_base.explode("investor_name")
    investor_base["investor_name"] = investor_base["investor_name"].astype(str).str.strip()

    invalid = {
        "", "undisclosed", "undisclosed investor", "undisclosed investors",
        "undisclosed angel investors", "group of angel investors",
        "angel investors", "investors"
    }

    investor_base = investor_base[~investor_base["investor_name"].str.lower().isin(invalid)]
    investor_base["investor_name_clean"] = investor_base["investor_name"].apply(clean_investor_name)

    investor_summary = investor_base.groupby("investor_name_clean").agg(
        investment_count=("startup_name_clean", "count"),
        unique_startups=("startup_name_clean", "nunique"),
        total_funding=("amount_million_usd", "sum"),
        median_funding=("amount_million_usd", "median"),
    ).reset_index()

    col3, col4 = st.columns(2)
    with col3:
        top_investor_count = investor_summary.sort_values("investment_count", ascending=False).head(15)
        st.plotly_chart(
            bar_chart(
                top_investor_count.sort_values("investment_count"),
                "investment_count",
                "investor_name_clean",
                "Most Active Investors",
                {"investor_name_clean": "Investor", "investment_count": "Investment Count"},
                orientation="h",
                color=COLOR_CYAN,
                height=560,
            ),
            use_container_width=True,
        )

    with col4:
        top_investor_value = investor_summary.sort_values("total_funding", ascending=False).head(15)
        st.plotly_chart(
            bar_chart(
                top_investor_value.sort_values("total_funding"),
                "total_funding",
                "investor_name_clean",
                "Investors by Associated Total Funding",
                {"investor_name_clean": "Investor", "total_funding": "Total Funding, Million USD"},
                orientation="h",
                color=COLOR_ORANGE,
                height=560,
            ),
            use_container_width=True,
        )

    st.caption(
        "Investor funding value represents the total value of deals involving that investor, not the exact individual contribution."
    )

    st.dataframe(investor_summary.sort_values("investment_count", ascending=False).head(30), use_container_width=True, hide_index=True)


# ============================================================
# Repeat Funding Tab
# ============================================================

with tabs[4]:
    st.markdown("## Repeat-Funded Startups")

    startup_summary = df.groupby("startup_name_clean").agg(
        funding_rounds=("startup_name_clean", "count"),
        total_funding=("amount_million_usd", "sum"),
        average_funding=("amount_million_usd", "mean"),
        median_funding=("amount_million_usd", "median"),
        first_funding=("date_clean", "min"),
        last_funding=("date_clean", "max"),
    ).reset_index()

    repeat = startup_summary[startup_summary["funding_rounds"] > 1].copy()

    render_insight(
        "Repeat funding can indicate stronger investor confidence because a startup is able to attract funding across multiple rounds.",
        "blue",
    )

    col1, col2 = st.columns(2)
    with col1:
        top_repeat_count = repeat.sort_values("funding_rounds", ascending=False).head(15)
        st.plotly_chart(
            bar_chart(
                top_repeat_count.sort_values("funding_rounds"),
                "funding_rounds",
                "startup_name_clean",
                "Top Startups by Repeat Funding Rounds",
                {"startup_name_clean": "Startup", "funding_rounds": "Funding Rounds"},
                orientation="h",
                color=COLOR_BLUE,
                height=560,
            ),
            use_container_width=True,
        )

    with col2:
        top_repeat_value = repeat.sort_values("total_funding", ascending=False).head(15)
        st.plotly_chart(
            bar_chart(
                top_repeat_value.sort_values("total_funding"),
                "total_funding",
                "startup_name_clean",
                "Top Repeat-Funded Startups by Total Funding",
                {"startup_name_clean": "Startup", "total_funding": "Total Funding, Million USD"},
                orientation="h",
                color=COLOR_GREEN,
                height=560,
            ),
            use_container_width=True,
        )

    st.markdown("### Funding History of Selected Startups")

    default_startups = [s for s in ["Ola", "Flipkart", "Paytm", "OYO Rooms", "BYJU'S"] if s in df["startup_name_clean"].unique()]
    selected_startups = st.multiselect(
        "Select startups to compare",
        sorted(df["startup_name_clean"].unique()),
        default=default_startups,
    )

    if selected_startups:
        history = df[df["startup_name_clean"].isin(selected_startups)].sort_values("date_clean")
        fig = px.line(
            history,
            x="date_clean",
            y="amount_million_usd",
            color="startup_name_clean",
            markers=True,
            title="Funding History of Selected Startups",
            labels={
                "date_clean": "Funding Date",
                "amount_million_usd": "Funding Amount, Million USD",
                "startup_name_clean": "Startup",
            },
            template=PLOTLY_TEMPLATE,
        )
        st.plotly_chart(fig_layout(fig, 520), use_container_width=True)

    st.dataframe(repeat.sort_values("funding_rounds", ascending=False).head(40), use_container_width=True, hide_index=True)


# ============================================================
# Outlier Tab
# ============================================================

with tabs[5]:
    st.markdown("## Outlier Impact Analysis")

    render_insight(
        f"<b>Outlier threshold:</b> funding above <b>{format_money_million(outlier_upper)}</b> is categorized as an outlier using the IQR method.",
        "orange",
    )
    render_insight(
        f"<b>Outlier contribution:</b> outliers account for approximately <b>{outlier_contribution:.2f}%</b> of total funding in the selected data.",
        "red",
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Q1", format_money_million(q1))
    with col2:
        st.metric("Q3", format_money_million(q3))
    with col3:
        st.metric("IQR", format_money_million(iqr))
    with col4:
        st.metric("Outlier Records", format_count(len(outlier_df)))

    col5, col6 = st.columns([1.15, 0.85])

    with col5:
        top_deals = funding_df.sort_values("amount_million_usd", ascending=False).head(20).copy()
        top_deals["label"] = top_deals["startup_name_clean"] + " (" + top_deals["year"].astype(str) + ")"

        st.plotly_chart(
            bar_chart(
                top_deals.sort_values("amount_million_usd"),
                "amount_million_usd",
                "label",
                "Top 20 Largest Funding Deals",
                {"label": "Startup", "amount_million_usd": "Funding Amount, Million USD"},
                orientation="h",
                color=COLOR_ORANGE,
                height=650,
            ),
            use_container_width=True,
        )

    with col6:
        comparison = pd.DataFrame({
            "Category": ["Without Outliers", "Outliers"],
            "Funding": [
                no_outlier_df["amount_million_usd"].sum(),
                outlier_df["amount_million_usd"].sum(),
            ],
        })
        st.plotly_chart(
            donut_chart(
                comparison,
                "Category",
                "Funding",
                "Funding Value Split",
                colors=[COLOR_CYAN, COLOR_ORANGE],
                height=410,
            ),
            use_container_width=True,
        )

        stats = pd.DataFrame({
            "Metric": ["Mean", "Median", "Max"],
            "With Outliers": [
                funding_df["amount_million_usd"].mean(),
                funding_df["amount_million_usd"].median(),
                funding_df["amount_million_usd"].max(),
            ],
            "Without Outliers": [
                no_outlier_df["amount_million_usd"].mean(),
                no_outlier_df["amount_million_usd"].median(),
                no_outlier_df["amount_million_usd"].max(),
            ],
        })
        st.dataframe(stats, use_container_width=True, hide_index=True)

    st.markdown("### Top Outlier Records")
    st.dataframe(
        outlier_df.sort_values("amount_million_usd", ascending=False)[[
            "date_clean",
            "startup_name_clean",
            "city_clean",
            "industry_group",
            "investment_type_clean",
            "investors",
            "amount_million_usd",
        ]].head(40),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# Data Explorer Tab
# ============================================================

with tabs[6]:
    st.markdown("## Data Explorer")

    st.markdown(
        """
        <div class="story-card">
            <div class="story-title">Explore the cleaned dataset</div>
            <div class="story-body">
            This table shows the cleaned data after applying the selected filters. You can search,
            sort, and download the filtered data as CSV.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    columns = [
        "date_clean",
        "startup_name_clean",
        "city_clean",
        "industry_group",
        "investment_type_clean",
        "investors",
        "amount_million_usd",
    ]
    columns = [col for col in columns if col in df.columns]

    st.dataframe(
        df[columns].sort_values("date_clean", ascending=False),
        use_container_width=True,
        hide_index=True,
        height=560,
    )

    st.download_button(
        "Download Filtered Data",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_indian_startup_funding.csv",
        mime="text/csv",
    )


# ============================================================
# Footer
# ============================================================

st.markdown(
    """
    <div class="footer">
        Built by Muh. Shafwan Faiq R. • Indian Startup Funding Analysis • Streamlit Data Portfolio
    </div>
    """,
    unsafe_allow_html=True,
)
