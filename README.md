# EquiLearn Analytics

> **Turning raw student clickstream data into equity-first instructional interventions — because data without action is just noise.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20EquiLearn-4A90D9?style=for-the-badge)](https://rahmatsyawaludin-equilearn.streamlit.app/)
[![Portfolio](https://img.shields.io/badge/Back%20to%20Portfolio-grey?style=for-the-badge)](https://rahmatsyawaludin.github.io/portfolio/)

---

## The Problem

In Indonesia, a student in Jakarta and a student in Maluku can enrol in the same digital course — but they are not learning under the same conditions. One has a desktop and broadband. The other has a mobile phone on a low-bandwidth connection in a high-deprivation region.

Most LMS analytics dashboards treat these two students identically. They count completion rates. They report average scores. They never ask *why* the gap exists — or what a designer should do about it.

EquiLearn was built to ask that question, and answer it.

---

## The Solution

EquiLearn is a 5-page interactive analytics platform that processes raw student engagement data — clickstreams, device types, assignment submissions, regional deprivation indices — and transforms it into **actionable instructional interventions** grounded in equity principles and learning design theory.

It doesn't just visualise data. It reads the data, identifies the structural inequities, and tells you — as a designer — exactly what to do next.

---

## The Dataset

50 students across Indonesia, tracked across:

| Variable | Description |
|----------|-------------|
| `imd_band` | Index of Multiple Deprivation — 5 bands from 0–10% (high deprivation) to 90–100% (low deprivation) |
| `region` | Geographic region — including Maluku, West Papua, Jakarta, Sumatra |
| `device` | Device type — Desktop, Mobile (Low-Bandwidth), Tablet |
| `total_clicks` | Total LMS interactions across the course |
| `final_score` | Final assessment result |
| `assignment_submissions` | Number of assignments submitted |
| `outcome` | Pass, Withdrawn, or In Progress |

Data is served live from **Google Sheets** via the CSV export API — no database required.

---

## The 5 Pages

### 01 · Equity Overview
Maps the full cohort by deprivation index and pass rate. The headline finding: students in the highest deprivation band (IMD 0–10%) pass at a significantly lower rate than the lowest deprivation band — and mobile device usage is concentrated in that same cohort.

### 02 · Engagement Analysis
Disaggregates LMS clicks, session time, and assignment submission by outcome and deprivation band. Key signal: high-passing students average **42 total clicks**; withdrawn students average only **22** — a 2× engagement gap that appears within the first two weeks.

### 03 · Device & Access Analysis
Treats device type as a structural equity variable, not a learner preference. Desktop users outperform mobile users by an average of **12 score points**. Mobile (Low-Bandwidth) users are disproportionately from high-deprivation areas in Maluku and West Papua — confirming that the performance gap is a hardware access gap, not a learning ability gap.

### 04 · Instructional Interventions
This is the "so what?" page. Every data finding maps directly to a designer's recommended response, tagged with the relevant instructional framework:

| Data Finding | Designer's Recommendation | Frameworks |
|---|---|---|
| High-deprivation students use mobile significantly more — yet LMS content isn't optimised for low-bandwidth | Audit all materials for mobile responsiveness. Convert PDFs to lightweight HTML. Add a Low-Bandwidth Mode toggle. | Equity-First Design · Offline-First · UDL |
| Withdrawn students average only 1 assignment submission vs. 3.5 for passing students | Automated flag: no Assignment 1 by Week 3 → trigger personal outreach via SMS/WhatsApp | ADDIE · SAM Iteration · Formative Design |
| Maluku and West Papua students show lower scores and higher withdrawal rates | Design a region-aware onboarding module with culturally grounded context from Eastern Indonesia | Needs Analysis · Culturally Responsive Design · Backward Design |
| 2× click gap between passing and withdrawn students appears in first two weeks | Week 2 threshold: fewer than 15 clicks → automated check-in prompt | Cognitive Load Theory · SAM · Formative Design |
| Desktop users outscore mobile users by 12 points | Partner with regional institutions for device lending. Design Mobile-First content variants as the default, not an add-on. | UDL · Equity-First Design · Accessibility |

### 05 · Technical
The architecture page. Shows the full data pipeline — from Google Sheets master tab → Pandas ETL → equity segmentation → Streamlit visualisation — with live code samples and the complete tech stack.

---

## Key Features

- **📊 Equity-First Segmentation** — Every chart is disaggregated by IMD band, region, and device — not averaged away.
- **🔍 Interactive Filters** — Filter by device type and deprivation band across all pages via sidebar controls.
- **💡 Insight Cards** — Inline `insight` and `insight-warn` callouts surface the equity interpretation directly next to the chart — no separate report needed.
- **🔴 Prioritised Interventions** — High and Medium priority intervention cards, each mapping a data finding to a specific designer action and tagging the relevant instructional frameworks.
- **📡 Live Data via Google Sheets** — Master dataset served from Google Sheets CSV API with automatic fallback to embedded data if the sheet is unavailable.
- **🛠️ Under the Hood Page** — Full pipeline walkthrough with live code, for anyone who wants to fork and adapt it.

---

## Data Ethics

> *"Data is not just a number — it can be used to take action, while still maintaining data ethics."*

Every design decision in EquiLearn reflects this principle:

- **No individual student is identifiable** — all analysis is at cohort and band level
- **Deprivation is treated as a structural variable**, not a personal attribute — the design never blames the learner
- **Interventions are framed as designer responsibilities**, not learner deficits — the system needs to change, not the student
- The platform was built during postgraduate study in **Digital Data in Education** at Monash University — grounded in research on responsible use of learning analytics

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Language | Python |
| Dashboard Framework | Streamlit |
| Data Processing | Pandas · NumPy |
| Visualisation | Plotly Express · Plotly Graph Objects |
| Data Source | Google Sheets (CSV export API — live feed) |
| Typography | Syne · DM Sans (via Google Fonts) |
| Hosting | Streamlit Cloud |

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/rahmatsyawaludin/equilearn.git

# Navigate into the project
cd equilearn

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

Or skip setup entirely and **[open the live dashboard](https://rahmatsyawaludin-equilearn.streamlit.app/)**.

---

## Part of a Bigger Story

| Project | What It Demonstrates |
|---------|---------------------|
| [EquiLearn](https://rahmatsyawaludin-equilearn.streamlit.app/) ← **you are here** | Data ethics · Equity analytics · Instructional design from evidence |
| [PM Dashboard](https://rahmatsyawaludin-pm-dashboard.streamlit.app/) | Strategy plan turned into live technical product |
| [EduPulse](https://rahmatsyawaludin.github.io/edupulse/) | Instructional design meets frontend product |
| [Human Firewall](https://rahmatsyawaludin.github.io/case-study-human-firewall/) | Full L&D lifecycle · Behaviour design · AR + Gamification |

---

## About the Author

**Rahmat Syawaludin** — Learning Designer · Instructional Designer · MEd Digital Learning, Monash University (LPDP Scholar)

📧 rahmatsywldn@gmail.com
🌐 [Portfolio](https://rahmatsyawaludin.github.io/portfolio/)
💼 [LinkedIn](https://linkedin.com/in/rahmat-syawaludin)
