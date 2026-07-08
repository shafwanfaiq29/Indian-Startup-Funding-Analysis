
# ============================================================
# Indian Startup Funding Analysis
# Clean & Readable Streamlit Dashboard
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
# CSS — high contrast, readable, no global text override
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1220px;
    }

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
        border-radius: 24px;
        padding: 32px;
        margin-bottom: 22px;
        box-shadow: 0 14px 36px rgba(15, 23, 42, 0.18);
    }

    .hero-kicker {
        color: #bfdbfe;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #ffffff;
        font-size: 44px;
        line-height: 1.08;
        font-weight: 900;
        letter-spacing: -0.04em;
        margin-bottom: 12px;
    }

    .hero-desc {
        color: #e0f2fe;
        font-size: 17px;
        line-height: 1.55;
        max-width: 920px;
    }

    .pill {
        display: inline-block;
        color: #ffffff;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.28);
        border-radius: 999px;
        padding: 6px 12px;
        margin-right: 8px;
        margin-top: 16px;
        font-size: 13px;
        font-weight: 700;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #dbe3ef;
        border-radius: 18px;
        padding: 20px;
        min-height: 132px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    }

    .metric-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 9px;
    }

    .metric-value {
        color: #0f172a;
        font-size: 31px;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 8px;
    }

    .metric-note {
        color: #475569;
        font-size: 13px;
        line-height: 1.4;
    }

    .insight-box {
        background: #ffffff;
        border: 1px solid #dbe3ef;
        border-left: 6px solid #2563eb;
        border-radius: 16px;
        padding: 16px 18px;
        margin-bottom: 12px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
        color: #334155;
        font-size: 15px;
        line-height: 1.6;
    }

    .insight-green { border-left-color: #16a34a; }
    .insight-orange { border-left-color: #ea580c; }
    .insight-red { border-left-color: #dc2626; }

    .section-card {
        background: #ffffff;
        border: 1px solid #dbe3ef;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
        margin-bottom: 14px;
    }

    .section-card h3 {
        color: #0f172a;
        margin-top: 0;
        margin-bottom: 8px;
    }

    .section-card p {
        color: #334155;
        line-height: 1.6;
        margin-bottom: 0;
    }

    .mini-title {
        color: #0f172a;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .mini-body {
        color: #475569;
        font-size: 14px;
        line-height: 1.55;
    }

    .footer {
        margin-top: 30px;
        padding-top: 18px;
        border-top: 1px solid #e2e8f0;
        color: #64748b;
        text-align: center;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dbe3ef;
        border-radius: 16px;
        padding: 16px;
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
    }

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 32px;
        }
        .hero {
            padding: 24px;
        }
        .metric-value {
            font-size: 24px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Helper Functions
# ============================================================

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

BLUE = "#2563eb"
GREEN = "#16a34a"
ORANGE = "#ea580c"
CYAN = "#0891b2"
RED = "#dc2626"
GRAY = "#64748b"


def fmt_num(value) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f}"


def fmt_money(value) -> str:
    """Value is in million USD."""
    if pd.isna(value):
        return "N/A"
    if abs(value) >= 1000:
        return f"${value / 1000:,.2f}B"
    return f"${value:,.2f}M"


def metric_card(label: str, value: str, note: str = ""):
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


def insight(text: str, tone: str = "blue"):
    cls = "insight-box"
    if tone == "green":
        cls += " insight-green"
    elif tone == "orange":
        cls += " insight-orange"
    elif tone == "red":
        cls += " insight-red"

    st.markdown(f"""<div class="{cls}">{text}</div>""", unsafe_allow_html=True)


def style_fig(fig, height=430):
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#334155"),
        title=dict(font=dict(size=20, color="#0f172a"), x=0.02, xanchor="left"),
        margin=dict(l=20, r=20, t=70, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e2e8f0", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#e2e8f0", zeroline=False)
    return fig


def bar_chart(data, x, y, title, labels=None, orientation="v", color=BLUE, height=430):
    fig = px.bar(
        data,
        x=x,
        y=y,
        orientation=orientation,
        title=title,
        labels=labels or {},
        text_auto=True,
        template="plotly_white",
    )
    fig.update_traces(marker_color=color, textposition="outside", cliponaxis=False)
    return style_fig(fig, height)


def line_chart(data, x, y, title, labels=None, color=BLUE, height=430):
    fig = px.line(
        data,
        x=x,
        y=y,
        markers=True,
        title=title,
        labels=labels or {},
        template="plotly_white",
    )
    fig.update_traces(line=dict(color=color, width=3), marker=dict(size=8, color=color))
    return style_fig(fig, height)


def donut_chart(data, names, values, title, height=430):
    fig = px.pie(
        data,
        names=names,
        values=values,
        hole=0.6,
        title=title,
        template="plotly_white",
        color_discrete_sequence=[BLUE, ORANGE, GREEN, CYAN],
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return style_fig(fig, height)


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
def load_data():
    possible_paths = [
        Path("data/startup_funding_cleaned.csv"),
        Path("startup_funding_cleaned.csv"),
    ]

    data_path = None
    for path in possible_paths:
        if path.exists():
            data_path = path
            break

    if data_path is None:
        st.error("Dataset tidak ditemukan. Pastikan file `data/startup_funding_cleaned.csv` tersedia di repository.")
        st.stop()

    df = pd.read_csv(data_path)

    if "date_clean" in df.columns:
        df["date_clean"] = pd.to_datetime(df["date_clean"], errors="coerce")
    elif "date" in df.columns:
        df["date_clean"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    else:
        df["date_clean"] = pd.NaT

    if "amount_million_usd" not in df.columns:
        if "amount_clean" in df.columns:
            df["amount_million_usd"] = pd.to_numeric(df["amount_clean"], errors="coerce") / 1_000_000
        else:
            df["amount_million_usd"] = np.nan
    else:
        df["amount_million_usd"] = pd.to_numeric(df["amount_million_usd"], errors="coerce")

    if "year" not in df.columns:
        df["year"] = df["date_clean"].dt.year
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    if "month_name" not in df.columns:
        df["month_name"] = df["date_clean"].dt.month_name()

    fallback = {
        "startup_name_clean": "startup_name",
        "city_clean": "city",
        "industry_group": "industry",
        "investment_type_clean": "investment_type",
    }

    for clean_col, raw_col in fallback.items():
        if clean_col not in df.columns:
            df[clean_col] = df[raw_col] if raw_col in df.columns else "Unknown"
        df[clean_col] = df[clean_col].fillna("Unknown").astype(str)

    return df


# ============================================================
# Load + Filters
# ============================================================

df_original = load_data()

st.sidebar.title("Dashboard Filters")
st.sidebar.caption("Filter akan memengaruhi grafik dan KPI utama.")

years = sorted([int(y) for y in df_original["year"].dropna().unique()])
year_range = st.sidebar.slider(
    "Year range",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years)),
)

city_options = sorted(df_original.loc[df_original["city_clean"] != "Unknown", "city_clean"].dropna().unique())
industry_options = sorted(df_original.loc[df_original["industry_group"] != "Unknown", "industry_group"].dropna().unique())
investment_options = sorted(df_original.loc[df_original["investment_type_clean"] != "Unknown", "investment_type_clean"].dropna().unique())

selected_cities = st.sidebar.multiselect("Cities", city_options)
selected_industries = st.sidebar.multiselect("Industries", industry_options)
selected_investments = st.sidebar.multiselect("Investment types", investment_options)
include_unknown = st.sidebar.checkbox("Include Unknown labels", value=False)

df = df_original.copy()
df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

if selected_cities:
    df = df[df["city_clean"].isin(selected_cities)]

if selected_industries:
    df = df[df["industry_group"].isin(selected_industries)]

if selected_investments:
    df = df[df["investment_type_clean"].isin(selected_investments)]

if not include_unknown:
    for col in ["city_clean", "industry_group", "investment_type_clean"]:
        df = df[df[col] != "Unknown"]

if df.empty:
    st.warning("Tidak ada data berdasarkan filter yang dipilih.")
    st.stop()

funding_df = df[df["amount_million_usd"].notna()].copy()

total_records = len(df)
unique_startups = df["startup_name_clean"].nunique()
valid_amount = len(funding_df)
total_funding = funding_df["amount_million_usd"].sum()
avg_funding = funding_df["amount_million_usd"].mean()
median_funding = funding_df["amount_million_usd"].median()
largest_deal = funding_df["amount_million_usd"].max()

if len(funding_df) > 0:
    q1 = funding_df["amount_million_usd"].quantile(0.25)
    q3 = funding_df["amount_million_usd"].quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + 1.5 * iqr
    outlier_df = funding_df[funding_df["amount_million_usd"] > upper_bound]
    no_outlier_df = funding_df[funding_df["amount_million_usd"] <= upper_bound]
    outlier_contribution = (outlier_df["amount_million_usd"].sum() / total_funding * 100) if total_funding else 0
else:
    q1 = q3 = iqr = upper_bound = np.nan
    outlier_df = funding_df
    no_outlier_df = funding_df
    outlier_contribution = 0


# ============================================================
# Header
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Data Analytics Portfolio Project</div>
        <div class="hero-title">Indian Startup Funding Analysis</div>
        <div class="hero-desc">
            Interactive dashboard to explore startup funding trends in India across time, cities,
            industries, investment types, investors, repeat-funded startups, and outlier impact.
        </div>
        <span class="pill">Python</span>
        <span class="pill">Pandas</span>
        <span class="pill">Plotly</span>
        <span class="pill">Streamlit</span>
        <span class="pill">EDA</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI Section
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Funding records", fmt_num(total_records), f"{fmt_num(unique_startups)} unique startups")
with c2:
    metric_card("Total funding", fmt_money(total_funding), f"{fmt_num(valid_amount)} records with valid amount")
with c3:
    metric_card("Median funding", fmt_money(median_funding), f"Average: {fmt_money(avg_funding)}")
with c4:
    metric_card("Outlier contribution", f"{outlier_contribution:.2f}%", f"Threshold: {fmt_money(upper_bound)}")


# ============================================================
# Tabs
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Time Trends",
    "Cities & Industries",
    "Investors & Startups",
    "Outliers",
    "Data"
])


