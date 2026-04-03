import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
import streamlit.components.v1 as components

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Operational Lead Time Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS  —  dark glassmorphism theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #ffffff !important;
    }

    /* ── App background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
        color: #ffffff !important;
    }

    /* ── Header ── */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label { color: #ffffff !important; font-size:0.82rem; }

    /* Override input backgrounds to fix white text visibility */
    [data-baseweb="input"], [data-baseweb="select"] > div, div[data-baseweb="popover"], div[role="listbox"] {
        background-color: rgba(20, 20, 40, 0.9) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #ffffff !important;
    }
    input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    div[role="option"] {
        background-color: rgba(20, 20, 40, 0.9) !important;
    }
    div[role="option"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 16px;
        padding: 22px 24px;
        backdrop-filter: blur(16px);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transform-style: preserve-3d;
    }
    .metric-card:hover {
        transform: perspective(1000px) translateY(-8px) rotateX(4deg) rotateY(-2deg) scale(1.02);
        box-shadow: -10px 25px 50px rgba(0,0,0,0.6), inset 0 2px 4px rgba(255,255,255,0.25);
        border: 1px solid rgba(255,255,255,0.3);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    .card-blue::before   { background: linear-gradient(90deg,#667eea,#764ba2); }
    .card-teal::before   { background: linear-gradient(90deg,#11998e,#38ef7d); }
    .card-orange::before { background: linear-gradient(90deg,#f7971e,#ffd200); }
    .card-red::before    { background: linear-gradient(90deg,#f953c6,#b91d73); }

    .metric-label {
        font-size: 0.80rem;
        font-weight: 500;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.1;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #ffffff;
        margin-top: 6px;
    }
    .metric-icon {
        font-size: 1.8rem;
        float: right;
        margin-top: -4px;
        opacity: 0.6;
    }

    /* ── Section titles ── */
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-top: 6px;
    }

    /* ── Page header ── */
    .page-header {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 28px 36px;
        backdrop-filter: blur(20px);
        margin-bottom: 28px;
        background-image: radial-gradient(circle at top right, rgba(102,126,234,0.2), transparent 60%);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4), inset 0 2px 3px rgba(255,255,255,0.1);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
    }
    .page-header:hover {
        transform: translateY(-3px) scale(1.005);
        box-shadow: 0 20px 45px rgba(0,0,0,0.5), inset 0 2px 4px rgba(255,255,255,0.2);
    }
    .page-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg,#a78bfa,#38bdf8,#34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 4px 0;
    }
    .page-sub {
        font-size: 0.9rem;
        color: #ffffff;
    }

    /* ── Dataframe ── */
    .dataframe-wrapper {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }

    /* ── Chart containers ── */
    .chart-container {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 16px;
        backdrop-filter: blur(10px);
    }

    /* ── Divider ── */
    hr { border-color: rgba(255,255,255,0.07); }

    /* ── Alert / info ── */
    .stAlert { background: rgba(255,255,255,0.05); border-radius:12px; }

    /* ── Plotly chart border ── */
    .js-plotly-plot { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PLOTLY BASE TEMPLATE
# ─────────────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#ffffff"),
    margin=dict(l=12, r=12, t=42, b=12),
    legend=dict(
        bgcolor="rgba(255,255,255,0.05)",
        bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1,
        font=dict(size=11, color="#ffffff"),
    ),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.1)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.1)"),
    colorway=["#667eea","#38ef7d","#f7971e","#f953c6","#38bdf8","#a78bfa","#fbbf24"],
)

COLOR_PALETTE = [
    "#7c6fe3","#6ee7f7","#5be7c4","#f97316","#f471b5",
    "#a3e635","#facc15","#60a5fa","#c084fc","#34d399",
]

# ─────────────────────────────────────────────
#  DATA LOADING & PREPROCESSING
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(filepath: str) -> pd.DataFrame:
    """Load and preprocess the operational lead-time CSV."""
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        st.error(f"❌ File not found: `{filepath}`. Please ensure the CSV file is in the same directory.")
        st.stop()
    except Exception as exc:
        st.error(f"❌ Failed to read CSV file: {exc}")
        st.stop()

    # ── Parse date columns ──
    date_cols = [
        "Arrival_Date", "QC_Handover_Date",
        "Verification_Completion_Date", "System_Input_Completion_Date",
    ]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # ── Compute lead-time metrics (days) ──
    df["Lead_Time_QC"]     = (df["QC_Handover_Date"]            - df["Arrival_Date"]).dt.days
    df["Lead_Time_Verif"]  = (df["Verification_Completion_Date"] - df["QC_Handover_Date"]).dt.days
    df["Lead_Time_System"] = (df["System_Input_Completion_Date"] - df["Verification_Completion_Date"]).dt.days
    df["Total_Lead_Time"]  = (df["System_Input_Completion_Date"] - df["Arrival_Date"]).dt.days
    df["Net_Processing_Time"] = (df["System_Input_Completion_Date"] - df["QC_Handover_Date"]).dt.days

    # ── Clean up ──
    df["Return_Status"]    = df["Return_Status"].fillna("No")
    df["Issue_Description"]= df["Issue_Description"].fillna("-")

    return df


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
FILE_PATH = os.path.join(os.path.dirname(__file__), "Oprasional Lead Time.csv")
df_raw = load_data(FILE_PATH)


# ─────────────── SIDEBAR ───────────────────
with st.sidebar:
    st.markdown("""
        <div style='text-align:center;padding:10px 0 20px 0;'>
            <div style='font-size:2.4rem;'>📦</div>
            <div style='font-size:1rem;font-weight:700;color:#ffffff;letter-spacing:1px;'>LeadTime Analytics</div>
            <div style='font-size:0.72rem;color:#ffffff;margin-top:2px;'>Operational Intelligence</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 Filter Data")
    st.markdown("---")

    # ── Date range ──
    min_date = df_raw["Arrival_Date"].min().date()
    max_date = df_raw["Arrival_Date"].max().date()
    st.markdown("**📅 Arrival Date Range**")
    date_start = st.date_input("From Date", value=min_date, min_value=min_date, max_value=max_date, key="date_from")
    date_end   = st.date_input("To Date", value=max_date, min_value=min_date, max_value=max_date, key="date_to")

    st.markdown("")

    # ── Category ──
    all_cats = sorted(df_raw["Category"].dropna().unique().tolist())
    sel_cats = st.multiselect(
        "🏷️ Category",
        options=all_cats,
        default=all_cats,
        placeholder="Select category…",
    )

    # ── Logistics Vendor ──
    all_vendors = sorted(df_raw["Logistics_Vendor"].dropna().unique().tolist())
    sel_vendors = st.multiselect(
        "🚚 Logistics Vendor",
        options=all_vendors,
        default=all_vendors,
        placeholder="Select vendor…",
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;color:#ffffff;text-align:center;'>Dashboard v1.0 · Data as of Jan 2026</div>",
        unsafe_allow_html=True,
    )


# ─────────────── APPLY FILTERS ─────────────
df = df_raw.copy()
df = df[
    (df["Arrival_Date"].dt.date >= date_start) &
    (df["Arrival_Date"].dt.date <= date_end)
]
if sel_cats:
    df = df[df["Category"].isin(sel_cats)]
if sel_vendors:
    df = df[df["Logistics_Vendor"].isin(sel_vendors)]


# ─────────────── PAGE HEADER ──────────────
st.markdown("""
    <div class="page-header">
        <div class="page-title">📦 Operational Lead Time Dashboard</div>
        <div class="page-sub">
            End-to-end monitoring & analysis of the goods receipt lead time process — from Arrival to System Input.
        </div>
    </div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  ROW 1 — KPI CARDS
# ═══════════════════════════════════════════
st.markdown('<div class="section-title">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
st.markdown("")

total_orders  = df["Order_ID"].nunique()
total_qty     = df["Qty"].sum()
total_box_qty = df["Box_Qty"].sum()
avg_lead_time = df["Total_Lead_Time"].mean()
return_count  = (df["Return_Status"].str.strip().str.lower() == "yes").sum()
return_rate   = (return_count / len(df) * 100) if len(df) > 0 else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card card-blue">
        <span class="metric-icon">🆔</span>
        <div class="metric-label">Total Order ID</div>
        <div class="metric-value">{total_orders:,}</div>
        <div class="metric-sub">Unique orders in period</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card card-teal">
        <span class="metric-icon">📦</span>
        <div class="metric-label">Total Qty · Box Qty</div>
        <div class="metric-value">{total_qty:,}</div>
        <div class="metric-sub">Box: {total_box_qty:,} units delivered</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    avg_str = f"{avg_lead_time:.1f}" if not np.isnan(avg_lead_time) else "—"
    st.markdown(f"""
    <div class="metric-card card-orange">
        <span class="metric-icon">⏱️</span>
        <div class="metric-label">Avg Total Lead Time</div>
        <div class="metric-value">{avg_str}</div>
        <div class="metric-sub">Average days Arrival → System Input</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card card-red">
        <span class="metric-icon">🔄</span>
        <div class="metric-label">Return Rate</div>
        <div class="metric-value">{return_rate:.1f}%</div>
        <div class="metric-sub">{return_count} orders from {len(df)} data rows</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════
#  ROW 2 — SLA COMPARISON HIGHLIGHT
# ═══════════════════════════════════════════
st.markdown('<div class="section-title">🎯 SLA Target Evaluation (Standard: Max 4 Days)</div>', unsafe_allow_html=True)
st.markdown("")

gross_sla_hit = (df["Total_Lead_Time"] <= 4).sum()
gross_sla_rate = (gross_sla_hit / len(df) * 100) if len(df) > 0 else 0

net_sla_hit = (df["Net_Processing_Time"] <= 4).sum()
net_sla_rate = (net_sla_hit / len(df) * 100) if len(df) > 0 else 0

col_sla1, col_sla2 = st.columns(2)
with col_sla1:
    st.markdown(f"""
    <div class="metric-card card-red" style="padding: 18px 24px;">
        <span class="metric-icon">🏢</span>
        <div class="metric-label" style="color: #ffffff;">Strict System (From Arrival Date)</div>
        <div style="font-size: 2.8rem; font-weight: 800; color: #f953c6; line-height: 1.1;">{gross_sla_rate:.1f}%</div>
        <div class="metric-sub" style="color: #ffffff; margin-top: 8px;">
            Only <b>{gross_sla_hit:,}</b> out of {len(df):,} orders met SLA.<br>
            <span style="opacity:0.8;">This metric is heavily affected by warehouse queueing.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_sla2:
    st.markdown(f"""
    <div class="metric-card card-teal" style="padding: 18px 24px;">
        <span class="metric-icon">🏃‍♂️</span>
        <div class="metric-label" style="color: #ffffff;">Actual Team Performance (From QC Handover)</div>
        <div style="font-size: 2.8rem; font-weight: 800; color: #38ef7d; line-height: 1.1;">{net_sla_rate:.1f}%</div>
        <div class="metric-sub" style="color: #ffffff; margin-top: 8px;">
            Actually, <b>{net_sla_hit:,}</b> out of {len(df):,} orders met SLA!<br>
            <span style="opacity:0.8;">True team performance is much better when queue time is excluded.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════
#  ROW 3 — MAIN CHARTS
# ═══════════════════════════════════════════
st.markdown('<div class="section-title">📈 Main Lead Time Analysis</div>', unsafe_allow_html=True)
st.markdown("")

col_left, col_right = st.columns(2)

# ── LEFT: Avg Total Lead Time by Category ──
with col_left:
    lead_by_cat = (
        df.groupby("Category")["Total_Lead_Time"]
        .mean()
        .reset_index()
        .rename(columns={"Total_Lead_Time": "Avg_Lead_Time"})
        .sort_values("Avg_Lead_Time", ascending=False)
    )

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=lead_by_cat["Category"],
        y=lead_by_cat["Avg_Lead_Time"],
        marker=dict(
            color=lead_by_cat["Avg_Lead_Time"],
            colorscale="Plasma",
            showscale=False,
            line=dict(color="rgba(255,255,255,0.3)", width=2),
        ),
        text=[f"{v:.1f}d" for v in lead_by_cat["Avg_Lead_Time"]],
        textposition="outside",
        textfont=dict(color="#ffffff", size=11),
        hovertemplate="<b>%{x}</b><br>Avg Lead Time: %{y:.1f} hari<extra></extra>",
    ))
    fig_bar.update_layout(
        **PLOTLY_THEME,
        title=dict(text="🏷️ Avg Total Lead Time by Category", font=dict(size=13, color="#ffffff")),
        xaxis_title="",
        yaxis_title="Days",
        height=360,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── RIGHT: Bottleneck Analysis ──
with col_right:
    phase_data = {
        "Phase": ["QC Handover", "Verification", "System Input"],
        "Avg_Days": [
            df["Lead_Time_QC"].mean(),
            df["Lead_Time_Verif"].mean(),
            df["Lead_Time_System"].mean(),
        ],
    }
    phase_df = pd.DataFrame(phase_data).sort_values("Avg_Days", ascending=True)

    fig_bottleneck = go.Figure()
    fig_bottleneck.add_trace(go.Funnel(
        y=phase_df["Phase"],
        x=phase_df["Avg_Days"],
        marker=dict(
            color=["#34d399","#f7971e","#f953c6"][:len(phase_df)],
            line=dict(color="rgba(255,255,255,0.4)", width=2),
        ),
        textposition="inside",
        textinfo="value+percent initial",
        textfont=dict(color="#000000"),
        hoverinfo="y+x",
    ))
    fig_bottleneck.update_layout(
        **PLOTLY_THEME,
        title=dict(text="⚡ Bottleneck Analysis by Phase", font=dict(size=13, color="#ffffff")),
        xaxis_title="Average Days",
        yaxis_title="",
        height=360,
    )
    st.plotly_chart(fig_bottleneck, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  ROW 3 — TREND & ISSUE CHARTS
# ═══════════════════════════════════════════
st.markdown('<div class="section-title">📉 Trends & Issue Distribution</div>', unsafe_allow_html=True)
st.markdown("")

col_line, col_donut = st.columns(2)

# ── LEFT: Arrival Volume Trend ──
with col_line:
    trend_df = (
        df.groupby(df["Arrival_Date"].dt.date)["Qty"]
        .sum()
        .reset_index()
        .rename(columns={"Arrival_Date": "Date", "Qty": "Total_Qty"})
        .sort_values("Date")
    )

    fig_line = go.Figure()
    # Area fill
    fig_line.add_trace(go.Scatter(
        x=trend_df["Date"],
        y=trend_df["Total_Qty"],
        fill="tozeroy",
        fillcolor="rgba(102,126,234,0.15)",
        line=dict(color="#a78bfa", width=2.5),
        mode="lines+markers",
        marker=dict(size=6, color="#667eea", line=dict(color="#ffffff", width=1)),
        hovertemplate="<b>%{x}</b><br>Total Qty: %{y:,}<extra></extra>",
        name="Total Qty",
    ))
    fig_line.update_layout(
        **PLOTLY_THEME,
        title=dict(text="📅 Goods Arrival Volume Trend", font=dict(size=13, color="#ffffff")),
        xaxis_title="Arrival Date",
        yaxis_title="Total Qty",
        height=360,
        showlegend=False,
        hovermode="x unified",
    )
    fig_line.update_xaxes(
        rangeslider=dict(visible=True, thickness=0.08, bgcolor="rgba(255,255,255,0.05)"),
        type="date"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ── RIGHT: Issue Description Donut ──
with col_donut:
    issue_df = (
        df[df["Issue_Description"] != "-"]["Issue_Description"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Issue", "Issue_Description": "Count"})
    )
    # Rename columns correctly depending on pandas version
    if "Issue_Description" in issue_df.columns and "count" in issue_df.columns:
        issue_df.columns = ["Issue", "Count"]
    elif issue_df.columns[0] == "Issue_Description":
        issue_df.columns = ["Issue", "Count"]

    if issue_df.empty:
        st.info("No issue data for the selected filter range.")
    else:
        fig_donut = go.Figure(go.Pie(
            labels=issue_df.iloc[:, 0],
            values=issue_df.iloc[:, 1],
            hole=0.55,
            pull=[0.05] * len(issue_df),
            marker=dict(
                colors=COLOR_PALETTE[:len(issue_df)],
                line=dict(color="rgba(255,255,255,0.15)", width=2),
            ),
            textinfo="percent+label",
            insidetextfont=dict(size=11, color="#000000"),
            outsidetextfont=dict(size=11, color="#ffffff"),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>",
        ))
        fig_donut.add_annotation(
            text="Issue<br>Breakdown",
            x=0.5, y=0.5,
            font=dict(size=13, color="#ffffff"),
            showarrow=False,
        )
        fig_donut.update_layout(
            **PLOTLY_THEME,
            title=dict(text="🐛 Operational Issues Breakdown", font=dict(size=13, color="#ffffff")),
            height=360,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  ROW 4 — DETAILED DATA TABLE
# ═══════════════════════════════════════════
st.markdown('<div class="section-title">🗂️ Raw Data — Detailed Table</div>', unsafe_allow_html=True)
st.markdown("")

display_cols = [
    "Order_ID", "Category", "Logistics_Vendor", "Priority_Phase",
    "Arrival_Date", "QC_Handover_Date", "Verification_Completion_Date",
    "System_Input_Completion_Date",
    "Lead_Time_QC", "Lead_Time_Verif", "Lead_Time_System", "Total_Lead_Time",
    "Qty", "Box_Qty", "Return_Status", "Issue_Description",
]
display_cols = [c for c in display_cols if c in df.columns]

with st.container():
    st.dataframe(
        df[display_cols].reset_index(drop=True),
        use_container_width=True,
        height=380,
        column_config={
            "Order_ID":                        st.column_config.TextColumn("Order ID"),
            "Category":                        st.column_config.TextColumn("Category"),
            "Logistics_Vendor":                st.column_config.TextColumn("Vendor"),
            "Priority_Phase":                  st.column_config.TextColumn("Priority Phase"),
            "Arrival_Date":                    st.column_config.DateColumn("Arrival Date", format="DD-MM-YYYY"),
            "QC_Handover_Date":                st.column_config.DateColumn("QC Handover", format="DD-MM-YYYY"),
            "Verification_Completion_Date":    st.column_config.DateColumn("Verification", format="DD-MM-YYYY"),
            "System_Input_Completion_Date":    st.column_config.DateColumn("System Input", format="DD-MM-YYYY"),
            "Lead_Time_QC":                    st.column_config.NumberColumn("LT QC (days)", format="%d days"),
            "Lead_Time_Verif":                 st.column_config.NumberColumn("LT Verif (days)", format="%d days"),
            "Lead_Time_System":                st.column_config.NumberColumn("LT System (days)", format="%d days"),
            "Total_Lead_Time":                 st.column_config.NumberColumn("Total LT (days)", format="%d days"),
            "Qty":                             st.column_config.NumberColumn("Qty", format="%d"),
            "Box_Qty":                         st.column_config.NumberColumn("Box Qty", format="%d"),
            "Return_Status":                   st.column_config.TextColumn("Return"),
            "Issue_Description":               st.column_config.TextColumn("Issue"),
        },
    )

# ── Download button ──
csv_out = df[display_cols].to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv_out,
    file_name="filtered_lead_time.csv",
    mime="text/csv",
)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center;font-size:0.75rem;color:#ffffff;'>Built with ❤️ using Streamlit & Plotly — Operational Lead Time Analytics</div>",
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════
#  HOLOGRAPHIC CARD TILT EFFECT (JAVASCRIPT)
# ═══════════════════════════════════════════
components.html("""
<script>
    const parentDoc = window.parent.document;
    
    function applyCardTilt() {
        // Select all plot charts and metric cards in the layout
        const elements = parentDoc.querySelectorAll('.stPlotlyChart, .metric-card');
        
        elements.forEach(el => {
            // Prevent attaching multiple listeners to the same element
            if (el.dataset.tiltAttached === "true") return;
            el.dataset.tiltAttached = "true";
            
            // Apply required base 3D perspective styles
            el.style.transformStyle = "preserve-3d";
            el.style.transition = "transform 0.4s ease";
            
            el.addEventListener('mousemove', (e) => {
                const rect = el.getBoundingClientRect();
                // Cursor position relative to the element (0,0 is top-left)
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                // Tilt calculation (Max roughly 4 degrees rotation per element)
                const rotateX = ((y - centerY) / centerY) * -4;
                const rotateY = ((x - centerX) / centerX) * 4;
                
                el.style.transition = "transform 0.05s linear";
                el.style.transform = `perspective(1000px) scale3d(1.02, 1.02, 1.02) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });
            
            el.addEventListener('mouseleave', () => {
                // Return to static 2D
                el.style.transition = "transform 0.5s ease";
                el.style.transform = "perspective(1000px) scale3d(1, 1, 1) rotateX(0deg) rotateY(0deg)";
            });
        });
    }

    // Since Streamlit renders elements asynchronously, we re-apply periodically
    setInterval(() => { applyCardTilt(); }, 1500);
</script>
""", height=0, width=0)
