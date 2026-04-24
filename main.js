// EquiLearn Analytics — Main Controller
// Rahmat Syawaludin · MEd Digital Learning · Monash University

// ---- INTERVENTIONS DATA ----
const INTERVENTIONS = [
  {
    finding: "25% of students stopped interacting after the first month — concentrated in high-deprivation bands (0–30%).",
    intervention: "Implement a proactive nudge system: automated low-bandwidth SMS reminders for students who haven't synced in 5 days. Prioritise offline-first learners using mobile as primary device.",
    frameworks: ["ADDIE", "Equity-First Design", "UDL"],
    severity: "high"
  },
  {
    finding: "Sharp engagement drop at Week 5 — coinciding with the first major assessment. At-risk students are 3× more likely to withdraw at this point.",
    intervention: "Redesign the Week 4 scaffold: add a low-stakes 'practice checkpoint' one week prior. Reduce cognitive load by simplifying navigation and chunking content into micro-modules.",
    frameworks: ["SAM Iteration", "Cognitive Load Theory", "Formative Design"],
    severity: "high"
  },
  {
    finding: "PDF resources show the lowest engagement from mobile users — likely due to file size and rendering on low-spec devices.",
    intervention: "Audit all PDF resources for mobile responsiveness. Convert high-traffic PDFs to HTML pages or compressed video summaries. Apply LMS Optimisation principles.",
    frameworks: ["LMS Optimisation", "Offline-First", "Accessibility"],
    severity: "medium"
  },
  {
    finding: "High-achievers spend 4× more time in Peer Forums and use Quiz resources 2.3× more frequently than at-risk peers.",
    intervention: "Make Peer Forum participation a visible, scaffolded activity — not optional. Introduce structured peer-response prompts in Weeks 2–4 to normalise social learning before the friction point.",
    frameworks: ["Social Learning Theory", "Vygotsky ZPD", "Community of Practice"],
    severity: "medium"
  },
  {
    finding: "Students with declared disabilities show 30% lower overall click volume despite equal enrolment rates.",
    intervention: "Conduct a targeted accessibility audit of all Week 1–3 materials. Implement alternative format options (audio, transcript, simplified layout) as default — not as add-ons.",
    frameworks: ["Universal Design for Learning", "Inclusive Design", "Accessibility"],
    severity: "high"
  },
  {
    finding: "Students in lower education bands (Lower Than A Level) disengage 2 weeks earlier than HE-qualified peers.",
    intervention: "Design a differentiated onboarding module for students with lower prior qualifications. Use backward design to scaffold foundational literacy into the first two weeks without condescension.",
    frameworks: ["Backward Design", "Differentiated Instruction", "Needs Analysis"],
    severity: "medium"
  }
];

// ---- SEVERITY COLOURS ----
const SEV = {
  high:   { finding: "#c84a4a", intervention: "#4ac87a" },
  medium: { finding: "#c8954a", intervention: "#4a8fc8" },
};

// ---- RENDER INTERVENTIONS ----
function renderInterventions() {
  const grid = document.getElementById("interventionGrid");
  grid.innerHTML = INTERVENTIONS.map((item, i) => `
    <div class="intervention-card" style="animation-delay:${i * 0.08}s">
      <div>
        <div class="int-label int-data" style="color:${SEV[item.severity].finding}">
          ⚠ Data Finding
        </div>
        <p class="int-text">${item.finding}</p>
        <div class="int-framework">
          ${item.frameworks.map(f => `<span class="int-tag">${f}</span>`).join("")}
        </div>
      </div>
      <div>
        <div class="int-label int-action" style="color:${SEV[item.severity].intervention}">
          → Designer's Recommendation
        </div>
        <p class="int-text">${item.intervention}</p>
      </div>
    </div>
  `).join("");
}

