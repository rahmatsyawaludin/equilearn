# EquiLearn Analytics — Streamlit Dashboard

> *Transforming raw student clickstreams into instructional interventions to close equity gaps.*

**Live App →** *(add your Streamlit Cloud URL here after deployment)*  
**Portfolio →** [rahmatsyawaludin.github.io/portfolio](https://rahmatsyawaludin.github.io/portfolio)  
**Author →** Rahmat Syawaludin · MEd Digital Learning · Monash University · LPDP Scholar

---

## Overview

EquiLearn is a decision-support dashboard for Instructional Designers and Educational Leaders. It analyses 50 students across Indonesia — disaggregated by deprivation index (IMD Band), region, device type, and prior education — to surface equity gaps and actionable instructional interventions.

---

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/rahmatsyawaludin/equilearn.git
cd equilearn

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Deploy to Streamlit Cloud (Free, ~60 seconds)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account → select this repo
4. Set **Main file path** → `app.py`
5. Click **Deploy**

---

## Data Source

Live data is fetched at runtime from Google Sheets via the GViz CSV endpoint.  
If Sheets is unavailable, the app falls back to embedded sample data automatically.

| Tab | GID | Columns |
|-----|-----|---------|
| Master_Data | `73304917` | `student_id`, `region`, `imd_band`, `device`, `prior_education`, `total_clicks`, `avg_time_per_session`, `assignments_submitted`, `final_score`, `status` |

---

## Dashboard Pages

| Page | What it shows |
|------|---------------|
| 01 · Equity Overview | IMD band distribution, pass rate by band, region map |
| 02 · Engagement Analysis | Clicks vs score, assignment submission by outcome, at-risk flagging |
| 03 · Device & Access | Device type breakdown, mobile users by deprivation band, prior education vs score |
| 04 · Interventions | 6 data finding → designer recommendation pairs |
| 05 · Technical | Pipeline code, stack, live data preview |

---

## Stack

| Layer | Tool |
|-------|------|
| App framework | Streamlit |
| Data processing | Python · Pandas · NumPy |
| Visualisation | Plotly |
| Data source | Google Sheets (GViz CSV API) |
| Hosting | Streamlit Cloud + GitHub |

---

## Theoretical Framework

| Theory | Application |
|--------|-------------|
| **Equity-First Design** | All metrics disaggregated by IMD Band before reporting aggregates |
| **Cognitive Load Theory** (Sweller, 1988) | Assignment drop-offs interpreted as extraneous load signals |
| **Universal Design for Learning** (CAST, 2018) | Device equity gap → default mobile-first content design |
| **Social Learning Theory** (Vygotsky, 1978) | Engagement patterns as design outcomes, not learner traits |
| **ADDIE / SAM** | All interventions framed within industry-standard ID practice |

---

## Connect

- 🌐 [rahmatsyawaludin.github.io/portfolio](https://rahmatsyawaludin.github.io/portfolio)
- 💼 [linkedin.com/in/rahmat-syawaludin](https://linkedin.com/in/rahmat-syawaludin)
- ✉ rahmatsywldn@gmail.com

---

*"Learning design is not about content delivery — it is about engineering the conditions in which people grow."*