# ============================================================
# Overview
# ============================================================

with tab1:
    st.subheader("Executive Overview")

    col_a, col_b = st.columns([1.1, 0.9])

    with col_a:
        st.markdown(
            """
            <div class="section-card">
                <h3>What this dashboard shows</h3>
                <p>
                    This dashboard analyzes Indian startup funding data to understand how funding patterns differ
                    across time, cities, industries, investment types, investors, and repeat-funded startups.
                    The main story is that <b>funding frequency</b> and <b>funding value</b> can lead to different insights.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        insight("<b>Bengaluru</b> is the most dominant startup funding hub.", "blue")
        insight("<b>E-commerce</b> leads by both funding count and total funding.", "green")
        insight("<b>Seed Funding</b> is most frequent, but <b>Private Equity</b> contributes the largest funding value.", "orange")
        insight(f"<b>Outliers contribute {outlier_contribution:.2f}%</b> of total funding in the selected data.", "red")

    with col_b:
        top_city = df["city_clean"].value_counts().idxmax()
        top_industry = df["industry_group"].value_counts().idxmax()
        top_investment_count = df["investment_type_clean"].value_counts().idxmax()
        top_investment_value = df.groupby("investment_type_clean")["amount_million_usd"].sum().idxmax()

        summary_table = pd.DataFrame({
            "Question": [
                "Top city by frequency",
                "Top industry by frequency",
                "Most frequent investment type",
                "Highest-value investment type",
                "Outlier contribution"
            ],
            "Answer": [
                top_city,
                top_industry,
                top_investment_count,
                top_investment_value,
                f"{outlier_contribution:.2f}%"
            ]
        })

        st.dataframe(summary_table, use_container_width=True, hide_index=True)

    st.subheader("Quick Visual Summary")

    yearly = df.groupby("year").agg(
        funding_deals=("startup_name_clean", "count"),
        total_funding=("amount_million_usd", "sum")
    ).reset_index().sort_values("year")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            line_chart(
                yearly,
                "year",
                "funding_deals",
                "Funding Deals by Year",
                {"year": "Year", "funding_deals": "Funding Deals"},
                BLUE
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
                GREEN
            ),
            use_container_width=True,
        )


# ============================================================
# Time Trends
# ============================================================

with tab2:
    st.subheader("Funding Trends Over Time")

    yearly_summary = df.groupby("year").agg(
        funding_deals=("startup_name_clean", "count"),
        unique_startups=("startup_name_clean", "nunique"),
        total_funding=("amount_million_usd", "sum"),
        average_funding=("amount_million_usd", "mean"),
        median_funding=("amount_million_usd", "median"),
    ).reset_index().sort_values("year")

    top_deal_year = yearly_summary.loc[yearly_summary["funding_deals"].idxmax(), "year"]
    top_value_year = yearly_summary.loc[yearly_summary["total_funding"].idxmax(), "year"]

    insight(
        f"The highest number of funding deals occurred in <b>{top_deal_year}</b>, "
        f"while the highest total funding occurred in <b>{top_value_year}</b>. "
        "This shows that deal volume and funding value tell different stories.",
        "blue"
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
                color=BLUE
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
                color=GREEN
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
                ORANGE
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
                CYAN
            ),
            use_container_width=True,
        )

    st.markdown("### Monthly Funding Pattern")

    monthly = df.groupby("month_name").agg(
        funding_deals=("startup_name_clean", "count"),
        total_funding=("amount_million_usd", "sum"),
        median_funding=("amount_million_usd", "median")
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
                color=BLUE
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
                color=GREEN
            ),
            use_container_width=True,
        )

    st.dataframe(yearly_summary, use_container_width=True, hide_index=True)


# ============================================================
# Cities & Industries
# ============================================================

with tab3:
    st.subheader("Cities & Industries")

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

    insight(
        "Bengaluru dominates the startup funding map, while E-commerce leads as the strongest industry.",
        "green"
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
                color=BLUE,
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
                color=CYAN,
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
                color=GREEN,
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
                color=ORANGE,
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
            color=BLUE,
            height=620,
        ),
        use_container_width=True,
    )


# ============================================================
# Investors & Startups
# ============================================================

with tab4:
    st.subheader("Investor and Startup Analysis")

    investment_summary = df.groupby("investment_type_clean").agg(
        funding_deals=("startup_name_clean", "count"),
        total_funding=("amount_million_usd", "sum"),
        median_funding=("amount_million_usd", "median")
    ).reset_index()

    insight(
        "Seed Funding appears most frequently, while Private Equity contributes the largest total funding.",
        "orange"
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
                color=BLUE,
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
                color=GREEN,
                height=500,
            ),
            use_container_width=True,
        )

    st.markdown("### Investor Activity")

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
                color=CYAN,
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
                "Investors by Associated Funding Value",
                {"investor_name_clean": "Investor", "total_funding": "Total Funding, Million USD"},
                orientation="h",
                color=ORANGE,
                height=560,
            ),
            use_container_width=True,
        )

    st.caption(
        "Investor funding value represents the total value of deals involving that investor, not the exact individual contribution."
    )

    st.markdown("### Repeat-Funded Startups")

    startup_summary = df.groupby("startup_name_clean").agg(
        funding_rounds=("startup_name_clean", "count"),
        total_funding=("amount_million_usd", "sum"),
        median_funding=("amount_million_usd", "median"),
        first_funding=("date_clean", "min"),
        last_funding=("date_clean", "max"),
    ).reset_index()

    repeat = startup_summary[startup_summary["funding_rounds"] > 1].copy()

    col5, col6 = st.columns(2)
    with col5:
        top_repeat_count = repeat.sort_values("funding_rounds", ascending=False).head(15)
        st.plotly_chart(
            bar_chart(
                top_repeat_count.sort_values("funding_rounds"),
                "funding_rounds",
                "startup_name_clean",
                "Top Startups by Repeat Funding Rounds",
                {"startup_name_clean": "Startup", "funding_rounds": "Funding Rounds"},
                orientation="h",
                color=BLUE,
                height=560,
            ),
            use_container_width=True,
        )
    with col6:
        top_repeat_value = repeat.sort_values("total_funding", ascending=False).head(15)
        st.plotly_chart(
            bar_chart(
                top_repeat_value.sort_values("total_funding"),
                "total_funding",
                "startup_name_clean",
                "Top Repeat-Funded Startups by Total Funding",
                {"startup_name_clean": "Startup", "total_funding": "Total Funding, Million USD"},
                orientation="h",
                color=GREEN,
                height=560,
            ),
            use_container_width=True,
        )


# ============================================================
# Outliers
# ============================================================

with tab5:
    st.subheader("Outlier Impact Analysis")

    insight(
        f"Using the IQR method, funding above <b>{fmt_money(upper_bound)}</b> is categorized as an outlier.",
        "orange"
    )
    insight(
        f"Outliers contribute approximately <b>{outlier_contribution:.2f}%</b> of total funding, meaning total funding is heavily shaped by a small number of very large deals.",
        "red"
    )

    o1, o2, o3, o4 = st.columns(4)
    with o1:
        st.metric("Q1", fmt_money(q1))
    with o2:
        st.metric("Q3", fmt_money(q3))
    with o3:
        st.metric("IQR", fmt_money(iqr))
    with o4:
        st.metric("Outlier Records", fmt_num(len(outlier_df)))

    col1, col2 = st.columns([1.15, 0.85])

    with col1:
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
                color=ORANGE,
                height=650,
            ),
            use_container_width=True,
        )

    with col2:
        split = pd.DataFrame({
            "Category": ["Without Outliers", "Outliers"],
            "Funding": [
                no_outlier_df["amount_million_usd"].sum(),
                outlier_df["amount_million_usd"].sum()
            ]
        })

        st.plotly_chart(
            donut_chart(
                split,
                "Category",
                "Funding",
                "Funding Split: Outliers vs Non-Outliers",
                height=420
            ),
            use_container_width=True,
        )

        stats = pd.DataFrame({
            "Metric": ["Mean", "Median", "Max"],
            "With Outliers": [
                funding_df["amount_million_usd"].mean(),
                funding_df["amount_million_usd"].median(),
                funding_df["amount_million_usd"].max()
            ],
            "Without Outliers": [
                no_outlier_df["amount_million_usd"].mean(),
                no_outlier_df["amount_million_usd"].median(),
                no_outlier_df["amount_million_usd"].max()
            ]
        })
        st.dataframe(stats, use_container_width=True, hide_index=True)

    st.markdown("### Top Outlier Deals")
    st.dataframe(
        outlier_df.sort_values("amount_million_usd", ascending=False)[[
            "date_clean",
            "startup_name_clean",
            "city_clean",
            "industry_group",
            "investment_type_clean",
            "investors",
            "amount_million_usd"
        ]].head(40),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# Data
# ============================================================

with tab6:
    st.subheader("Data Explorer")

    st.markdown(
        """
        <div class="section-card">
            <h3>Cleaned Dataset</h3>
            <p>
                This table shows the cleaned dataset after applying the selected filters.
                You can sort, explore, and download the filtered data.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    columns = [
        "date_clean",
        "startup_name_clean",
        "city_clean",
        "industry_group",
        "investment_type_clean",
        "investors",
        "amount_million_usd"
    ]
    columns = [c for c in columns if c in df.columns]

    st.dataframe(
        df[columns].sort_values("date_clean", ascending=False),
        use_container_width=True,
        hide_index=True,
        height=560
    )

    st.download_button(
        "Download Filtered Data",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_indian_startup_funding.csv",
        mime="text/csv"
    )


st.markdown(
    """
    <div class="footer">
        Indian Startup Funding Analysis • Built with Streamlit • Data Analytics Portfolio
    </div>
    """,
    unsafe_allow_html=True
)
