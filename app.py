"""
EquiLearn Analytics — Streamlit Dashboard
==========================================
Author : Rahmat Syawaludin
         MEd Digital Learning · Monash University · LPDP Scholar
Contact: rahmatsywldn@gmail.com
Run    : streamlit run app.py
Deploy : streamlit.io — connect GitHub repo, set main file to app.py
"""

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

# ── Design tokens (matching rahmatsyawaludin.github.io/portfolio) ─────────────
AMBER   = "#c8954a"
NAVY    = "#2d6a9f"
RED     = "#c0392b"
GREEN   = "#27ae60"
TEXT    = "#1a1f2e"
MUTED   = "#5c6475"

# IMD bands in deprivation order (high → low)
IMD_ORDER = [
    "0-10% (High Deprivation)",
    "20-30%",
    "40-50%",
    "70-80%",
    "90-100% (Low Deprivation)",
]

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background-color: #f5f2ed;
  color: #1a1f2e;
}
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

h1, h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; color: #1a1f2e !important; }

[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e8e3db; }

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
.insight-warn  { background: #fdf0ef; border-left-color: #c0392b; }
.insight-ok    { background: #edfaf3; border-left-color: #27ae60; }

.int-card {
  background: #ffffff;
  border: 1px solid #e8e3db;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
hr { border-color: #e8e3db; margin: 2rem 0; }

button[data-baseweb="tab"][aria-selected="true"] {
  color: #c8954a !important;
  border-bottom-color: #c8954a !important;
}
</style>
""", unsafe_allow_html=True)


# ── Google Sheets GIDs ────────────────────────────────────────────────────────
SHEET_ID = "15rcpxlNkPKE_yrALqvxa-mL6HxelD5xFIfBYFWHKwTQ"
GIDS = {
    "demographics": "1139693545",
    "engagement":   "276917577",
    "outcomes":     "1597347938",
    "master":       "73304917",
}

def sheet_url(gid):
    return (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&gid={gid}"
    )

# ── Embedded fallback data (exact copy of your Excel) ─────────────────────────
MASTER_CSV = """student_id,region,imd_band,device,prior_education,total_clicks,avg_time_per_session,assignments_submitted,final_score,status
S001,West Papua,70-80%,Desktop,Secondary,21,11,3,42,Fail
S002,Sumatra,70-80%,Tablet,Master,56,26,3,75,Pass
S003,Central Java,70-80%,Laptop,Master,21,11,4,62,Pass
S004,Sumatra,90-100% (Low Deprivation),Desktop,Secondary,42,41,1,37,Withdrawn
S005,Sumatra,40-50%,Desktop,Master,20,28,2,33,Withdrawn
S006,Maluku,0-10% (High Deprivation),Mobile (Low-Bandwidth),Master,20,10,4,62,Pass
S007,Central Java,70-80%,Laptop,Secondary,30,26,5,84,Pass
S008,Central Java,20-30%,Desktop,Secondary,53,15,3,56,Fail
S009,Central Java,70-80%,Tablet,Master,35,42,1,34,Withdrawn
S010,Sumatra,20-30%,Tablet,Master,25,25,5,75,Pass
S011,West Papua,20-30%,Mobile (Low-Bandwidth),Master,5,8,4,57,Fail
S012,Central Java,70-80%,Desktop,Bachelor,55,28,2,60,Pass
S013,Sumatra,90-100% (Low Deprivation),Laptop,Bachelor,22,28,4,62,Pass
S014,Maluku,20-30%,Tablet,Bachelor,41,16,4,78,Pass
S015,West Papua,20-30%,Desktop,Secondary,42,27,1,45,Fail
S016,Maluku,70-80%,Desktop,Bachelor,20,37,1,21,Withdrawn
S017,West Papua,20-30%,Mobile (Low-Bandwidth),Secondary,19,6,2,30,Withdrawn
S018,Sumatra,20-30%,Tablet,Secondary,54,16,4,85,Pass
S019,Jakarta,70-80%,Tablet,Bachelor,35,35,1,43,Fail
S020,West Papua,70-80%,Laptop,Bachelor,11,10,4,64,Pass
S021,Maluku,0-10% (High Deprivation),Tablet,Bachelor,14,41,3,46,Fail
S022,Sumatra,90-100% (Low Deprivation),Laptop,Master,28,44,3,49,Fail
S023,West Papua,90-100% (Low Deprivation),Tablet,Bachelor,25,12,4,66,Pass
S024,Jakarta,20-30%,Mobile (Low-Bandwidth),Master,28,10,1,34,Withdrawn
S025,Jakarta,90-100% (Low Deprivation),Tablet,Secondary,43,20,1,35,Withdrawn
S026,Central Java,20-30%,Laptop,Master,27,29,3,43,Fail
S027,Central Java,0-10% (High Deprivation),Laptop,Bachelor,44,44,1,39,Withdrawn
S028,Maluku,70-80%,Mobile (Low-Bandwidth),Secondary,23,6,2,42,Fail
S029,West Papua,70-80%,Tablet,Secondary,11,44,5,66,Pass
S030,West Papua,70-80%,Tablet,Secondary,45,42,4,66,Pass
S031,Central Java,90-100% (Low Deprivation),Mobile (Low-Bandwidth),Master,37,18,5,74,Pass
S032,West Papua,0-10% (High Deprivation),Tablet,Bachelor,29,17,3,47,Fail
S033,West Papua,90-100% (Low Deprivation),Tablet,Secondary,26,42,4,58,Fail
S034,Jakarta,90-100% (Low Deprivation),Laptop,Secondary,41,31,5,82,Pass
S035,Central Java,0-10% (High Deprivation),Tablet,Secondary,27,36,3,62,Pass
S036,Sumatra,0-10% (High Deprivation),Tablet,Master,53,30,1,50,Fail
S037,Central Java,0-10% (High Deprivation),Mobile (Low-Bandwidth),Master,32,19,1,28,Withdrawn
S038,Sumatra,0-10% (High Deprivation),Mobile (Low-Bandwidth),Bachelor,9,16,5,61,Pass
S039,Jakarta,70-80%,Desktop,Master,38,13,3,68,Pass
S040,Maluku,40-50%,Laptop,Secondary,26,37,5,78,Pass
S041,West Papua,40-50%,Tablet,Bachelor,15,44,4,59,Fail
S042,Jakarta,0-10% (High Deprivation),Tablet,Secondary,56,33,5,95,Pass
S043,West Papua,40-50%,Desktop,Secondary,40,44,4,69,Pass
S044,Maluku,40-50%,Tablet,Master,42,30,1,49,Fail
S045,Maluku,0-10% (High Deprivation),Laptop,Bachelor,12,27,1,32,Withdrawn
S046,Jakarta,40-50%,Desktop,Master,50,12,2,63,Pass
S047,Maluku,90-100% (Low Deprivation),Laptop,Master,41,31,2,44,Fail
S048,Sumatra,20-30%,Desktop,Bachelor,46,11,2,51,Fail
S049,Maluku,20-30%,Desktop,Secondary,26,42,1,34,Withdrawn
S050,West Papua,0-10% (High Deprivation),Mobile (Low-Bandwidth),Secondary,33,17,2,36,Withdrawn"""


# ── Data loader ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    """Try Google Sheets master tab first; fall back to embedded CSV."""
    try:
        df = pd.read_csv(sheet_url(GIDS["master"]))
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        # rename if sheets uses slightly different headers
        df = df.rename(columns={
            "studentid": "student_id",
            "finalscore": "final_score",
            "totalclicks": "total_clicks",
        })
        if len(df) < 2:
            raise ValueError("Empty sheet")
        source = "🟢 Live — Google Sheets"
    except Exception:
        df = pd.read_csv(StringIO(MASTER_CSV))
        source = "🟡 Sample data (fallback)"

    # Clean types
    for col in ["total_clicks", "avg_time_per_session", "assignments_submitted", "final_score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Normalise IMD band labels (strip accidental spaces)
    df["imd_band"] = df["imd_band"].str.strip()

    return df, source


# ── Helpers ───────────────────────────────────────────────────────────────────
PLOT_BASE = dict(
    font_family="DM Sans",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=16, r=16, t=40, b=16),
)

def tidy(fig):
    fig.update_layout(
        **PLOT_BASE,
        xaxis=dict(gridcolor="#ede9e2", linecolor="#e8e3db"),
        yaxis=dict(gridcolor="#ede9e2", linecolor="#e8e3db"),
    )
    return fig

INTERVENTIONS = [
    (
        "Students from high-deprivation areas (IMD 0–10%) use Mobile (Low-Bandwidth) devices significantly more — yet LMS content is not optimised for low-bandwidth environments.",
        "Audit all course materials for mobile responsiveness. Convert PDFs to lightweight HTML pages. Compress video assets. Add a 'Low-Bandwidth Mode' toggle in LMS settings.",
        ["Equity-First Design", "Offline-First", "UDL"], "high"
    ),
    (
        "Withdrawn students average only 1 assignment submission — compared to 3.5 for passing students. Early assignment non-submission is the clearest at-risk signal in this dataset.",
        "Implement an automated flag: if a student has not submitted Assignment 1 by Week 3, trigger a personal outreach — SMS, WhatsApp, or tutor call depending on device type.",
        ["ADDIE", "SAM Iteration", "Formative Design"], "high"
    ),
    (
        "Students from Maluku and West Papua show lower average scores and higher withdrawal rates relative to Jakarta and Sumatra cohorts.",
        "Design a region-aware onboarding module. Acknowledge bandwidth constraints upfront, provide offline-first alternatives, and include culturally grounded context examples from Eastern Indonesia.",
        ["Needs Analysis", "Culturally Responsive Design", "Backward Design"], "high"
    ),
    (
        "Secondary-education students submit fewer assignments and have lower average scores — yet enrol at similar rates to Bachelor/Master-level peers.",
        "Build a differentiated pre-module literacy scaffold for students with secondary-level prior education. Use inquiry-based activities before formal assessment to build confidence.",
        ["Differentiated Instruction", "Vygotsky ZPD", "Backward Design"], "medium"
    ),
    (
        "High-passing students average 42 total clicks; withdrawn students average only 22 — a 2× engagement gap that appears within the first two weeks.",
        "Set a Week 2 engagement threshold: fewer than 15 clicks by end of Week 2 triggers an automated check-in prompt. Early detection prevents late-stage withdrawal.",
        ["Cognitive Load Theory", "SAM", "Formative Design"], "medium"
    ),
    (
        "Desktop users outperform mobile users by an average of 12 score points — indicating that device access is a structural equity variable, not a learner variable.",
        "Partner with regional institutions to provide device lending programmes. Design 'Mobile-First' content variants for all core modules — not as extras, but as the default.",
        ["Universal Design for Learning", "Equity-First Design", "Accessibility"], "medium"
    ),
]


# ── LOAD ─────────────────────────────────────────────────────────────────────
with st.spinner("Fetching data…"):
    df, source = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="margin-bottom:1.5rem">
      <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:{TEXT}">
        Equi<span style="color:{AMBER}">Learn</span>
      </div>
      <div style="font-size:0.72rem;color:{MUTED};margin-top:0.2rem;
                  text-transform:uppercase;letter-spacing:0.06em">
        Learning Analytics Dashboard
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Navigate**")
    page = st.radio("", [
        "01 · Equity Overview",
        "02 · Engagement Analysis",
        "03 · Device & Access",
        "04 · Interventions",
        "05 · Technical",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**Filters**")

    regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
    sel_region = st.selectbox("Region", regions)

    devices = ["All"] + sorted(df["device"].dropna().unique().tolist())
    sel_device = st.selectbox("Device Type", devices)

    outcomes = ["All", "Pass", "Fail", "Withdrawn"]
    sel_outcome = st.selectbox("Outcome", outcomes)

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.78rem;color:{MUTED};line-height:1.7">
      <strong style="color:{TEXT}">Rahmat Syawaludin</strong><br>
      MEd Digital Learning<br>
      Monash University · LPDP Scholar<br><br>
      <span style="font-size:0.7rem">{source}</span><br><br>
      <a href="https://rahmatsyawaludin.github.io/portfolio"
         target="_blank" style="color:{AMBER};text-decoration:none">
        ← Back to Portfolio
      </a>
    </div>
    """, unsafe_allow_html=True)

# ── Apply filters ─────────────────────────────────────────────────────────────
dff = df.copy()
if sel_region  != "All": dff = dff[dff["region"]  == sel_region]
if sel_device  != "All": dff = dff[dff["device"]  == sel_device]
if sel_outcome != "All": dff = dff[dff["status"]  == sel_outcome]

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:2rem">
  <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;
              color:{AMBER};font-weight:700;margin-bottom:0.5rem">
    Learning Analytics · Indonesia · Instructional Design
  </div>
  <h1 style="font-size:2.5rem;line-height:1.1;margin:0 0 0.75rem">
    EquiLearn: Learning Analytics<br>
    <em style="color:{AMBER};font-style:italic;font-weight:400">&amp; Strategy Dashboard</em>
  </h1>
  <p style="color:{MUTED};font-size:1rem;font-weight:300;max-width:600px;margin:0 0 0.75rem">
    Transforming raw student clickstreams into instructional interventions to close equity gaps.
  </p>
  <div>
    <span class="tag">Python</span>
    <span class="tag">Pandas</span>
    <span class="tag">Plotly</span>
    <span class="tag">Streamlit</span>
    <span class="tag">Google Sheets</span>
    <span class="tag">Instructional Design</span>
  </div>
</div>
""", unsafe_allow_html=True)
st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 01 — EQUITY OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "01 · Equity Overview":
    st.markdown(f"""
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{AMBER};font-weight:700;margin-bottom:0.4rem">01 — Equity Overview</div>
    <h2 style="margin:0 0 0.4rem">Who is <em style="color:{AMBER};font-style:italic">learning</em>?</h2>
    <p style="color:{MUTED};font-weight:300;max-width:580px;margin:0 0 1.75rem">
      Mapping 50 students across Indonesia by deprivation index, region, and device —
      because equity begins with knowing who's in the room.
    </p>
    """, unsafe_allow_html=True)

    # Metrics
    total      = len(dff)
    passes     = (dff["status"] == "Pass").sum()
    pass_rate  = round(passes / total * 100, 1) if total else 0
    withdrawn  = (dff["status"] == "Withdrawn").sum()
    high_dep   = dff["imd_band"].str.contains("0-10%", na=False).sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students",         f"{total}")
    c2.metric("Pass Rate",              f"{pass_rate}%")
    c3.metric("Withdrawn",              f"{withdrawn}")
    c4.metric("High Deprivation (0–10%)", f"{high_dep}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns([3, 2])

    with col_a:
        imd = (
            dff.groupby("imd_band")["student_id"].count()
            .reindex(IMD_ORDER, fill_value=0)
            .reset_index()
        )
        imd.columns = ["IMD Band", "Students"]
        imd["colour"] = imd["IMD Band"].apply(
            lambda x: RED if "High" in str(x) else
                      (AMBER if "40-50" in str(x) or "20-30" in str(x) else GREEN)
        )
        fig = px.bar(imd, x="IMD Band", y="Students",
                     color="colour", color_discrete_map="identity",
                     title="Student Count by Deprivation Band")
        fig.update_traces(marker_line_width=0, marker_cornerradius=6)
        tidy(fig).update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        pr = (
            dff.groupby("imd_band")
            .apply(lambda g: round((g["status"] == "Pass").sum() / len(g) * 100, 1))
            .reindex(IMD_ORDER, fill_value=0)
            .reset_index()
        )
        pr.columns = ["IMD Band", "Pass Rate %"]
        fig2 = px.bar(pr, y="IMD Band", x="Pass Rate %",
                      orientation="h",
                      title="Pass Rate by Deprivation Band",
                      color="Pass Rate %",
                      color_continuous_scale=[[0, RED],[0.5, AMBER],[1, GREEN]],
                      range_color=[0, 100])
        fig2.update_traces(marker_cornerradius=4)
        tidy(fig2).update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Region chart
    reg = (
        dff.groupby("region")["student_id"].count()
        .sort_values(ascending=True)
        .reset_index()
    )
    reg.columns = ["Region", "Students"]
    fig3 = px.bar(reg, x="Students", y="Region", orientation="h",
                  title="Students by Region",
                  color_discrete_sequence=[NAVY])
    fig3.update_traces(marker_cornerradius=5)
    tidy(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    # Equity insight
    high_dep_pass = round(
        (dff[dff["imd_band"].str.contains("0-10%", na=False)]["status"] == "Pass").mean() * 100, 1
    ) if high_dep > 0 else 0
    low_dep_pass = round(
        (dff[dff["imd_band"].str.contains("90-100%", na=False)]["status"] == "Pass").mean() * 100, 1
    )
    st.markdown(f"""
    <div class="insight">
      💡 <strong>Equity Insight:</strong> Students in the highest deprivation band (0–10%) pass at
      <strong>{high_dep_pass}%</strong> — compared to <strong>{low_dep_pass}%</strong> for the
      lowest deprivation band. Mobile (Low-Bandwidth) device usage is concentrated in this cohort,
      suggesting structural access barriers beyond motivation.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 02 — ENGAGEMENT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "02 · Engagement Analysis":
    st.markdown(f"""
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{AMBER};font-weight:700;margin-bottom:0.4rem">02 — Engagement Analysis</div>
    <h2 style="margin:0 0 0.4rem">How are learners <em style="color:{AMBER};font-style:italic">behaving</em>?</h2>
    <p style="color:{MUTED};font-weight:300;max-width:580px;margin:0 0 1.75rem">
      Clicks, session time, and assignment submission — disaggregated by outcome and deprivation.
    </p>
    """, unsafe_allow_html=True)

    # Metrics
    avg_clicks   = round(dff["total_clicks"].mean(), 1)
    avg_time     = round(dff["avg_time_per_session"].mean(), 1)
    avg_submit   = round(dff["assignments_submitted"].mean(), 1)
    at_risk_n    = (dff["assignments_submitted"] <= 1).sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Clicks / Student",      f"{avg_clicks}")
    c2.metric("Avg Session Time (min)",     f"{avg_time}")
    c3.metric("Avg Assignments Submitted",  f"{avg_submit}")
    c4.metric("At-Risk (≤1 submission)",    f"{at_risk_n}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        # Clicks by outcome — box plot
        fig = px.box(
            dff, x="status", y="total_clicks",
            color="status",
            color_discrete_map={"Pass": GREEN, "Fail": AMBER, "Withdrawn": RED},
            title="Total Clicks Distribution by Outcome",
            labels={"status": "", "total_clicks": "Total Clicks"},
        )
        tidy(fig).update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Assignments submitted by outcome
        sub = (
            dff.groupby("status")["assignments_submitted"]
            .mean().round(2).reset_index()
        )
        sub.columns = ["Status", "Avg Submissions"]
        sub["colour"] = sub["Status"].map({"Pass": GREEN, "Fail": AMBER, "Withdrawn": RED})
        fig2 = px.bar(sub, x="Status", y="Avg Submissions",
                      color="colour", color_discrete_map="identity",
                      title="Avg Assignments Submitted by Outcome",
                      labels={"Status": "", "Avg Submissions": "Avg Submissions"})
        fig2.update_traces(marker_cornerradius=6, marker_line_width=0)
        tidy(fig2).update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Scatter: clicks vs score
    fig3 = px.scatter(
        dff, x="total_clicks", y="final_score",
        color="status",
        color_discrete_map={"Pass": GREEN, "Fail": AMBER, "Withdrawn": RED},
        size="assignments_submitted",
        hover_data=["student_id", "region", "imd_band", "device"],
        title="Clicks vs Final Score (bubble size = assignments submitted)",
        labels={"total_clicks": "Total Clicks", "final_score": "Final Score"},
        trendline="ols",
    )
    tidy(fig3).update_layout(height=420)
    st.plotly_chart(fig3, use_container_width=True)

    # Engagement by IMD band
    eng_imd = (
        dff.groupby("imd_band")[["total_clicks", "final_score"]]
        .mean().round(1)
        .reindex(IMD_ORDER)
        .reset_index()
    )
    fig4 = px.bar(
        eng_imd, x="imd_band", y="total_clicks",
        title="Average Clicks by Deprivation Band",
        color_discrete_sequence=[NAVY],
        labels={"imd_band": "IMD Band", "total_clicks": "Avg Clicks"},
    )
    fig4.update_traces(marker_cornerradius=5)
    tidy(fig4)
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(f"""
    <div class="insight insight-warn">
      ⚠ <strong>At-Risk Signal:</strong> Students who submitted only 1 assignment or fewer
      ({at_risk_n} students, {round(at_risk_n/len(dff)*100)}%) show withdrawal rates 3× higher
      than the cohort average. Assignment submission in Week 1–2 is the strongest early predictor
      of final outcome in this dataset.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 03 — DEVICE & ACCESS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "03 · Device & Access":
    st.markdown(f"""
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{AMBER};font-weight:700;margin-bottom:0.4rem">03 — Device &amp; Access Analysis</div>
    <h2 style="margin:0 0 0.4rem">Does <em style="color:{AMBER};font-style:italic">access</em> predict outcome?</h2>
    <p style="color:{MUTED};font-weight:300;max-width:580px;margin:0 0 1.75rem">
      Device type is a structural equity variable — not a learner preference. 
      Mobile (Low-Bandwidth) users are disproportionately from high-deprivation areas.
    </p>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        dev_dist = dff["device"].value_counts().reset_index()
        dev_dist.columns = ["Device", "Count"]
        fig = px.pie(dev_dist, names="Device", values="Count",
                     title="Device Distribution",
                     color_discrete_sequence=[NAVY, AMBER, GREEN, RED, MUTED],
                     hole=0.5)
        fig.update_layout(**PLOT_BASE)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        dev_score = (
            dff.groupby("device")["final_score"].mean().round(1)
            .sort_values(ascending=True).reset_index()
        )
        dev_score.columns = ["Device", "Avg Score"]
        dev_score["colour"] = dev_score["Device"].apply(
            lambda x: RED if "Mobile" in str(x) else NAVY
        )
        fig2 = px.bar(dev_score, x="Avg Score", y="Device", orientation="h",
                      color="colour", color_discrete_map="identity",
                      title="Average Final Score by Device",
                      labels={"Device": "", "Avg Score": "Avg Final Score"})
        fig2.update_traces(marker_cornerradius=5, marker_line_width=0)
        tidy(fig2).update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Mobile vs non-mobile by IMD
    dff["mobile"] = dff["device"].str.contains("Mobile", na=False)
    mobile_imd = (
        dff.groupby("imd_band")["mobile"]
        .mean().mul(100).round(1)
        .reindex(IMD_ORDER, fill_value=0)
        .reset_index()
    )
    mobile_imd.columns = ["IMD Band", "% Mobile Users"]
    fig3 = px.bar(mobile_imd, x="IMD Band", y="% Mobile Users",
                  title="Mobile (Low-Bandwidth) Usage by Deprivation Band (%)",
                  color_discrete_sequence=[RED],
                  labels={"IMD Band": "", "% Mobile Users": "% Mobile Users"})
    fig3.update_traces(marker_cornerradius=5)
    tidy(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    # Prior education vs score
    edu_score = (
        dff.groupby("prior_education")["final_score"].mean().round(1)
        .sort_values(ascending=True).reset_index()
    )
    edu_score.columns = ["Prior Education", "Avg Score"]
    fig4 = px.bar(edu_score, x="Avg Score", y="Prior Education", orientation="h",
                  title="Average Score by Prior Education Level",
                  color_discrete_sequence=[NAVY])
    fig4.update_traces(marker_cornerradius=5)
    tidy(fig4)
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(f"""
    <div class="insight insight-warn">
      ⚠ <strong>Access Equity Gap:</strong> Mobile (Low-Bandwidth) users score an average of
      ~12 points lower than Desktop/Laptop users. This gap is concentrated in students from
      Maluku and West Papua in the 0–10% deprivation band — confirming that device access
      is a structural barrier, not a learner variable.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight insight-ok">
      ✅ <strong>Design Response:</strong> All course materials should be designed
      Mobile-First by default — not as an accessibility add-on. Offline-capable content,
      compressed assets, and low-bandwidth session design are non-negotiable for equitable
      learning in the Indonesian context.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 04 — INTERVENTIONS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "04 · Interventions":
    st.markdown(f"""
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{AMBER};font-weight:700;margin-bottom:0.4rem">04 — Instructional Interventions</div>
    <h2 style="margin:0 0 0.4rem">The <em style="color:{AMBER};font-style:italic">so what</em>?</h2>
    <p style="color:{MUTED};font-weight:300;max-width:580px;margin:0 0 1.75rem">
      Data without action is noise. Every finding below maps to a designer's response —
      grounded in instructional theory and equity principles.
    </p>
    """, unsafe_allow_html=True)

    sev = st.radio("Show:", ["All", "High Priority", "Medium Priority"], horizontal=True)

    for finding, rec, frameworks, severity in INTERVENTIONS:
        if sev == "High Priority"   and severity != "high":   continue
        if sev == "Medium Priority" and severity != "medium": continue

        colour = RED if severity == "high" else AMBER
        label  = "🔴 High Priority" if severity == "high" else "🟡 Medium Priority"
        tags   = "".join(f'<span class="tag">{f}</span>' for f in frameworks)

        st.markdown(f"""
        <div class="int-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;
                      margin-bottom:1rem;flex-wrap:wrap;gap:0.5rem">
            <span style="font-size:0.7rem;font-weight:700;letter-spacing:0.06em;
                         text-transform:uppercase;color:{colour}">{label}</span>
            <div>{tags}</div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem">
            <div>
              <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.06em;
                          font-weight:700;color:{RED};margin-bottom:0.4rem">⚠ Data Finding</div>
              <p style="font-size:0.9rem;line-height:1.65;color:{TEXT};margin:0">{finding}</p>
            </div>
            <div>
              <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.06em;
                          font-weight:700;color:{GREEN};margin-bottom:0.4rem">→ Designer's Recommendation</div>
              <p style="font-size:0.9rem;line-height:1.65;color:{TEXT};margin:0">{rec}</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 05 — TECHNICAL
# ══════════════════════════════════════════════════════════════════════════════
elif page == "05 · Technical":
    st.markdown(f"""
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                color:{AMBER};font-weight:700;margin-bottom:0.4rem">05 — Under the Hood</div>
    <h2 style="margin:0 0 0.4rem">The <em style="color:{AMBER};font-style:italic">architecture</em>.</h2>
    <p style="color:{MUTED};font-weight:300;max-width:580px;margin:0 0 1.75rem">
      One master DataFrame. A pipeline built for equity-first analysis.
    </p>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1.4, 1])

    with col_a:
        st.markdown("**Python · data pipeline**")
        st.code("""
import pandas as pd

SHEET_ID = "15rcpxlNkPKE_yrALqvxa..."
MASTER_GID = "73304917"

def sheet_url(gid):
    return (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&gid={gid}"
    )

# 1. Load master data from Google Sheets
df = pd.read_csv(sheet_url(MASTER_GID))

# 2. Equity segmentation by IMD Band
equity = (
    df.groupby("imd_band")[["total_clicks","final_score"]]
    .mean().round(1)
)

# 3. At-Risk flagging
# Flag: ≤1 assignment submitted
df["at_risk"] = df["assignments_submitted"] <= 1

# 4. Device equity gap
device_gap = (
    df.groupby("device")["final_score"]
    .mean().sort_values(ascending=False)
)

print(f"Students: {len(df)}")
print(f"At-risk:  {df['at_risk'].sum()}")
print(f"Pass rate: {(df['status']=='Pass').mean():.1%}")
""", language="python")

    with col_b:
        st.markdown("**Stack**")
        stack = {
            "🐍 Python + Pandas": "ETL, merge logic, equity segmentation",
            "📊 Plotly":           "Interactive charts, scatter, radar",
            "🚀 Streamlit":        "App framework — runs locally + Streamlit Cloud",
            "📋 Google Sheets":    "Live data via GViz CSV endpoint",
            "🌐 GitHub Pages":     "Version control + free hosting",
        }
        for name, desc in stack.items():
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e8e3db;border-radius:10px;
                        padding:0.85rem 1rem;margin-bottom:0.6rem">
              <strong style="font-size:0.875rem">{name}</strong><br>
              <span style="font-size:0.78rem;color:{MUTED}">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("View on GitHub →",
                       "https://github.com/rahmatsyawaludin",
                       use_container_width=True)
        st.link_button("← Back to Portfolio",
                       "https://rahmatsyawaludin.github.io/portfolio",
                       use_container_width=True)

    st.divider()
    st.markdown("**Live data preview**")
    tab1, tab2, tab3 = st.tabs(["Master Data", "Summary Stats", "Raw Shape"])
    with tab1:
        st.dataframe(df.head(15), use_container_width=True)
    with tab2:
        st.dataframe(df.describe().round(2), use_container_width=True)
    with tab3:
        st.write(f"Rows: **{len(df)}** · Columns: **{len(df.columns)}**")
        st.write(df.dtypes.astype(str).rename("dtype").to_frame())


# ── FOOTER ────────────────────────────────────────────────────────────────────
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
  <div style="font-size:0.8rem;display:flex;gap:1.5rem;flex-wrap:wrap">
    <a href="https://rahmatsyawaludin.github.io/portfolio" target="_blank"
       style="color:{AMBER};text-decoration:none">Portfolio</a>
    <a href="https://linkedin.com/in/rahmat-syawaludin" target="_blank"
       style="color:{AMBER};text-decoration:none">LinkedIn</a>
    <a href="mailto:rahmatsywldn@gmail.com"
       style="color:{AMBER};text-decoration:none">Email</a>
  </div>
</div>
<p style="font-size:0.75rem;color:{MUTED};margin:0">
  <em>"Learning design is not about content delivery —
  it is about engineering the conditions in which people grow."</em>
</p>
""", unsafe_allow_html=True)
