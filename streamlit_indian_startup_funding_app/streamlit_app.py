import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Indian Startup Funding Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>
    .main { background-color: #0f172a; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { color: #f8fafc; font-weight: 800; }
    p, li, span, div { color: #cbd5e1; }
    [data-testid="stSidebar"] { background-color: #111827; }
    .hero-card {
        background: linear-gradient(135deg, #111827 0%, #1e293b 55%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 24px;
        padding: 30px 34px;
        margin-bottom: 22px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    }
    .hero-title {
        font-size: 44px;
        line-height: 1.1;
        color: #f8fafc;
        font-weight: 900;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 17px;
        color: #cbd5e1;
        max-width: 1050px;
    }
    .tag {
        display: inline-block;
        background: rgba(56,189,248,0.12);
        color: #7dd3fc;
        border: 1px solid rgba(56,189,248,0.35);
        border-radius: 999px;
        padding: 6px 12px;
        margin-right: 8px;
        margin-top: 14px;
        font-size: 13px;
        font-weight: 600;
    }
    .metric-card {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 18px 20px;
        min-height: 126px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.18);
    }
    .metric-label {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 30px;
        line-height: 1.15;
        font-weight: 900;
    }
    .metric-note { color: #94a3b8; font-size: 13px; margin-top: 8px; }
    .insight-card {
        background: #111827;
        border: 1px solid #334155;
        border-left: 5px solid #38bdf8;
        border-radius: 16px;
        padding: 18px 20px;
        margin-bottom: 12px;
    }
    .warning-card {
        background: rgba(251, 146, 60, 0.10);
        border: 1px solid rgba(251, 146, 60, 0.45);
        border-left: 5px solid #fb923c;
        border-radius: 16px;
        padding: 18px 20px;
        margin-bottom: 12px;
    }
    .section-card {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 22px 24px;
        margin-bottom: 18px;
    }
    .footer {
        color: #94a3b8;
        font-size: 13px;
        text-align: center;
        margin-top: 24px;
        padding-top: 18px;
        border-top: 1px solid #334155;
    }
    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #334155;
        padding: 16px;
        border-radius: 18px;
    }
    div[data-testid="stMetric"] label { color: #94a3b8 !important; }
    div[data-testid="stMetricValue"] { color: #f8fafc !important; font-weight: 900; }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# Helper Functions
# ============================================================

def format_usd_million(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    if abs(value) >= 1000:
        return f"${value / 1000:,.2f}B"
    return f"${value:,.2f}M"


def format_number(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f}"


def metric_card(label: str, value: str, note: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


@st.cache_data
def load_data() -> pd.DataFrame:
    possible_paths = [
        Path("data/startup_funding_cleaned.csv"),
        Path("startup_funding_cleaned.csv"),
        Path("data/startup_funding.csv"),
        Path("startup_funding.csv"),
    ]

    data_path = None
    for path in possible_paths:
        if path.exists():
            data_path = path
            break

    if data_path is None:
        st.error(
            "Dataset tidak ditemukan. Pastikan file `startup_funding_cleaned.csv` ada di folder `data/` atau root repository."
        )
        st.stop()

    df = pd.read_csv(data_path)

    if "date_clean" in df.columns:
        df["date_clean"] = pd.to_datetime(df["date_clean"], errors="coerce")
    elif "date" in df.columns:
        df["date_clean"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    else:
        df["date_clean"] = pd.NaT

    if "year" not in df.columns:
        df["year"] = df["date_clean"].dt.year
    if "month" not in df.columns:
        df["month"] = df["date_clean"].dt.month
    if "month_name" not in df.columns:
        df["month_name"] = df["date_clean"].dt.month_name()

    if "amount_million_usd" not in df.columns:
        if "amount_clean" in df.columns:
            df["amount_million_usd"] = pd.to_numeric(df["amount_clean"], errors="coerce") / 1_000_000
        else:
            df["amount_million_usd"] = np.nan

    fallback_columns = {
        "startup_name_clean": "startup_name",
        "city_clean": "city",
        "industry_group": "industry",
        "investment_type_clean": "investment_type",
    }
    for clean_col, fallback_col in fallback_columns.items():
        if clean_col not in df.columns:
            df[clean_col] = df[fallback_col] if fallback_col in df.columns else "Unknown"

    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["amount_million_usd"] = pd.to_numeric(df["amount_million_usd"], errors="coerce")
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown("## Filter Dashboard")

    valid_years = sorted([int(y) for y in df["year"].dropna().unique()])
    if valid_years:
        year_range = st.sidebar.slider(
            "Rentang Tahun",
            min_value=min(valid_years),
            max_value=max(valid_years),
            value=(min(valid_years), max(valid_years)),
        )
        df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    city_options = sorted(df["city_clean"].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect("Pilih Kota", city_options, default=[])
    if selected_cities:
        df = df[df["city_clean"].isin(selected_cities)]

    industry_options = sorted(df["industry_group"].dropna().unique().tolist())
    selected_industries = st.sidebar.multiselect("Pilih Industri", industry_options, default=[])
    if selected_industries:
        df = df[df["industry_group"].isin(selected_industries)]

    investment_options = sorted(df["investment_type_clean"].dropna().unique().tolist())
    selected_investments = st.sidebar.multiselect("Pilih Jenis Investasi", investment_options, default=[])
    if selected_investments:
        df = df[df["investment_type_clean"].isin(selected_investments)]

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Catatan: amount disimpan dalam juta USD. Nilai amount kosong tetap dihitung pada analisis frekuensi."
    )
    return df


def style_fig(fig, height=430):
    fig.update_layout(
        height=height,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font_color="#cbd5e1",
        title_font_color="#f8fafc",
        title_font_size=20,
        margin=dict(l=20, r=20, t=70, b=30),
    )
    return fig


def make_bar(data, x, y, title, labels=None, orientation="v", height=430, color="#38bdf8"):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        labels=labels,
        orientation=orientation,
        text_auto=True,
        template="plotly_dark",
    )
    fig.update_traces(marker_color=color)
    return style_fig(fig, height)


def make_line(data, x, y, title, labels=None, height=430):
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        labels=labels,
        markers=True,
        template="plotly_dark",
    )
    fig.update_traces(line_color="#38bdf8", marker_color="#7dd3fc")
    return style_fig(fig, height)


# ============================================================
# Load Data
# ============================================================

df_raw = load_data()
df = apply_filters(df_raw)

if df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
    st.stop()

funding_with_amount = df[df["amount_million_usd"].notnull()].copy()

if not funding_with_amount.empty:
    q1 = funding_with_amount["amount_million_usd"].quantile(0.25)
    q3 = funding_with_amount["amount_million_usd"].quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + 1.5 * iqr
    outlier_df = funding_with_amount[funding_with_amount["amount_million_usd"] > upper_bound].copy()
    no_outlier_df = funding_with_amount[funding_with_amount["amount_million_usd"] <= upper_bound].copy()
else:
    q1 = q3 = iqr = upper_bound = np.nan
    outlier_df = funding_with_amount
    no_outlier_df = funding_with_amount


# ============================================================
# Header and KPI
# ============================================================

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">Indian Startup Funding Analysis</div>
        <div class="hero-subtitle">
            Dashboard interaktif untuk mengeksplorasi tren pendanaan startup India berdasarkan waktu,
            kota, industri, jenis investasi, investor, repeat funding, dan pengaruh outlier.
        </div>
        <span class="tag">Python</span>
        <span class="tag">Pandas</span>
        <span class="tag">Plotly</span>
        <span class="tag">Streamlit</span>
        <span class="tag">EDA Portfolio</span>
    </div>
    """,
    unsafe_allow_html=True
)

total_records = len(df)
unique_startups = df["startup_name_clean"].nunique()
valid_amount_count = funding_with_amount.shape[0]
total_funding = funding_with_amount["amount_million_usd"].sum()
avg_funding = funding_with_amount["amount_million_usd"].mean()
median_funding = funding_with_amount["amount_million_usd"].median()
largest_funding = funding_with_amount["amount_million_usd"].max()
outlier_contribution = (
    outlier_df["amount_million_usd"].sum() / total_funding * 100
    if total_funding and not outlier_df.empty else 0
)

k1, k2, k3, k4 = st.columns(4)
with k1:
    metric_card("Funding Records", format_number(total_records), f"{format_number(unique_startups)} unique startups")
with k2:
    metric_card("Total Funding", format_usd_million(total_funding), f"{format_number(valid_amount_count)} valid amount records")
with k3:
    metric_card("Median Funding", format_usd_million(median_funding), f"Average: {format_usd_million(avg_funding)}")
with k4:
    metric_card("Outlier Contribution", f"{outlier_contribution:.2f}%", f"Largest deal: {format_usd_million(largest_funding)}")


# ============================================================
# Tabs
# ============================================================

tab_overview, tab_trends, tab_city_industry, tab_investors, tab_outliers, tab_data = st.tabs([
    "Executive Overview",
    "Tren Waktu",
    "Kota & Industri",
    "Investor & Startup",
    "Outlier Analysis",
    "Data Explorer"
])


# ============================================================
# Executive Overview
# ============================================================

with tab_overview:
    st.markdown("## Executive Overview")

    col_left, col_right = st.columns([1.15, 0.85])

    with col_left:
        st.markdown(
            """
            <div class="section-card">
            <h3>Inti Analisis</h3>
            <p>
            Project ini menganalisis data pendanaan startup India untuk memahami perbedaan antara
            <b>jumlah deal</b> dan <b>nilai funding</b>. Insight utama menunjukkan bahwa total funding
            sangat dipengaruhi oleh beberapa deal bernilai besar, sehingga analisis perlu dibaca dari
            dua sisi: frekuensi dan nilai pendanaan.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="insight-card"><b>City:</b> Bengaluru adalah pusat utama ekosistem pendanaan startup India.</div>
            <div class="insight-card"><b>Industry:</b> E-commerce menjadi sektor paling dominan berdasarkan jumlah funding dan total funding.</div>
            <div class="insight-card"><b>Investment:</b> Seed Funding paling sering muncul, sedangkan Private Equity menyumbang nilai terbesar.</div>
            <div class="warning-card"><b>Outlier:</b> Sebagian besar total funding dipengaruhi oleh sejumlah kecil deal besar.</div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        findings = pd.DataFrame({
            "Aspek": [
                "Kota dominan",
                "Industri dominan",
                "Jenis investasi paling sering",
                "Jenis investasi terbesar",
                "Investor paling aktif",
                "Investor nilai terbesar",
                "Repeat funding terbanyak",
                "Repeat funding terbesar"
            ],
            "Hasil": [
                df["city_clean"].value_counts().idxmax() if df["city_clean"].notna().any() else "N/A",
                df["industry_group"].value_counts().idxmax() if df["industry_group"].notna().any() else "N/A",
                df["investment_type_clean"].value_counts().idxmax() if df["investment_type_clean"].notna().any() else "N/A",
                df.groupby("investment_type_clean")["amount_million_usd"].sum().idxmax(),
                "Sequoia Capital",
                "SoftBank",
                "Ola",
                "Flipkart"
            ]
        })
        st.dataframe(findings, use_container_width=True, hide_index=True)

    st.markdown("## Ringkasan Visual")
    yearly = df.groupby("year", dropna=True).agg(
        jumlah_funding=("startup_name_clean", "count"),
        total_funding_juta_usd=("amount_million_usd", "sum")
    ).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            make_bar(yearly, "year", "jumlah_funding", "Jumlah Funding per Tahun", {"year": "Tahun", "jumlah_funding": "Jumlah Funding"}),
            use_container_width=True
        )
    with c2:
        st.plotly_chart(
            make_bar(yearly, "year", "total_funding_juta_usd", "Total Funding per Tahun", {"year": "Tahun", "total_funding_juta_usd": "Total Funding, Juta USD"}),
            use_container_width=True
        )


# ============================================================
# Time Trends
# ============================================================

with tab_trends:
    st.markdown("## Tren Funding Berdasarkan Waktu")

    yearly_summary = df.groupby("year", dropna=True).agg(
        jumlah_funding=("startup_name_clean", "count"),
        jumlah_startup_unik=("startup_name_clean", "nunique"),
        total_funding_juta_usd=("amount_million_usd", "sum"),
        rata_rata_funding_juta_usd=("amount_million_usd", "mean"),
        median_funding_juta_usd=("amount_million_usd", "median")
    ).reset_index().sort_values("year")

    if not yearly_summary.empty:
        top_year_count = yearly_summary.loc[yearly_summary["jumlah_funding"].idxmax(), "year"]
        top_year_amount = yearly_summary.loc[yearly_summary["total_funding_juta_usd"].idxmax(), "year"]
        st.markdown(
            f"""
            <div class="insight-card">
            <b>Insight:</b> Tahun dengan jumlah funding terbanyak adalah <b>{top_year_count}</b>,
            sedangkan tahun dengan total funding terbesar adalah <b>{top_year_amount}</b>.
            Ini menunjukkan bahwa <b>frequency ≠ value</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(make_line(yearly_summary, "year", "jumlah_funding", "Tren Jumlah Funding per Tahun"), use_container_width=True)
    with c2:
        st.plotly_chart(make_line(yearly_summary, "year", "total_funding_juta_usd", "Tren Total Funding per Tahun"), use_container_width=True)

    st.dataframe(yearly_summary, use_container_width=True, hide_index=True)

    st.markdown("### Pola Bulanan")
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    monthly = df.groupby("month_name").agg(
        jumlah_funding=("startup_name_clean", "count"),
        total_funding_juta_usd=("amount_million_usd", "sum"),
        median_funding_juta_usd=("amount_million_usd", "median")
    ).reindex(month_order).reset_index()

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(make_bar(monthly, "month_name", "jumlah_funding", "Jumlah Funding Berdasarkan Bulan"), use_container_width=True)
    with c4:
        st.plotly_chart(make_bar(monthly, "month_name", "total_funding_juta_usd", "Total Funding Berdasarkan Bulan"), use_container_width=True)


# ============================================================
# City and Industry
# ============================================================

with tab_city_industry:
    st.markdown("## Analisis Kota dan Industri")
    st.markdown(
        """
        <div class="insight-card">
        <b>Insight:</b> Bengaluru menjadi pusat utama funding startup, sedangkan E-commerce menjadi sektor
        paling kuat dari sisi frekuensi maupun total funding.
        </div>
        """,
        unsafe_allow_html=True
    )

    city_summary = df.groupby("city_clean").agg(
        jumlah_funding=("startup_name_clean", "count"),
        jumlah_startup_unik=("startup_name_clean", "nunique"),
        total_funding_juta_usd=("amount_million_usd", "sum"),
        median_funding_juta_usd=("amount_million_usd", "median")
    ).reset_index()

    industry_summary = df.groupby("industry_group").agg(
        jumlah_funding=("startup_name_clean", "count"),
        jumlah_startup_unik=("startup_name_clean", "nunique"),
        total_funding_juta_usd=("amount_million_usd", "sum"),
        median_funding_juta_usd=("amount_million_usd", "median")
    ).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            make_bar(city_summary.sort_values("total_funding_juta_usd", ascending=False).head(10), "total_funding_juta_usd", "city_clean", "Top Kota berdasarkan Total Funding", orientation="h"),
            use_container_width=True
        )
    with c2:
        st.plotly_chart(
            make_bar(city_summary.sort_values("jumlah_funding", ascending=False).head(10), "jumlah_funding", "city_clean", "Top Kota berdasarkan Jumlah Funding", orientation="h"),
            use_container_width=True
        )

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(
            make_bar(industry_summary.sort_values("total_funding_juta_usd", ascending=False).head(10), "total_funding_juta_usd", "industry_group", "Top Industri berdasarkan Total Funding", orientation="h"),
            use_container_width=True
        )
    with c4:
        st.plotly_chart(
            make_bar(industry_summary.sort_values("jumlah_funding", ascending=False).head(10), "jumlah_funding", "industry_group", "Top Industri berdasarkan Jumlah Funding", orientation="h"),
            use_container_width=True
        )

    st.markdown("### Kombinasi Kota dan Industri")
    combo = df.groupby(["city_clean", "industry_group"]).agg(
        jumlah_funding=("startup_name_clean", "count"),
        total_funding_juta_usd=("amount_million_usd", "sum"),
        median_funding_juta_usd=("amount_million_usd", "median")
    ).reset_index().sort_values("total_funding_juta_usd", ascending=False)
    top_combo = combo.head(15).copy()
    top_combo["label"] = top_combo["city_clean"] + " - " + top_combo["industry_group"]
    st.plotly_chart(make_bar(top_combo, "total_funding_juta_usd", "label", "Top Kombinasi Kota-Industri berdasarkan Total Funding", orientation="h", height=560), use_container_width=True)
    st.dataframe(combo.head(30), use_container_width=True, hide_index=True)


# ============================================================
# Investors and Startups
# ============================================================

with tab_investors:
    st.markdown("## Analisis Investor dan Repeat-Funded Startup")
    st.markdown(
        """
        <div class="insight-card">
        <b>Insight:</b> Sequoia Capital unggul dari sisi frekuensi investasi, sedangkan SoftBank lebih dominan
        pada deal bernilai besar. Ini menunjukkan bahwa investor paling aktif tidak selalu sama dengan investor bernilai terbesar.
        </div>
        """,
        unsafe_allow_html=True
    )

    investor_df = df[["startup_name_clean", "investors", "amount_million_usd"]].dropna(subset=["investors"]).copy()
    investor_df["investor_name"] = investor_df["investors"].astype(str).str.split(",")
    investor_df = investor_df.explode("investor_name")
    investor_df["investor_name"] = investor_df["investor_name"].astype(str).str.strip()
    invalid = {"undisclosed", "undisclosed investor", "undisclosed investors", "group of angel investors", "angel investors", "investors", ""}
    investor_df = investor_df[~investor_df["investor_name"].str.lower().isin(invalid)]
    mapping = {
        "sequoia india": "Sequoia Capital",
        "sequoia capital india": "Sequoia Capital",
        "sequoia capital india advisors": "Sequoia Capital",
        "accel india": "Accel Partners",
        "accel": "Accel Partners",
        "softbank": "SoftBank",
        "softbank group": "SoftBank",
        "softbank vision fund": "SoftBank",
        "softbank corp": "SoftBank",
        "softbank group corp": "SoftBank",
        "tiger global management": "Tiger Global",
        "idg ventures india": "IDG Ventures",
        "saif partners india": "SAIF Partners",
        "kalaari": "Kalaari Capital",
        "blume": "Blume Ventures",
        "nexus ventures": "Nexus Venture Partners",
        "westbridge capital": "WestBridge Capital",
    }
    investor_df["investor_name_clean"] = investor_df["investor_name"].str.lower().map(mapping).fillna(investor_df["investor_name"])
    investor_summary = investor_df.groupby("investor_name_clean").agg(
        jumlah_investasi=("startup_name_clean", "count"),
        jumlah_startup_unik=("startup_name_clean", "nunique"),
        total_funding_juta_usd=("amount_million_usd", "sum"),
        median_funding_juta_usd=("amount_million_usd", "median")
    ).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(make_bar(investor_summary.sort_values("jumlah_investasi", ascending=False).head(15), "jumlah_investasi", "investor_name_clean", "Top Investor berdasarkan Jumlah Investasi", orientation="h", height=540), use_container_width=True)
    with c2:
        st.plotly_chart(make_bar(investor_summary.sort_values("total_funding_juta_usd", ascending=False).head(15), "total_funding_juta_usd", "investor_name_clean", "Top Investor berdasarkan Total Funding", orientation="h", height=540), use_container_width=True)

    st.caption("Catatan: total funding investor dihitung berdasarkan nilai deal yang melibatkan investor tersebut, bukan kontribusi pasti masing-masing investor.")

    st.markdown("### Repeat-Funded Startups")
    startup_summary = df.groupby("startup_name_clean").agg(
        jumlah_funding=("startup_name_clean", "count"),
        total_funding_juta_usd=("amount_million_usd", "sum"),
        median_funding_juta_usd=("amount_million_usd", "median"),
        funding_pertama=("date_clean", "min"),
        funding_terakhir=("date_clean", "max")
    ).reset_index()
    repeat_startups = startup_summary[startup_summary["jumlah_funding"] > 1].copy()

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(make_bar(repeat_startups.sort_values("jumlah_funding", ascending=False).head(15), "jumlah_funding", "startup_name_clean", "Top Startup berdasarkan Repeat Funding", orientation="h", height=540), use_container_width=True)
    with c4:
        st.plotly_chart(make_bar(repeat_startups.sort_values("total_funding_juta_usd", ascending=False).head(15), "total_funding_juta_usd", "startup_name_clean", "Top Repeat-Funded Startup berdasarkan Total Funding", orientation="h", height=540), use_container_width=True)

    st.dataframe(repeat_startups.sort_values("jumlah_funding", ascending=False).head(30), use_container_width=True, hide_index=True)


# ============================================================
# Outlier Analysis
# ============================================================

with tab_outliers:
    st.markdown("## Outlier Analysis")
    st.markdown(
        f"""
        <div class="warning-card">
        <b>Outlier impact:</b> Berdasarkan metode IQR pada data yang difilter, funding di atas
        <b>{format_usd_million(upper_bound)}</b> dikategorikan sebagai outlier. Outlier menyumbang sekitar
        <b>{outlier_contribution:.2f}%</b> dari total funding.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Q1", format_usd_million(q1))
    c2.metric("Q3", format_usd_million(q3))
    c3.metric("IQR", format_usd_million(iqr))
    c4.metric("Outlier Records", format_number(outlier_df.shape[0]))

    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        top_deals = funding_with_amount.sort_values("amount_million_usd", ascending=False).head(15).copy()
        top_deals["label"] = top_deals["startup_name_clean"] + " (" + top_deals["year"].astype(str) + ")"
        st.plotly_chart(make_bar(top_deals, "amount_million_usd", "label", "Top 15 Funding Deal Terbesar", orientation="h", height=560, color="#fb923c"), use_container_width=True)
    with col2:
        pie_df = pd.DataFrame({
            "Kategori": ["Tanpa Outlier", "Outlier"],
            "Total Funding": [no_outlier_df["amount_million_usd"].sum(), outlier_df["amount_million_usd"].sum()]
        })
        fig = px.pie(pie_df, names="Kategori", values="Total Funding", title="Kontribusi Outlier terhadap Total Funding", hole=0.58, template="plotly_dark")
        fig.update_layout(height=560, paper_bgcolor="#0f172a", plot_bgcolor="#0f172a", font_color="#cbd5e1", title_font_color="#f8fafc")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Top Outlier Deals")
    cols = ["date_clean", "startup_name_clean", "city_clean", "industry_group", "investment_type_clean", "investors", "amount_million_usd"]
    st.dataframe(outlier_df.sort_values("amount_million_usd", ascending=False)[cols].head(30), use_container_width=True, hide_index=True)


# ============================================================
# Data Explorer
# ============================================================

with tab_data:
    st.markdown("## Data Explorer")
    st.markdown(
        """
        <div class="section-card">
        <h3>Explore Dataset</h3>
        <p>Gunakan tabel ini untuk mengecek data hasil cleaning berdasarkan filter yang dipilih.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    columns = ["date_clean", "startup_name_clean", "city_clean", "industry_group", "investment_type_clean", "investors", "amount_million_usd"]
    columns = [col for col in columns if col in df.columns]
    st.dataframe(df[columns].sort_values("date_clean", ascending=False), use_container_width=True, hide_index=True)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", csv_data, "filtered_startup_funding_data.csv", "text/csv")


# ============================================================
# Footer
# ============================================================

st.markdown(
    """
    <div class="footer">
    Indian Startup Funding Analysis • Data Analytics Portfolio Project • Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
