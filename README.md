# EquiLearn Analytics — Streamlit Dashboard

> *Transforming raw student clickstreams into instructional interventions to close equity gaps.*

**Live App →** *(add your Streamlit Cloud URL here after deployment)*  
**Portfolio →** [rahmatsyawaludin.github.io/portfolio](https://rahmatsyawaludin.github.io/portfolio)  
**Author →** Rahmat Syawaludin · MEd Digital Learning · Monash University · LPDP Scholar

---

## Overview

EquiLearn is a decision-support dashboard for Instructional Designers and Educational Leaders. It analyses student interaction data from a virtual learning environment (VLE) to surface equity gaps, behavioural friction points, and actionable design interventions — grounded in instructional theory.

**Translated 32,593 student records and 100,000+ LMS interactions into instructional design interventions targeting equity gaps in digital learning environments.**

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

---

## Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy** — live in ~60 seconds

---

## Data Source

**Google Sheets (live)** — the app fetches directly from your Google Sheet at runtime via the GViz CSV endpoint. No data is stored in the repo.

| Tab | GID | Key Fields |
|-----|-----|------------|
| Demographics | `1139693545` | `id_student`, `imd_band`, `region`, `highest_education`, `disability`, `final_result` |
| Engagement | `276917577` | `id_student`, `week`, `sum_click`, `content_type` |
| Outcomes | `1597347938` | `id_student`, `assessment_score`, `submission_week` |

If Sheets is unavailable, the app automatically falls back to built-in sample data.

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

Every metric maps to an instructional design principle:

- **Equity-First Design** — IMD Band disaggregation surfaces who is being left behind
- **Cognitive Load Theory** *(Sweller, 1988)* — Week 5 drop-offs signal extraneous load, not motivation failure
- **Universal Design for Learning** *(CAST, 2018)* — disability engagement gaps require default accessibility, not add-on accommodations
- **Social Learning Theory** *(Vygotsky, 1978)* — Forum over-indexing by high-achievers is a design outcome, not a personality trait
- **ADDIE / SAM** — all interventions are framed within industry-standard instructional design frameworks

---

## Dashboard Structure

| Page | Content |
|------|---------|
| 01 · Equity Overview | IMD distribution, pass rate by band, engagement gap |
| 02 · Behavioural Analysis | Weekly clicks, Week 5 friction point, at-risk flagging |
| 03 · Content Analysis | Material type engagement, achiever vs at-risk radar |
| 04 · Interventions | 6 data finding → designer recommendation pairs |
| 05 · Technical | Pipeline code, stack, live data preview |

---

## Project Context

This project sits at the intersection of two threads in my professional practice.

**The analytics thread** — During my MEd at Monash, *Digital Data in Education* (EDF5771) introduced me to learning analytics as a design discipline. The question I kept returning to: what does this data actually ask of a designer?

**The equity thread** — My fieldwork in Pulau-Pulau Babar, Maluku Barat Daya (Babar Kalesang project) made equity-first design personal. Designing for 300–500 students with no internet, shared devices, and under-resourced teachers taught me that the gap between data and intervention is where instructional designers earn their role.

EquiLearn is an attempt to make that translation explicit and replicable.

---

## Connect

- 🌐 [rahmatsyawaludin.github.io/portfolio](https://rahmatsyawaludin.github.io/portfolio)
- 💼 [linkedin.com/in/rahmat-syawaludin](https://linkedin.com/in/rahmat-syawaludin)
- ✉ rahmatsywldn@gmail.com

---

*"Learning design is not about content delivery — it is about engineering the conditions in which people grow."*
