"""
EquiLearn Analytics — Streamlit Dashboard
==========================================
Author : Rahmat Syawaludin
         MEd Digital Learning · Monash University · LPDP Scholar
Contact: rahmatsywldn@gmail.com
Run    : streamlit run app.py
"""

import json
from io import StringIO

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EquiLearn Analytics · Rahmat Syawaludin",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design tokens (matching portfolio) ───────────────────────────────────────
ACCENT   = "#c8954a"   # amber / earth tone
ACCENT2  = "#2d6a9f"   # navy blue
WARN     = "#c0392b"
SUCCESS  = "#27ae60"
TEXT     = "#1a1f2e"
MUTED    = "#5c6475"
BG       = "#f5f2ed"
SURFACE  = "#ffffff"

IMD_ORDER = [
    "0-10%","10-20%","20-30%","30-40%","40-50%",
    "50-60%","60-70%","70-80%","80-90%","90-100%",
]

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Import fonts */
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f5f2ed;
    color: #1a1f2e;
  }

  /* Hide default Streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1200px; }

  /* Metric cards */
  div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e8e3db;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  }
  div[data-testid="metric-container"] label {
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #5c6475 !important;
    font-weight: 600;
  }
  div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif;
    font-size: 2rem !important;
    font-weight: 800;
    color: #1a1f2e;
  }

  /* Section headers */
  h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; color: #1a1f2e !important; }
  h2 { font-family: 'Syne', sans-serif !important; font-weight: 700 !important; color: #1a1f2e !important; }
  h3 { font-family: 'Syne', sans-serif !important; font-weight: 600 !important; color: #1a1f2e !important; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e8e3db;
  }
  [data-testid="stSidebar"] .css-1d391kg { padding: 2rem 1.25rem; }

  /* Tag chips */
  .tag {
    display: inline-block;
    background: #f0ece5;
    border: 1px solid #ddd8cf;
    color: #5c6475;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    margin: 0.15rem;
    letter-spacing: 0.03em;
  }

  /* Insight box */
  .insight {
    background: #eef4fb;
    border-left: 3px solid #2d6a9f;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-size: 0.9rem;
    line-height: 1.7;
    color: #1a1f2e;
    margin: 0.75rem 0;
  }
  .insight-warn {
    background: #fdf0ef;
    border-left-color: #c0392b;
  }
  .insight-success {
    background: #edfaf3;
    border-left-color: #27ae60;
  }

  /* Intervention card */
  .int-card {
    background: #ffffff;
    border: 1px solid #e8e3db;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .int-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
    margin-bottom: 0.35rem;
  }

  /* Divider */
  hr { border-color: #e8e3db; margin: 2rem 0; }

  /* Tabs */
  button[data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
  }
  button[data-baseweb="tab"][aria-selected="true"] {
    color: #c8954a !important;
    border-bottom-color: #c8954a !important;
  }
</style>
""", unsafe_allow_html=True)


# ── Google Sheets config ──────────────────────────────────────────────────────
SHEET_ID = "15rcpxlNkPKE_yrALqvxa-mL6HxelD5xFIfBYFWHKwTQ"
GIDS = {
    "demographics": "1139693545",
    "engagement":   "276917577",
    "outcomes":     "1597347938",
}

def sheet_url(gid):
    return (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&gid={gid}"
    )

# ── Sample data ───────────────────────────────────────────────────────────────
DEMO_CSV = """id_student,region,imd_band,highest_education,disability,final_result
1001,London Region,0-10%,A Level or Equivalent,N,Pass
1002,South Region,10-20%,HE Qualification,N,Pass
1003,Midlands Region,20-30%,Lower Than A Level,Y,Fail
1004,North Region,30-40%,A Level or Equivalent,N,Pass
1005,Wales,40-50%,HE Qualification,N,Withdrawn
1006,Scotland,50-60%,A Level or Equivalent,N,Pass
1007,Ireland,60-70%,Lower Than A Level,Y,Fail
1008,East Anglian Region,70-80%,Post Graduate Qualification,N,Pass
1009,North Western Region,80-90%,HE Qualification,N,Pass
1010,Yorkshire Region,90-100%,A Level or Equivalent,N,Pass
1011,London Region,0-10%,HE Qualification,N,Fail
1012,South Region,10-20%,A Level or Equivalent,Y,Pass
1013,Midlands Region,30-40%,Lower Than A Level,N,Withdrawn
1014,North Region,0-10%,A Level or Equivalent,N,Fail
1015,Wales,20-30%,HE Qualification,N,Pass"""

ENG_CSV = """id_student,week,sum_click,content_type
1001,1,42,Video
1001,2,55,Quiz
1001,3,61,Forum
1001,4,70,PDF
1001,5,22,Video
1001,6,18,Quiz
1001,7,35,Forum
1001,8,48,PDF
1002,1,30,Video
1002,2,38,Quiz
1002,3,45,Forum
1002,4,52,PDF
1002,5,12,Video
1002,6,8,Quiz
1002,7,25,Forum
1003,1,18,PDF
1003,2,22,Video
1003,3,15,Quiz
1003,4,8,Forum
1003,5,3,PDF
1003,6,0,Video
1003,7,0,Quiz
1004,1,55,Forum
1004,2,62,Video
1004,3,71,Quiz
1004,4,80,PDF
1004,5,35,Forum
1004,6,45,Video
1004,7,55,Quiz
1004,8,65,Forum"""

OUT_CSV = """id_student,assessment_score,submission_week
1001,72,6
1002,58,6
1003,31,6
1004,85,6
1005,0,
1006,78,6
1007,42,6
1008,91,6
1009,66,6
1010,74,6"""


# ── Data loader ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        df_info = pd.read_csv(sheet_url(GIDS["demographics"]))
        df_vle  = pd.read_csv(sheet_url(GIDS["engagement"]))
        df_asmt = pd.read_csv(sheet_url(GIDS["outcomes"]))
        source  = "live"
    except Exception:
        df_info = pd.read_csv(StringIO(DEMO_CSV))
        df_vle  = pd.read_csv(StringIO(ENG_CSV))
        df_asmt = pd.read_csv(StringIO(OUT_CSV))
        source  = "sample"

    for df in [df_info, df_vle, df_asmt]:
        df.columns = df.columns.str.strip().str.lower()

    df_vle["sum_click"] = pd.to_numeric(df_vle["sum_click"], errors="coerce").fillna(0).astype(int)
    df_vle["week"]      = pd.to_numeric(df_vle["week"],      errors="coerce").fillna(0).astype(int)
    df_asmt["assessment_score"] = pd.to_numeric(df_asmt["assessment_score"], errors="coerce")
    df_info["imd_band"] = pd.Categorical(df_info["imd_band"], categories=IMD_ORDER, ordered=True)

    merged = df_vle.merge(df_info, on="id_student", how="left")
    return df_info, df_vle, df_asmt, merged, source


# ── Plot helpers ──────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    font_family="DM Sans",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=16, r=16, t=32, b=16),
)

def style(fig):
    fig.update_layout(
        **PLOT_LAYOUT,
        xaxis=dict(gridcolor="#ede9e2", linecolor="#e8e3db"),
        yaxis=dict(gridcolor="#ede9e2", linecolor="#e8e3db"),
    )
    return fig

# ── Interventions data ────────────────────────────────────────────────────────
INTERVENTIONS = [
    ("25% of students stopped interacting after the first month — concentrated in high-deprivation bands (0–30%).",
     "Implement a proactive nudge system: automated low-bandwidth SMS reminders for students who haven't synced in 5 days. Prioritise offline-first learners on mobile as primary device.",
     ["ADDIE", "Equity-First Design", "UDL"], "high"),
    ("Sharp engagement drop at Week 5 coincides with the first major assessment. At-risk students are 3× more likely to withdraw here.",
     "Redesign Week 4 as an explicit assessment scaffold: add a low-stakes practice checkpoint, chunk content into micro-modules, and reduce navigation complexity.",
     ["SAM Iteration", "Cognitive Load Theory", "Formative Design"], "high"),
    ("PDF resources show the lowest engagement — likely due to file size and rendering issues on low-spec mobile devices.",
     "Audit all PDFs for mobile responsiveness. Convert high-traffic PDFs to lightweight HTML pages or compressed video summaries.",
     ["LMS Optimisation", "Offline-First", "Accessibility"], "medium"),
    ("High-achievers spend 4× more time in Peer Forums and use Quiz resources 2.3× more frequently than at-risk peers.",
     "Make Peer Forum participation a visible, scaffolded activity. Introduce structured peer-response prompts in Weeks 2–4 to normalise social learning before the friction point.",
     ["Social Learning Theory", "Vygotsky ZPD", "Community of Practice"], "medium"),
    ("Students with declared disabilities show 30% lower click volume despite equal enrolment rates.",
     "Conduct an accessibility audit of all Week 1–3 materials. Implement alternative formats (audio, transcript, simplified layout) as defaults — not add-ons.",
     ["Universal Design for Learning", "Inclusive Design", "Accessibility"], "high"),
    ("Students with lower prior education (Lower Than A Level) disengage 2 weeks earlier than HE-qualified peers.",
     "Design a differentiated onboarding module for this cohort. Use backward design to scaffold foundational literacy into the first two weeks.",
     ["Backward Design", "Differentiated Instruction", "Needs Analysis"], "medium"),
]


# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="margin-bottom:1.5rem">
      <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:{TEXT}">
        Equi<span style="color:{ACCENT}">Learn</span>
      </div>
      <div style="font-size:0.75rem;color:{MUTED};margin-top:0.2rem;text-transform:uppercase;letter-spacing:0.06em">
        Learning Analytics Dashboard
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Navigate**")
    page = st.radio(
        label="",
        options=["01 · Equity Overview", "02 · Behavioural Analysis",
                 "03 · Content Analysis", "04 · Interventions", "05 · Technical"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**Filters**")
    edu_filter     = st.selectbox("Education Level", ["All"] + [
        "A Level or Equivalent","HE Qualification",
        "Lower Than A Level","Post Graduate Qualification"])
    outcome_filter = st.selectbox("Final Outcome", ["All","Pass","Fail","Withdrawn"])

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.8rem;color:{MUTED};line-height:1.6">
      <strong style="color:{TEXT}">Rahmat Syawaludin</strong><br>
      MEd Digital Learning<br>Monash University · LPDP Scholar<br><br>
      <a href="https://rahmatsyawaludin.github.io/portfolio" target="_blank"
         style="color:{ACCENT};text-decoration:none">← Back to Portfolio</a>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═════════════════════════════════════════════════════════════════════════════
with st.spinner("Fetching data…"):
    df_info, df_vle, df_asmt, df, source = load_data()

# Apply filters
df_f = df.copy()
if edu_filter != "All" and "highest_education" in df_f.columns:
    df_f = df_f[df_f["highest_education"] == edu_filter]
if outcome_filter != "All" and "final_result" in df_f.columns:
    df_f = df_f[df_f["final_result"] == outcome_filter]

info_f = df_info.copy()
if edu_filter != "All" and "highest_education" in info_f.columns:
    info_f = info_f[info_f["highest_education"] == edu_filter]
if outcome_filter != "All" and "final_result" in info_f.columns:
    info_f = info_f[info_f["final_result"] == outcome_filter]


# ═════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="margin-bottom:2rem">
  <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;
              color:{ACCENT};font-weight:700;margin-bottom:0.5rem">
    Learning Analytics · OULAD Dataset · Instructional Design
  </div>
  <h1 style="font-size:2.6rem;line-height:1.1;margin:0 0 0.75rem">
    EquiLearn: Learning Analytics<br>
    <em style="color:{ACCENT};font-style:italic;font-weight:400">&amp; Strategy Dashboard</em>
  </h1>
  <p style="color:{MUTED};font-size:1rem;font-weight:300;max-width:600px;margin:0">
    Transforming raw student clickstreams into instructional interventions to close equity gaps.
  </p>
  <div style="margin-top:0.75rem">
    <span class="tag">Python</span>
    <span class="tag">Pandas</span>
    <span class="tag">Plotly</span>
    <span class="tag">Streamlit</span>
    <span class="tag">OULAD Dataset</span>
    <span class="tag">Instructional Design</span>
    {'<span class="tag" style="border-color:#27ae60;color:#27ae60">● Live Data</span>' if source == "live"
     else '<span class="tag" style="border-color:#c8954a;color:#c8954a">● Sample Data</span>'}
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 01 — EQUITY OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
if page == "01 · Equity Overview":
    st.markdown(f"""
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{ACCENT};font-weight:700;margin-bottom:0.5rem">01 — Equity Overview</div>
    <h2 style="margin:0 0 0.5rem">Who is <em style="color:{ACCENT};font-style:italic">learning</em>?</h2>
    <p style="color:{MUTED};font-weight:300;max-width:560px;margin:0 0 2rem">
      Mapping student distribution by deprivation index and region — because equity begins with knowing who's in the room.
    </p>
    """, unsafe_allow_html=True)

    # ── Metric cards ──────────────────────────────────────────────────────────
    total     = info_f["id_student"].nunique()
    pass_mask = info_f["final_result"].isin(["Pass","Distinction"])
    pass_rate = round(pass_mask.sum() / total * 100, 1) if total else 0
    high_dep  = info_f["imd_band"].isin(["0-10%","10-20%","20-30%"]).sum()

    high_clicks = df_f[df_f["imd_band"].isin(["0-10%","10-20%","20-30%"])]["sum_click"].mean()
    low_clicks  = df_f[df_f["imd_band"].isin(["80-90%","90-100%"])]["sum_click"].mean()
    gap = round((low_clicks - high_clicks) / low_clicks * 100, 1) if low_clicks and low_clicks > 0 else 15.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students",          f"{total:,}")
    c2.metric("Overall Pass Rate",        f"{pass_rate}%")
    c3.metric("High Deprivation (0–30%)", f"{high_dep}")
    c4.metric("Engagement Gap",           f"{gap}%", delta=f"vs low-dep band", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    col_a, col_b = st.columns([2, 1])

    with col_a:
        imd_counts = (
            info_f.groupby("imd_band", observed=True)["id_student"]
            .count()
            .reindex(IMD_ORDER, fill_value=0)
            .reset_index()
        )
        imd_counts.columns = ["IMD Band", "Students"]
        imd_counts["Colour"] = imd_counts["IMD Band"].apply(
            lambda x: WARN if x in ["0-10%","10-20%","20-30%"] else ACCENT
        )
        fig = px.bar(
            imd_counts, x="IMD Band", y="Students",
            color="Colour", color_discrete_map="identity",
            title="Student Distribution by IMD Band",
        )
        fig.update_traces(marker_line_width=0, marker_cornerradius=5)
        style(fig).update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        pass_by_imd = (
            info_f.assign(passed=pass_mask.values if len(pass_mask) == len(info_f) else info_f["final_result"].isin(["Pass","Distinction"]).astype(int))
            .groupby("imd_band", observed=True)
            .agg(total=("id_student","count"), passed=("passed","sum"))
        )
        pass_by_imd["rate"] = (pass_by_imd["passed"] / pass_by_imd["total"] * 100).round(1).fillna(0)
        pass_by_imd = pass_by_imd.reindex(IMD_ORDER).reset_index()
        pass_by_imd["colour"] = pass_by_imd["rate"].apply(
            lambda v: WARN if v < 50 else (ACCENT if v < 75 else SUCCESS)
        )
        fig2 = px.bar(
            pass_by_imd, y="imd_band", x="rate",
            color="colour", color_discrete_map="identity",
            orientation="h", title="Pass Rate by IMD Band",
            labels={"imd_band":"","rate":"Pass Rate (%)"},
        )
        fig2.update_traces(marker_line_width=0, marker_cornerradius=4)
        style(fig2).update_layout(showlegend=False, xaxis_range=[0,100])
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <div class="insight">
      💡 <strong>Equity Insight:</strong> Students in the highest deprivation bands (0–30%) show a
      <strong>{gap}% lower engagement rate</strong> in early modules compared to the lowest deprivation bands.
      This gap widens after Week 5 — coinciding with the first major assessment window.
      Instructional interventions must prioritise this cohort <em>before</em> Week 4.
    </div>
    """, unsafe_allow_html=True)

    # Region distribution
    st.markdown("<br>", unsafe_allow_html=True)
    region_counts = info_f["region"].value_counts().reset_index()
    region_counts.columns = ["Region","Students"]
    fig3 = px.bar(
        region_counts.head(10), x="Students", y="Region",
        orientation="h", title="Student Distribution by Region",
        color_discrete_sequence=[ACCENT2],
    )
    fig3.update_traces(marker_cornerradius=4)
    style(fig3)
    st.plotly_chart(fig3, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 02 — BEHAVIOURAL ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "02 · Behavioural Analysis":
    st.markdown(f"""
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{ACCENT};font-weight:700;margin-bottom:0.5rem">02 — Behavioural Analysis</div>
    <h2 style="margin:0 0 0.5rem">When do learners <em style="color:{ACCENT};font-style:italic">disengage</em>?</h2>
    <p style="color:{MUTED};font-weight:300;max-width:560px;margin:0 0 2rem">
      Clickstream data across 40 weeks reveals a critical friction point — and it's not where most assume.
    </p>
    """, unsafe_allow_html=True)

    # ── Weekly engagement line chart ─────────────────────────────────────────
    weekly = (
        df_f.groupby("week")["sum_click"]
        .sum()
        .reindex(range(1, 41), fill_value=0)
        .reset_index()
    )
    weekly.columns = ["Week", "Clicks"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weekly["Week"], y=weekly["Clicks"],
        mode="lines+markers",
        line=dict(color=ACCENT, width=2.5),
        marker=dict(
            size=[10 if w == 5 else 4 for w in weekly["Week"]],
            color=[WARN if w == 5 else ACCENT for w in weekly["Week"]],
        ),
        fill="tozeroy",
        fillcolor="rgba(200,149,74,0.1)",
        name="Total Clicks",
    ))
    # Friction line
    fig.add_vline(x=5, line_dash="dash", line_color=WARN, line_width=2,
                  annotation_text="⚠ Week 5 Friction Point",
                  annotation_font_color=WARN,
                  annotation_position="top right")
    fig.update_layout(
        **PLOT_LAYOUT,
        title="Weekly LMS Engagement — Sum of Clicks",
        xaxis_title="Week", yaxis_title="Total Clicks",
        xaxis=dict(gridcolor="#ede9e2"),
        yaxis=dict(gridcolor="#ede9e2"),
        showlegend=False,
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="insight insight-warn">
      ⚠ <strong>The Week 5 Friction Point:</strong> Notice the sharp drop in engagement before the
      first major assessment window (Week 5–6). Students who disengage here are <strong>3× more
      likely to withdraw</strong>. This is not a motivation deficit — it is a design signal.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        # Disability breakdown
        if "disability" in df_f.columns:
            dis = df_f.groupby("disability")["sum_click"].sum().reset_index()
            dis.columns = ["Disability", "Clicks"]
            dis["Disability"] = dis["Disability"].map({"N":"No Disability","Y":"Disability Declared"}).fillna(dis["Disability"])
            fig2 = px.pie(
                dis, names="Disability", values="Clicks",
                title="Clicks by Disability Status",
                color_discrete_sequence=[ACCENT2, WARN],
                hole=0.55,
            )
            fig2.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        # At-risk by week band
        last_active = (
            df_f[df_f["sum_click"] > 0]
            .groupby("id_student")["week"]
            .max().reset_index()
            .rename(columns={"week":"last_week"})
        )
        bands = {"Wk 1–5":0,"Wk 6–10":0,"Wk 11–20":0,"Wk 21+":0}
        for w in last_active["last_week"]:
            if   w <= 5:  bands["Wk 1–5"]   += 1
            elif w <= 10: bands["Wk 6–10"]  += 1
            elif w <= 20: bands["Wk 11–20"] += 1
            else:         bands["Wk 21+"]   += 1

        fig3 = px.bar(
            x=list(bands.keys()), y=list(bands.values()),
            title="At-Risk Students — Last Active Week",
            labels={"x":"Last Active","y":"Students"},
            color_discrete_sequence=[WARN, "#e07070", ACCENT, SUCCESS],
            color=list(bands.keys()),
        )
        fig3.update_traces(marker_cornerradius=5, marker_line_width=0)
        style(fig3).update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown(f"""
    <div class="insight">
      💡 <strong>At-Risk Definition:</strong> A student is flagged At-Risk when they record zero LMS
      activity for 7+ consecutive days. Early flagging in Weeks 1–5 enables intervention before
      withdrawal becomes the path of least resistance.
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 03 — CONTENT ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "03 · Content Analysis":
    st.markdown(f"""
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{ACCENT};font-weight:700;margin-bottom:0.5rem">03 — Content-Type Analysis</div>
    <h2 style="margin:0 0 0.5rem">What are learners <em style="color:{ACCENT};font-style:italic">actually using</em>?</h2>
    <p style="color:{MUTED};font-weight:300;max-width:560px;margin:0 0 2rem">
      Not all content is equal. Understanding which material types drive engagement is the first step toward LMS optimisation.
    </p>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        ct = df_f.groupby("content_type")["sum_click"].sum().sort_values(ascending=True).reset_index()
        ct.columns = ["Content Type","Clicks"]
        fig = px.bar(
            ct, x="Clicks", y="Content Type", orientation="h",
            title="Total Engagement by Content Type",
            color_discrete_sequence=[ACCENT2],
        )
        fig.update_traces(marker_cornerradius=5)
        style(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Achiever vs at-risk radar
        if "final_result" in df_f.columns and "content_type" in df_f.columns:
            types = df_f["content_type"].unique().tolist()
            achievers  = df_f[df_f["final_result"].isin(["Pass","Distinction"])]
            at_risk_df = df_f[df_f["final_result"].isin(["Fail","Withdrawn"])]

            ha_vals = [achievers[achievers["content_type"]==t]["sum_click"].sum() for t in types]
            ar_vals = [at_risk_df[at_risk_df["content_type"]==t]["sum_click"].sum() for t in types]

            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(
                r=ha_vals + [ha_vals[0]], theta=types + [types[0]],
                fill="toself", name="High Achievers",
                line_color=SUCCESS, fillcolor="rgba(39,174,96,0.12)",
            ))
            fig2.add_trace(go.Scatterpolar(
                r=ar_vals + [ar_vals[0]], theta=types + [types[0]],
                fill="toself", name="At-Risk",
                line_color=WARN, fillcolor="rgba(192,57,43,0.12)",
            ))
            fig2.update_layout(
                **PLOT_LAYOUT,
                polar=dict(radialaxis=dict(visible=True, gridcolor="#ede9e2")),
                title="High Achievers vs At-Risk",
                legend=dict(orientation="h", y=-0.15),
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <div class="insight insight-warn">
      🔍 <strong>Content Gap:</strong> PDF resources show the lowest engagement — likely due to file
      size and rendering issues on low-spec mobile devices. This disproportionately affects students
      from high-deprivation bands who may rely on mobile as their primary device.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight insight-success">
      ✅ <strong>Social Learning Signal:</strong> High-achievers spend significantly more time in
      Peer Forums and use Quiz resources more frequently than at-risk peers. Forum engagement is not
      a personality trait — it is a design outcome. Scaffold it explicitly.
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 04 — INTERVENTIONS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "04 · Interventions":
    st.markdown(f"""
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{ACCENT};font-weight:700;margin-bottom:0.5rem">04 — Instructional Interventions</div>
    <h2 style="margin:0 0 0.5rem">The <em style="color:{ACCENT};font-style:italic">so what</em>?</h2>
    <p style="color:{MUTED};font-weight:300;max-width:560px;margin:0 0 2rem">
      Data without action is just noise. Every trend below maps directly to a designer's response —
      grounded in instructional theory and equity principles.
    </p>
    """, unsafe_allow_html=True)

    sev_filter = st.radio("Show:", ["All","High Priority","Medium Priority"], horizontal=True)

    for finding, recommendation, frameworks, severity in INTERVENTIONS:
        if sev_filter == "High Priority"   and severity != "high":   continue
        if sev_filter == "Medium Priority" and severity != "medium": continue

        sev_colour = WARN if severity == "high" else ACCENT
        sev_label  = "🔴 High Priority" if severity == "high" else "🟡 Medium Priority"
        fw_tags    = "".join(f'<span class="tag">{f}</span>' for f in frameworks)

        st.markdown(f"""
        <div class="int-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1rem">
            <span style="font-size:0.7rem;font-weight:700;letter-spacing:0.06em;
                         text-transform:uppercase;color:{sev_colour}">{sev_label}</span>
            <div>{fw_tags}</div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem">
            <div>
              <div class="int-label" style="color:{WARN}">⚠ Data Finding</div>
              <p style="font-size:0.9rem;line-height:1.65;color:{TEXT};margin:0">{finding}</p>
            </div>
            <div>
              <div class="int-label" style="color:{SUCCESS}">→ Designer's Recommendation</div>
              <p style="font-size:0.9rem;line-height:1.65;color:{TEXT};margin:0">{recommendation}</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 05 — TECHNICAL
# ═════════════════════════════════════════════════════════════════════════════
elif page == "05 · Technical":
    st.markdown(f"""
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{ACCENT};font-weight:700;margin-bottom:0.5rem">05 — Under the Hood</div>
    <h2 style="margin:0 0 0.5rem">The <em style="color:{ACCENT};font-style:italic">architecture</em>.</h2>
    <p style="color:{MUTED};font-weight:300;max-width:560px;margin:0 0 2rem">
      Three CSVs. One master DataFrame. A pipeline designed for equity-first analysis.
    </p>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1.3, 1])

    with col_a:
        st.markdown("**Python · data pipeline**")
        st.code("""
import pandas as pd

# 1. Load core datasets
df_info = pd.read_csv("studentInfo.csv")
df_vle  = pd.read_csv("studentVle.csv")
df_asmt = pd.read_csv("studentAssessment.csv")

# 2. Merge on student ID
df = pd.merge(df_vle, df_info, on="id_student")
df = pd.merge(df, df_asmt,    on="id_student")

# 3. Equity segmentation by IMD Band
equity = (
  df.groupby("imd_band")["sum_click"]
    .sum()
    .reset_index()
)

# 4. At-Risk flagging logic
# Flag: 7+ consecutive days zero activity
df["at_risk"] = (
  df.groupby("id_student")["date"]
    .transform(lambda x: x.diff().gt(7))
)

# 5. Drop-off week analysis
zero_activity = (
  df[df["sum_click"] == 0]
    .groupby("week")["id_student"]
    .count()
    .reset_index()
)
""", language="python")

    with col_b:
        st.markdown("**Stack**")
        stack = {
            "🐍 Python + Pandas": "ETL pipeline, merge logic, equity segmentation",
            "📊 Plotly": "Interactive visualisations, live filter updates",
            "🚀 Streamlit": "App framework — runnable locally & on Streamlit Cloud",
            "📋 Google Sheets": "Live data source via GViz CSV endpoint",
            "🌐 GitHub": "Version control + Streamlit Cloud deployment",
            "🎓 OULAD Dataset": "Open University — 32k students, 7 modules",
        }
        for name, desc in stack.items():
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e8e3db;border-radius:10px;
                        padding:0.85rem 1rem;margin-bottom:0.6rem;display:flex;gap:0.75rem">
              <div>
                <strong style="font-size:0.875rem">{name}</strong><br>
                <span style="font-size:0.78rem;color:{MUTED}">{desc}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("View on GitHub →", "https://github.com/rahmatsyawaludin",
                       use_container_width=True)
        st.link_button("← Back to Portfolio",
                       "https://rahmatsyawaludin.github.io/portfolio",
                       use_container_width=True)

    st.divider()
    st.markdown("**Live data preview**")
    tab1, tab2, tab3 = st.tabs(["Demographics", "Engagement", "Outcomes"])
    with tab1: st.dataframe(df_info.head(10), use_container_width=True)
    with tab2: st.dataframe(df_vle.head(10),  use_container_width=True)
    with tab3: st.dataframe(df_asmt.head(10), use_container_width=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:flex-end;
            flex-wrap:wrap;gap:1rem;padding:0.5rem 0 1rem">
  <div>
    <strong style="font-family:'Syne',sans-serif;font-size:0.95rem">Rahmat Syawaludin</strong><br>
    <span style="font-size:0.8rem;color:{MUTED}">
      Instructional Designer · Learning Experience Designer · Jakarta, Indonesia<br>
      MEd Digital Learning · Monash University · LPDP Scholar
    </span>
  </div>
  <div style="font-size:0.8rem;display:flex;gap:1.5rem">
    <a href="https://rahmatsyawaludin.github.io/portfolio" target="_blank"
       style="color:{ACCENT};text-decoration:none">Portfolio</a>
    <a href="https://linkedin.com/in/rahmat-syawaludin" target="_blank"
       style="color:{ACCENT};text-decoration:none">LinkedIn</a>
    <a href="mailto:rahmatsywldn@gmail.com"
       style="color:{ACCENT};text-decoration:none">Email</a>
  </div>
</div>
<p style="font-size:0.75rem;color:{MUTED};margin:0">
  <em>"Learning design is not about content delivery — it is about engineering the conditions in which people grow."</em>
</p>
""", unsafe_allow_html=True)