// ---- ANIMATE COUNTER ----
function animateCounter(el, target, duration = 1800) {
  const start = performance.now();
  const isLarge = target > 1000;
  function update(now) {
    const progress = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(ease * target);
    el.textContent = isLarge ? current.toLocaleString() : current;
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

function runCounters() {
  document.querySelectorAll(".stat-num[data-target]").forEach(el => {
    animateCounter(el, parseInt(el.dataset.target));
  });
}

// ---- POPULATE METRIC CARDS ----
function populateMetrics(demographics, engagement) {
  const total = demographics.length;
  const passed = demographics.filter(r => r.final_result === "Pass" || r.final_result === "Distinction").length;
  const passRate = total > 0 ? Math.round((passed / total) * 100) : 0;

  const highDep = demographics.filter(r => {
    const b = r.imd_band;
    return b === "0-10%" || b === "10-20%" || b === "20-30%";
  }).length;

  const highDepPct = total > 0 ? Math.round((highDep / total) * 100) : 0;

  // Avg clicks: high dep vs low dep
  const depMap = {};
  demographics.forEach(r => { depMap[r.id_student] = r.imd_band; });

  let highClicks = 0, highCount = 0, lowClicks = 0, lowCount = 0;
  engagement.forEach(r => {
    const b = depMap[r.id_student];
    const c = parseInt(r.sum_click) || 0;
    if (b === "0-10%" || b === "10-20%" || b === "20-30%") { highClicks += c; highCount++; }
    if (b === "80-90%" || b === "90-100%") { lowClicks += c; lowCount++; }
  });

  const avgHigh = highCount > 0 ? highClicks / highCount : 0;
  const avgLow  = lowCount  > 0 ? lowClicks  / lowCount  : 0;
  const gap = avgLow > 0 ? Math.round(((avgLow - avgHigh) / avgLow) * 100) : 15;

  document.getElementById("m-total").textContent    = total.toLocaleString();
  document.getElementById("m-passrate").textContent = passRate + "%";
  document.getElementById("m-highdep").textContent  = highDepPct + "%";
  document.getElementById("m-gap").textContent      = gap + "%";
}

// ---- THEME TOGGLE ----
function initTheme() {
  const toggle = document.getElementById("themeToggle");
  const body   = document.body;

  const saved = localStorage.getItem("equilearn-theme") || "dark";
  body.className = saved;

  toggle.addEventListener("click", () => {
    body.className = body.className === "dark" ? "light" : "dark";
    localStorage.setItem("equilearn-theme", body.className);
  });
}

// ---- FILTER HANDLERS ----
function initFilters(engagement) {
  const eduFilter     = document.getElementById("eduFilter");
  const outcomeFilter = document.getElementById("outcomeFilter");

  function applyFilters() {
    const edu     = eduFilter.value;
    const outcome = outcomeFilter.value;
    const filtered = engagement.filter(r => {
      const eduOk     = edu === "all"     || r.highest_education === edu;
      const outOk     = outcome === "all" || r.final_result === outcome;
      return eduOk && outOk;
    });
    renderEngagementChart(weeklyClicks(filtered));
  }

  eduFilter.addEventListener("change", applyFilters);
  outcomeFilter.addEventListener("change", applyFilters);
}

// ---- MERGE DATASETS ----
function mergeData(demographics, engagement) {
  // Attach demographic fields to each engagement row
  const demoMap = {};
  demographics.forEach(r => { demoMap[r.id_student] = r; });
  return engagement.map(r => ({
    ...r,
    ...(demoMap[r.id_student] || {})
  }));
}

// ---- MAIN INIT ----
async function init() {
  initTheme();
  renderInterventions();

  let data;

  try {
    data = await loadAllData();
    // If sheets returned empty / headers only
    if (!data.demographics || data.demographics.length < 2) throw new Error("No data");
  } catch (e) {
    console.warn("Google Sheets unavailable — using sample data.", e);
    data = SAMPLE_DATA;
  }

  const { demographics, engagement, outcomes } = data;
  const merged = mergeData(demographics, engagement);

  // Hide loading
  const loader = document.getElementById("loadingBar");
  loader.classList.add("hidden");
  setTimeout(() => loader.remove(), 600);

  // Run counters
  runCounters();

  // Metrics
  populateMetrics(demographics, engagement);

  // Charts
  renderIMDChart(aggregateByIMD(demographics));
  renderPassRateChart(passRateByIMD(demographics));
  renderEngagementChart(weeklyClicks(merged));
  renderDisabilityChart(demographics, engagement);
  renderAtRiskChart(demographics, engagement);
  renderContentTypeChart(engagement);
  renderAchieverChart(demographics, engagement, outcomes);

  // Filters (use merged so edu/outcome fields are on engagement rows)
  initFilters(merged);
}

// ---- SCROLL ANIMATION ----
function initScrollReveal() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll(".section, .metric-card, .chart-box, .intervention-card").forEach(el => {
    el.style.opacity = "0";
    el.style.transform = "translateY(24px)";
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    observer.observe(el);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  init();
  initScrollReveal();
});
