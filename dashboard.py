import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FraudShield · Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Premium CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Font ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  /* ── Root Variables ── */
  :root {
    --bg-primary:   #0a0e1a;
    --bg-secondary: #0f1629;
    --bg-card:      rgba(255,255,255,0.04);
    --border-card:  rgba(255,255,255,0.08);
    --accent-blue:  #4f8dff;
    --accent-cyan:  #00e5ff;
    --accent-red:   #ff4d6d;
    --accent-amber: #ffb347;
    --accent-green: #00e396;
    --accent-purple:#a78bfa;
    --text-primary: #e8ecf4;
    --text-muted:   #8892a4;
    --radius:       14px;
    --shadow:       0 8px 32px rgba(0,0,0,0.45);
  }

  /* ── Global ── */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
  }
  .block-container { padding: 1.5rem 2rem 3rem 2rem !important; }

  /* ── Animated gradient background ── */
  .stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #101728 40%, #0d1520 100%) !important;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1527 0%, #111c35 100%) !important;
    border-right: 1px solid rgba(79,141,255,0.18) !important;
  }
  [data-testid="stSidebar"] * { color: var(--text-primary) !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stSlider label { color: var(--text-muted) !important; font-weight: 500; }

  /* ── Hero Banner ── */
  .hero-banner {
    background: linear-gradient(120deg, rgba(79,141,255,0.15) 0%, rgba(0,229,255,0.10) 50%, rgba(167,139,250,0.12) 100%);
    border: 1px solid rgba(79,141,255,0.25);
    border-radius: var(--radius);
    padding: 2rem 2.5rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content:"";
    position:absolute; top:-60px; right:-60px;
    width:220px; height:220px;
    background: radial-gradient(circle, rgba(79,141,255,0.18) 0%, transparent 70%);
    border-radius:50%;
  }
  .hero-banner::after {
    content:"";
    position:absolute; bottom:-40px; left:30%;
    width:160px; height:160px;
    background: radial-gradient(circle, rgba(0,229,255,0.12) 0%, transparent 70%);
    border-radius:50%;
  }
  .hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #4f8dff 0%, #00e5ff 50%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.25rem 0;
  }
  .hero-sub {
    font-size: 1rem;
    color: var(--text-muted);
    font-weight: 400;
  }
  .hero-badge {
    display: inline-block;
    background: linear-gradient(90deg, rgba(0,229,150,0.2), rgba(0,229,150,0.08));
    border: 1px solid rgba(0,229,150,0.4);
    color: #00e396;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 3px 10px;
    border-radius: 99px;
    margin-left: 0.75rem;
    vertical-align: middle;
    text-transform: uppercase;
  }

  /* ── KPI Cards ── */
  .kpi-grid { display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1.5rem; }
  .kpi-card {
    flex: 1 1 160px;
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: var(--radius);
    padding: 1.1rem 1.3rem;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(16px);
    transition: transform .2s, box-shadow .2s;
  }
  .kpi-card:hover { transform:translateY(-3px); box-shadow: var(--shadow); }
  .kpi-card::before {
    content:"";
    position:absolute; top:0; left:0; right:0; height:3px;
    border-radius: var(--radius) var(--radius) 0 0;
  }
  .kpi-card.blue::before  { background: linear-gradient(90deg, #4f8dff, #00e5ff); }
  .kpi-card.red::before   { background: linear-gradient(90deg, #ff4d6d, #ff8c55); }
  .kpi-card.amber::before { background: linear-gradient(90deg, #ffb347, #ffda44); }
  .kpi-card.green::before { background: linear-gradient(90deg, #00e396, #00c9b2); }
  .kpi-card.purple::before{ background: linear-gradient(90deg, #a78bfa, #e879f9); }
  .kpi-label { font-size:0.75rem; color:var(--text-muted); font-weight:600; letter-spacing:.06em; text-transform:uppercase; margin-bottom:.35rem; }
  .kpi-value { font-size:1.9rem; font-weight:800; letter-spacing:-0.02em; line-height:1; }
  .kpi-card.blue  .kpi-value { color:#6eb4ff; }
  .kpi-card.red   .kpi-value { color:#ff6b85; }
  .kpi-card.amber .kpi-value { color:#ffbe5c; }
  .kpi-card.green .kpi-value { color:#00e396; }
  .kpi-card.purple.kpi-value { color:#b79dff; }
  .kpi-sub { font-size:0.7rem; color:var(--text-muted); margin-top:.4rem; }
  .kpi-icon { font-size:1.6rem; position:absolute; right:1rem; top:50%; transform:translateY(-50%); opacity:.25; }

  /* ── Section Headers ── */
  .section-header {
    display: flex;
    align-items:center;
    gap:.6rem;
    font-size:1.15rem;
    font-weight:700;
    color:var(--text-primary);
    margin: 1.6rem 0 .8rem 0;
    padding-bottom:.5rem;
    border-bottom:1px solid rgba(255,255,255,0.07);
  }
  .section-header .dot {
    width:8px; height:8px; border-radius:50%;
    background:linear-gradient(135deg,#4f8dff,#00e5ff);
    display:inline-block;
    box-shadow: 0 0 8px #4f8dff;
  }

  /* ── Glass Chart Card ── */
  .chart-card {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: var(--radius);
    padding: 1rem;
    backdrop-filter: blur(12px);
    margin-bottom: .5rem;
  }

  /* ── Insight Cards ── */
  .insight-grid { display:flex; flex-direction:column; gap:.65rem; }
  .insight-card {
    background: rgba(255,255,255,0.03);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 0 10px 10px 0;
    padding: .75rem 1rem;
    font-size:.9rem;
    color: var(--text-primary);
    transition: background .2s;
  }
  .insight-card:hover { background: rgba(79,141,255,0.08); }
  .insight-card.warn  { border-color: var(--accent-amber); }
  .insight-card.danger{ border-color: var(--accent-red);   }
  .insight-card.ok    { border-color: var(--accent-green); }

  /* ── Sidebar Badge ── */
  .sidebar-logo {
    font-size:1.3rem; font-weight:800;
    background: linear-gradient(90deg,#4f8dff,#00e5ff);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;
    margin-bottom:.5rem;
  }
  .sidebar-meta { font-size:.75rem; color:var(--text-muted); margin-bottom:1.2rem; }

  /* ── Divider ── */
  .fancy-divider {
    height:1px;
    background: linear-gradient(90deg, transparent, rgba(79,141,255,0.35), transparent);
    margin: 1.5rem 0;
  }

  /* ── Dataframe ── */
  [data-testid="stDataFrame"] { border-radius:var(--radius); overflow:hidden; }

  /* ── Streamlit overrides ── */
  .stMetric label { color: var(--text-muted) !important; }
  .stMetric [data-testid="stMetricValue"] { color: #6eb4ff !important; font-weight:700; }
  div[data-testid="stSelectbox"] > div:first-child { background: rgba(255,255,255,0.05) !important; border:1px solid rgba(255,255,255,0.1) !important; border-radius:8px; }
  div[data-testid="stSlider"] > div { color: var(--accent-blue) !important; }

  /* ── Footer ── */
  .premium-footer {
    text-align:center;
    font-size:.75rem;
    color:var(--text-muted);
    margin-top:2rem;
    padding-top:1rem;
    border-top:1px solid rgba(255,255,255,0.06);
  }
  .premium-footer span { color: #4f8dff; }
</style>
""", unsafe_allow_html=True)

# ─── Plotly Theme ─────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#8892a4"),
    title_font=dict(family="Inter", color="#e8ecf4", size=15),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c2cad8")),
    margin=dict(t=50, l=10, r=10, b=10),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True, zeroline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True, zeroline=False),
    colorway=["#4f8dff","#ff4d6d","#00e396","#ffb347","#a78bfa","#00e5ff"],
)

COLORS      = {"Normal": "#4f8dff", "Fraud": "#ff4d6d"}
RISK_COLORS = {"Low": "#00e396",    "Medium": "#ffb347", "High": "#ff4d6d"}

# ─── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("enhanced_data.csv")
        df["Class"]      = df["Class"].astype(int)
        df["prediction"] = df["prediction"].astype(int)
        df["Hour"]       = df["Hour"].astype(int)
        return df
    except FileNotFoundError:
        st.error("⚠️  enhanced_data.csv not found. Run feature_engineering.py first.")
        return pd.DataFrame()

def calculate_kpis(df):
    total    = len(df)
    fraud    = int(df["Class"].sum())
    pct      = (fraud / total * 100) if total > 0 else 0
    amount   = df["Amount"].sum()
    hi_risk  = int((df["risk_score"] > 0.8).sum())
    model_acc= None
    if "prediction" in df.columns:
        model_acc = (df["Class"] == df["prediction"]).mean() * 100
    return dict(total=total, fraud=fraud, pct=pct, amount=amount,
                hi_risk=hi_risk, model_acc=model_acc)

# ─── Charts ───────────────────────────────────────────────────────────────────
def pie_chart(df):
    counts = df["Class"].value_counts().reset_index()
    counts.columns = ["Class", "Count"]
    counts["Class"] = counts["Class"].map({0: "Normal", 1: "Fraud"}).astype(str)
    counts = counts[counts["Class"].isin(["Normal", "Fraud"])]
    ordered = [l for l in ["Normal", "Fraud"] if l in counts["Class"].values]
    ordered_counts = counts.set_index("Class").reindex(ordered)["Count"].tolist()
    fig = go.Figure(go.Pie(
        labels=ordered,
        values=ordered_counts,
        hole=0.52,
        marker=dict(
            colors=[COLORS[l] for l in ordered],
            line=dict(color="#0a0e1a", width=2)
        ),
        textposition="outside",
        textinfo="percent+label",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title="Transaction Distribution")
    return fig

def time_series(df):
    td = df.groupby(["Hour", "Class"]).size().reset_index(name="Count")
    td["Class"] = td["Class"].map({0: "Normal", 1: "Fraud"}).astype(str)
    td = td[td["Class"].isin(["Normal", "Fraud"])]
    fig = go.Figure()
    for label, color in COLORS.items():
        subset = td[td["Class"] == label]
        if subset.empty:
            continue
        fig.add_trace(go.Scatter(
            x=subset["Hour"], y=subset["Count"],
            mode="lines+markers", name=label,
            fill="tozeroy", opacity=0.75,
            line=dict(color=color, width=2),
            marker=dict(color=color, size=5),
        ))
    fig.update_layout(**PLOTLY_LAYOUT,
                      title="Hourly Transaction Volume",
                      xaxis_title="Hour of Day", yaxis_title="Volume")
    return fig

def risk_bar(df):
    cats = ["Low", "Medium", "High"]
    counts = df["Risk_Category"].value_counts().reindex(cats, fill_value=0)
    fig = go.Figure(go.Bar(
        x=cats,
        y=counts.values,
        marker_color=[RISK_COLORS[c] for c in cats],
        marker_line_width=0,
        opacity=0.9,
        text=counts.values,
        textposition="outside",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title="Risk Category Distribution",
                      xaxis_title="", yaxis_title="Count", showlegend=False)
    return fig

def amount_fraud_bar(df):
    fd = df[df["Class"]==1].groupby("Amount_Bin").size().reset_index(name="Fraud_Count")
    fig = px.bar(fd, x="Amount_Bin", y="Fraud_Count",
                 title="Fraud Counts by Transaction Tier",
                 color="Fraud_Count",
                 color_continuous_scale=["#ffb347","#ff4d6d","#c9003a"],
                 text_auto=True)
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="Fraud Count",
                      coloraxis_showscale=False)
    return fig

def risk_histogram(df):
    fig = px.histogram(df, x="risk_score", nbins=60,
                       title="Risk Score Distribution",
                       color_discrete_sequence=["#4f8dff"],
                       marginal="violin", opacity=0.8)
    fig.update_layout(**PLOTLY_LAYOUT,
                      xaxis_title="Risk Score", yaxis_title="Frequency")
    return fig

def scatter_amount_risk(df):
    sample = df.sample(min(4000, len(df)), random_state=42)
    fig = go.Figure()
    for cls, label, color in [(0, "Normal", "#4f8dff"), (1, "Fraud", "#ff4d6d")]:
        sub = sample[sample["Class"] == cls]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["Amount_Log"], y=sub["risk_score"],
            mode="markers", name=label,
            marker=dict(color=color, size=4, opacity=0.65),
        ))
    fig.update_layout(**PLOTLY_LAYOUT, title="Log-Amount vs Risk Score",
                      xaxis_title="Log(Amount)", yaxis_title="Risk Score")
    return fig

def fraud_heatmap(df):
    pivot = df.groupby(["Time_of_Day","Risk_Category"])["Class"].sum().reset_index()
    pivot = pivot.pivot(index="Time_of_Day", columns="Risk_Category", values="Class").fillna(0)
    cats  = [c for c in ["Low","Medium","High"] if c in pivot.columns]
    times = ["Morning","Afternoon","Evening","Night"]
    times = [t for t in times if t in pivot.index]
    pivot = pivot.reindex(index=times, columns=cats)
    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale=[[0,"rgba(79,141,255,0.1)"],[0.5,"#ffb347"],[1,"#ff4d6d"]],
        showscale=True,
        hovertemplate="Time: %{y}<br>Risk: %{x}<br>Frauds: %{z}<extra></extra>",
    ))
    fig.update_layout(**PLOTLY_LAYOUT,
                      title="Fraud Intensity · Time vs Risk",
                      xaxis_title="Risk Category", yaxis_title="Time of Day")
    return fig

# ─── Insights ────────────────────────────────────────────────────────────────
def insights(df, kpis):
    rows = []
    # Fraud rate
    if kpis["pct"] < 1:
        rows.append(("ok",    f"✅  Fraud rate is <b>{kpis['pct']:.3f}%</b> — detection system is performing well."))
    else:
        rows.append(("danger",f"🚨  Elevated fraud rate of <b>{kpis['pct']:.2f}%</b> — immediate review recommended."))
    # High-risk
    hr_pct = kpis["hi_risk"] / kpis["total"] * 100
    rows.append(("warn", f"⚡  <b>{kpis['hi_risk']:,}</b> transactions ({hr_pct:.2f}%) carry a risk score above 0.80."))
    # Peak hour
    peak = df.groupby("Hour").size().idxmax()
    rows.append(("",     f"📈  Peak transaction volume occurs at <b>{peak}:00</b> — consider heightened monitoring."))
    # Amount comparison
    avg_f = df[df["Class"]==1]["Amount"].mean()
    avg_n = df[df["Class"]==0]["Amount"].mean()
    if avg_f > avg_n:
        rows.append(("warn", f"💰  Avg fraud amount <b>${avg_f:,.2f}</b> vs normal <b>${avg_n:,.2f}</b> — higher-value transactions are riskier."))
    # Correlation
    corr = df[["Amount","risk_score"]].corr().iloc[0,1]
    rows.append(("",     f"📊  Amount ↔ Risk Score correlation: <b>{corr:.3f}</b> — {'moderate positive link' if corr > 0.2 else 'weak link, non-linear patterns present'}."))
    # Model accuracy
    if kpis["model_acc"] is not None:
        cls = "ok" if kpis["model_acc"] > 95 else "warn"
        rows.append((cls, f"🤖  Model accuracy on current filter: <b>{kpis['model_acc']:.2f}%</b>."))
    return rows

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    df = load_data()
    if df.empty:
        return

    # ── Sidebar ──────────────────────────────────────────────────────────────
    st.sidebar.markdown('<div class="sidebar-logo">🛡️ FraudShield</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-meta">Real-time risk analytics platform</div>', unsafe_allow_html=True)
    st.sidebar.markdown("---")

    st.sidebar.markdown("**🔎 Filter Controls**")
    risk_cats    = ["All"] + sorted(df["Risk_Category"].unique().tolist())
    time_cats    = ["All"] + sorted(df["Time_of_Day"].dropna().unique().tolist())
    amount_bins  = ["All"] + sorted(df["Amount_Bin"].astype(str).unique().tolist())
    class_opts   = {"All": None, "Normal Only": 0, "Fraud Only": 1}

    sel_risk   = st.sidebar.selectbox("Risk Category",   risk_cats)
    sel_time   = st.sidebar.selectbox("Time of Day",     time_cats)
    sel_bin    = st.sidebar.selectbox("Amount Tier",     amount_bins)
    sel_class  = st.sidebar.selectbox("Transaction Type",list(class_opts.keys()))
    min_s, max_s = st.sidebar.slider(
        "Risk Score Range",
        float(df["risk_score"].min()), float(df["risk_score"].max()),
        (float(df["risk_score"].min()), float(df["risk_score"].max())), 0.01)

    # ── Filter ───────────────────────────────────────────────────────────────
    fdf = df.copy()
    if sel_risk  != "All": fdf = fdf[fdf["Risk_Category"]           == sel_risk]
    if sel_time  != "All": fdf = fdf[fdf["Time_of_Day"]             == sel_time]
    if sel_bin   != "All": fdf = fdf[fdf["Amount_Bin"].astype(str)  == sel_bin]
    cls_val = class_opts[sel_class]
    if cls_val is not None: fdf = fdf[fdf["Class"] == cls_val]
    fdf = fdf[(fdf["risk_score"] >= min_s) & (fdf["risk_score"] <= max_s)]

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"<div style='font-size:.78rem;color:#8892a4;'>Showing <b style='color:#4f8dff'>{len(fdf):,}</b> / {len(df):,} transactions</div>",
                        unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-title">🛡️ FraudShield Analytics<span class="hero-badge">Live</span></div>
      <div class="hero-sub">Advanced fraud detection &amp; real-time risk intelligence dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI ───────────────────────────────────────────────────────────────────
    kpis = calculate_kpis(fdf)
    st.markdown('<div class="section-header"><span class="dot"></span>Key Performance Indicators</div>', unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)

    def kpi_card(col, color, icon, label, value, sub=""):
        col.markdown(f"""
        <div class="kpi-card {color}">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{sub}</div>
          <div class="kpi-icon">{icon}</div>
        </div>""", unsafe_allow_html=True)

    kpi_card(c1,"blue",  "🔢","Total Transactions", f"{kpis['total']:,}",       "in filtered view")
    kpi_card(c2,"red",   "🚨","Fraud Detected",     f"{kpis['fraud']:,}",        f"{kpis['pct']:.3f}% of total")
    kpi_card(c3,"amber", "💰","Total Volume",        f"${kpis['amount']:,.0f}",   "transaction value")
    kpi_card(c4,"purple","⚡","High Risk",           f"{kpis['hi_risk']:,}",      "risk score > 0.80")
    acc_txt = f"{kpis['model_acc']:.1f}%" if kpis["model_acc"] else "N/A"
    kpi_card(c5,"green", "🤖","Model Accuracy",      acc_txt,                    "prediction vs actual")

    # ── Row 1 ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="dot"></span>Distribution &amp; Trends</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.0, 1.6])
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(pie_chart(fdf), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(time_series(fdf), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 2 ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="dot"></span>Risk &amp; Amount Analysis</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(risk_bar(fdf), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(amount_fraud_bar(fdf), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 3 ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="dot"></span>Deep Dive Analytics</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(risk_histogram(fdf), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(scatter_amount_risk(fdf), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Heatmap ───────────────────────────────────────────────────────────────
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fraud_heatmap(fdf), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Insights ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="dot"></span>AI Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-grid">', unsafe_allow_html=True)
    for cls, text in insights(fdf, kpis):
        st.markdown(f'<div class="insight-card {cls}">{text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Data Table ────────────────────────────────────────────────────────────
    with st.expander("📋  Transaction Detail Table (top 200 rows)", expanded=False):
        cols = ["Amount", "Risk_Category", "Time_of_Day", "Amount_Bin",
                "Hour", "Class", "risk_score", "prediction"]
        avail = [c for c in cols if c in fdf.columns]
        def row_style(row):
            if row.get("Class", 0) == 1:
                return ["background-color: rgba(255,77,109,0.15)"] * len(avail)
            elif row.get("risk_score", 0) > 0.8:
                return ["background-color: rgba(255,179,71,0.10)"] * len(avail)
            return [""] * len(avail)
        styled = fdf[avail].head(200).style.apply(row_style, axis=1)
        st.dataframe(styled, use_container_width=True, height=360)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="premium-footer">
      Built with <span>❤️</span> using Streamlit &amp; Plotly &nbsp;·&nbsp;
      <span>FraudShield Analytics v2.0</span> &nbsp;·&nbsp; Real-time credit card fraud intelligence
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()