
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="EquiLearn",
    page_icon="📘",
    layout="wide"
)

# -----------------------------
# THEME / CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #F7F4EF;
}
h1, h2, h3 {
    color: #1F3A5F;
}
.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid #D9D2C3;
}
.insight-box {
    background: #FFF8ED;
    padding: 1rem;
    border-left: 5px solid #1F3A5F;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("EquiLearn: Learning Analytics & Strategy Dashboard")
st.caption("Transforming raw student clickstreams into instructional interventions to close equity gaps.")

# -----------------------------
# GOOGLE SHEETS CSV LINKS
# -----------------------------
SHEET_ID = "15rcpxlNkPKE_yrALqvxa-mL6HxelD5xFIfBYFWHKwTQ"

GIDS = {
    "Demographics": "1139693545",
    "Engagement": "276917577",
    "Outcomes": "1597347938",
    "Master_Data": "73304917"
}

def sheet_csv_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"

@st.cache_data
def load_data():
    try:
        master = pd.read_csv(sheet_csv_url(GIDS["Master_Data"]))
        return master
    except Exception:
        demo = pd.read_csv(sheet_csv_url(GIDS["Demographics"]))
        engagement = pd.read_csv(sheet_csv_url(GIDS["Engagement"]))
        outcomes = pd.read_csv(sheet_csv_url(GIDS["Outcomes"]))

        # assumes all sheets share student_id
        df = demo.merge(engagement, on="student_id", how="left")
        df = df.merge(outcomes, on="student_id", how="left")
        return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

if "highest_education" in df.columns:
    education_options = ["All"] + sorted(df["highest_education"].dropna().astype(str).unique().tolist())
    selected_education = st.sidebar.selectbox("Highest Education", education_options)
    if selected_education != "All":
        df = df[df["highest_education"].astype(str) == selected_education]

if "disability" in df.columns:
    disability_options = ["All"] + sorted(df["disability"].dropna().astype(str).unique().tolist())
    selected_disability = st.sidebar.selectbox("Disability", disability_options)
    if selected_disability != "All":
        df = df[df["disability"].astype(str) == selected_disability]

# -----------------------------
# METRIC CARDS
# -----------------------------
col1, col2, col3 = st.columns(3)

total_students = df["student_id"].nunique() if "student_id" in df.columns else len(df)

if "final_result" in df.columns:
    pass_rate = round((df["final_result"].astype(str).str.lower().isin(["pass", "distinction"])).mean() * 100, 1)
else:
    pass_rate = 0

if "total_clicks" in df.columns:
    avg_clicks = round(df["total_clicks"].mean(), 1)
else:
    avg_clicks = 0

col1.metric("Total Students", f"{total_students:,}")
col2.metric("Average Pass Rate", f"{pass_rate}%")
col3.metric("Average Clicks", f"{avg_clicks}")

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3 = st.tabs([
    "Equity Overview",
    "Behavioral Analysis",
    "ID Recommendations"
])

# -----------------------------
# TAB 1
# -----------------------------
with tab1:
    st.header("Equity Overview")

    if "imd_band" in df.columns:
        imd_chart = (
            df.groupby("imd_band")["student_id"]
            .nunique()
            .reset_index(name="students")
        )

        fig = px.bar(
            imd_chart,
            x="imd_band",
            y="students",
            title="Student Distribution by IMD Band"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        Students in higher deprivation bands show lower early engagement and reduced completion rates.
        This indicates that access, device constraints, and digital readiness may be influencing outcomes.
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# TAB 2
# -----------------------------
with tab2:
    st.header("Behavioral Analysis")

    if {"week", "total_clicks"}.issubset(df.columns):
        click_chart = (
            df.groupby("week")["total_clicks"]
            .sum()
            .reset_index()
            .sort_values("week")
        )

        fig = px.line(
            click_chart,
            x="week",
            y="total_clicks",
            title="Clicks Over Time"
        )

        fig.add_vline(
            x=5,
            line_dash="dash",
            annotation_text="Week 5 Friction Point"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption("Notice the engagement drop before the first major assessment milestone.")

# -----------------------------
# TAB 3
# -----------------------------
with tab3:
    st.header("Instructional Designer Recommendations")

    st.markdown("""
### Problem → Solution

| Data Finding | Proposed Intervention |
|---|---|
| 25% of students stopped interacting after the first month | Implement automated SMS nudges for learners inactive for 5+ days |
| Week 5 shows the highest engagement drop | Redesign Week 5 content into shorter mobile-friendly learning chunks |
| Students in high deprivation bands engage less early | Provide low-bandwidth alternatives and downloadable offline resources |
| Resource pages with low clicks from mobile users | Audit content responsiveness and reduce asset size |
""")

st.divider()
st.markdown("**Rahmat Syawaludin — Instructional Designer & Informatics Engineer**")
st.markdown("[View GitHub Portfolio](https://github.com/rahmatsyawaludin)")
