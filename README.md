# EquiLearn: Learning Analytics & Strategy Dashboard

> *Transforming raw student clickstreams into instructional interventions to close equity gaps.*

**Live Demo →** [rahmatsyawaludin.github.io/equilearn](https://rahmatsyawaludin.github.io/equilearn)  
**Portfolio →** [rahmatsyawaludin.github.io/portfolio](https://rahmatsyawaludin.github.io/portfolio)  
**Author →** Rahmat Syawaludin · MEd Digital Learning, Monash University · LPDP Scholar

---

## Overview

EquiLearn is a decision-support dashboard for Instructional Designers and Educational Leaders. It analyses student interaction data from a virtual learning environment (VLE) to surface equity gaps, behavioural friction points, and actionable design interventions.

This project was built as a portfolio piece demonstrating the intersection of **learning analytics**, **instructional design theory**, and **data-informed curriculum strategy** — grounded in the equity-first principles developed during my Master of Education (Digital Learning) at Monash University.

**Translated 32,593 student records and 100,000+ LMS interactions into instructional design interventions targeting equity gaps in digital learning environments.**

---

## The Problem This Solves

Most learning analytics dashboards answer *what happened*. EquiLearn answers *what should an instructional designer do about it*.

Raw engagement data is abundant in modern LMS platforms. What's scarce is the pedagogical translation layer — the step that connects a drop in Week 5 clicks to a specific, theoretically grounded design intervention. This dashboard provides that layer.

---

## Dataset

**Source:** Open University Learning Analytics Dataset (OULAD)  
**Institution:** The Open University, UK  
**Scale:** 32,593 students · 7 modules · 40-week course cycles  
**License:** CC BY 4.0 · [UCI ML Repository](https://archive.ics.uci.edu/dataset/349/open+university+learning+analytics+dataset)

### Files Used

| File | Description | Key Fields |
|------|-------------|------------|
| `studentInfo.csv` | Demographics & outcomes | `imd_band`, `region`, `highest_education`, `disability`, `final_result` |
| `studentVle.csv` | Clickstream data | `id_student`, `date`, `sum_click`, `activity_type` |
| `studentAssessment.csv` | Assessment scores | `id_student`, `score`, `date_submitted` |

### Key Variable: IMD Band

The **Index of Multiple Deprivation (IMD)** is the UK government's official measure of relative deprivation across small geographic areas. It combines income, employment, education, health, crime, housing, and living environment into a single ranked score.

In this project, IMD Band is the primary equity lens — it allows us to ask not just *how* students engage, but *who* is being left behind and *why* structural factors outside the LMS contribute to learning gaps.

---

## Analytical Framework

### Three Core Insights

**1. The Engagement Gap**  
Comparing total click volume between students in the highest deprivation bands (0–30%) versus the lowest (70–100%). A persistent gap here signals that the LMS design itself may be creating friction for under-resourced learners — not a motivation deficit.

**2. The Drop-off Week**  
Identifying the week with the sharpest decline in engagement. In this dataset, Week 5 consistently emerges as the critical friction point — directly preceding the first major summative assessment. This is not coincidental: assessment anxiety, unclear expectations, and cognitive overload converge here.

**3. At-Risk Flagging**  
A student is flagged "At Risk" when they have recorded zero LMS activity for 7 or more consecutive days. This heuristic is intentionally conservative — early flagging enables early intervention before withdrawal becomes the path of least resistance.

---

## Theoretical Grounding

This dashboard is not a data science project wearing an education costume. Every metric and intervention is grounded in established instructional design and learning theory.

### Cognitive Load Theory *(Sweller, 1988)*
The Week 5 friction point is interpreted through the lens of extraneous cognitive load — the burden imposed by poor instructional design rather than the inherent complexity of content. Intervention: simplify navigation, chunk content, remove redundant elements before the first assessment window.

### Universal Design for Learning *(CAST, 2018)*
The disability engagement gap signals that UDL principles are not being applied at the material level. UDL requires multiple means of representation, action, and engagement as defaults — not accommodations requested after enrolment.

### Equity-First Design
Borrowing from community-based design practice: design for the learner with the fewest resources first, then scale upward. An LMS that works beautifully on a MacBook but fails on a low-spec Android in a low-bandwidth environment is not equitable — it is designed for one type of learner and tolerated by others.

### Social Learning Theory *(Vygotsky, 1978)*
High-achievers consistently over-index on Peer Forum engagement. This is not a personality trait — it is a design outcome. Forums that are scaffolded, structured, and made visible as core activities (not optional extras) shift social learning from accidental to intentional.

### ADDIE & SAM Frameworks
Interventions are framed within the ADDIE (Analyse, Design, Develop, Implement, Evaluate) and SAM (Successive Approximation Model) frameworks — reflecting industry-standard instructional design practice and allowing recommendations to be directly actionable by L&D teams.

---

## Dashboard Structure

```
Section 01 — Equity Overview
  └── IMD Band distribution
  └── Pass rate by deprivation band
  └── Key metric cards

Section 02 — Behavioural Analysis
  └── Weekly engagement line chart (40 weeks)
  └── Week 5 friction point annotation
  └── Interactive filters: education level, outcome
  └── Disability engagement breakdown
  └── At-risk student heatmap

Section 03 — Content-Type Analysis
  └── Engagement by material type (Video, Quiz, Forum, PDF)
  └── High Achievers vs At-Risk radar comparison

Section 04 — Instructional Interventions
  └── Six data-finding → designer recommendation pairs
  └── Framework tags per intervention

Section 05 — Technical Architecture
  └── Python pipeline code preview
  └── Stack documentation
```

---

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Data Source | Google Sheets (GViz CSV API) | Live, editable data — no backend required |
| Visualisation | Chart.js v4 | Bar, line, doughnut, radar charts |
| Frontend | Vanilla HTML / CSS / JS | Zero build step, GitHub Pages compatible |
| Typography | Syne + DM Sans (Google Fonts) | Display + body pairing |
| Hosting | GitHub Pages | Static, free, always live |

### Why not Streamlit?

Streamlit requires a running Python server, which adds hosting complexity and cost for a portfolio piece. A static HTML/JS architecture hosted on GitHub Pages is zero-maintenance, loads instantly, and is directly portable — the same decision made for my [PM Dashboard](https://rahmatsyawaludin.github.io/portfolio) portfolio project.

---

## Data Architecture

```python
# EquiLearn — Master Data Pipeline
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

print(f"Master DF: {df.shape[0]:,} rows")
print(f"At-risk students: {df['at_risk'].sum():,}")
```

---

## Using Your Own Data

The dashboard loads data from Google Sheets at runtime. To connect your own dataset:

1. Create a Google Sheet with these tabs and column headers:

**Demographics tab**
```
id_student | region | imd_band | highest_education | disability | final_result
```

**Engagement tab**
```
id_student | week | sum_click | content_type
```

**Outcomes tab**
```
id_student | assessment_score | submission_week
```

2. Set sharing to **"Anyone with the link can view"**

3. In `data.js`, replace `SHEET_ID` and the GID values in the `TABS` object with your own

---

## Project Context

This project sits at the intersection of two threads in my professional practice:

**The analytics thread** — During my MEd at Monash, the unit *Digital Data in Education* (EDF5771) introduced me to learning analytics as a design discipline, not just a reporting function. The question I kept returning to was: what does this data actually ask of a designer?

**The equity thread** — My fieldwork in Pulau-Pulau Babar, Maluku Barat Daya (the Babar Kalesang project) made equity-first design personal. Designing for 300–500 students with no internet, shared devices, and under-resourced teachers taught me that the gap between data and intervention is where instructional designers earn their role.

EquiLearn is an attempt to make that translation explicit and replicable.

---

## Connect

**Rahmat Syawaludin**  
Instructional Designer · Learning Experience Designer · Jakarta, Indonesia  
MEd Digital Learning · Monash University · LPDP Scholar

- 🌐 Portfolio: [rahmatsyawaludin.github.io/portfolio](https://rahmatsyawaludin.github.io/portfolio)
- 💼 LinkedIn: [linkedin.com/in/rahmat-syawaludin](https://linkedin.com/in/rahmat-syawaludin)
- ✉ Email: [rahmatsywldn@gmail.com](mailto:rahmatsywldn@gmail.com)

---

*"Learning design is not about content delivery — it is about engineering the conditions in which people grow."*
