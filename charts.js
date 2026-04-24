// EquiLearn Analytics — Chart Engine
// Chart.js v4 · Rahmat Syawaludin

const PALETTE = {
  accent:  "#c8954a",
  accent2: "#4a8fc8",
  warn:    "#c84a4a",
  success: "#4ac87a",
  muted:   "#8a95a8",
  surface: "#1a2232",
  text:    "#e8eaf0",
};

// Resolve CSS var for current theme
function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function chartDefaults() {
  return {
    color: cssVar("--text-muted") || PALETTE.muted,
    borderColor: cssVar("--border") || "rgba(255,255,255,0.07)",
  };
}

// ---- IMD BAR CHART ----
function renderIMDChart(data) {
  const ctx = document.getElementById("imdChart").getContext("2d");
  const imdOrder = ["0-10%","10-20%","20-30%","30-40%","40-50%","50-60%","60-70%","70-80%","80-90%","90-100%"];
  const labels = imdOrder.filter(k => data[k] !== undefined);
  const values = labels.map(k => data[k] || 0);

  // Gradient colour: darker = higher deprivation
  const gradient = ctx.createLinearGradient(0, 0, ctx.canvas.width, 0);
  gradient.addColorStop(0, "#c84a4a");
  gradient.addColorStop(0.5, PALETTE.accent);
  gradient.addColorStop(1, PALETTE.success);

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: gradient,
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#1a2232",
          titleColor: "#e8eaf0",
          bodyColor: "#8a95a8",
          borderColor: "rgba(255,255,255,0.1)",
          borderWidth: 1,
          callbacks: {
            label: ctx => ` ${ctx.parsed.y} students`
          }
        }
      },
      scales: {
        x: {
          ticks: { color: PALETTE.muted, font: { size: 11 } },
          grid: { color: "rgba(255,255,255,0.04)" }
        },
        y: {
          ticks: { color: PALETTE.muted, font: { size: 11 } },
          grid: { color: "rgba(255,255,255,0.04)" }
        }
      }
    }
  });
}

// ---- PASS RATE DOUGHNUT ----
function renderPassRateChart(data) {
  const ctx = document.getElementById("passRateChart").getContext("2d");
  const imdOrder = ["0-10%","10-20%","20-30%","30-40%","40-50%","50-60%","60-70%","70-80%","80-90%","90-100%"];
  const labels = imdOrder.filter(k => data[k] !== undefined);
  const values = labels.map(k => data[k] || 0);

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Pass Rate %",
        data: values,
        backgroundColor: values.map(v =>
          v < 50 ? "rgba(200,74,74,0.7)" :
          v < 65 ? "rgba(200,149,74,0.7)" :
                   "rgba(74,200,122,0.7)"
        ),
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#1a2232",
          bodyColor: "#8a95a8",
          callbacks: { label: ctx => ` ${ctx.parsed.x}%` }
        }
      },
      scales: {
        x: {
          max: 100,
          ticks: { color: PALETTE.muted, font: { size: 10 }, callback: v => v + "%" },
          grid: { color: "rgba(255,255,255,0.04)" }
        },
        y: {
          ticks: { color: PALETTE.muted, font: { size: 10 } },
          grid: { display: false }
        }
      }
    }
  });
}

// ---- ENGAGEMENT LINE CHART ----
let engagementChartInstance = null;

function renderEngagementChart(weeklyData) {
  const ctx = document.getElementById("engagementChart").getContext("2d");
  const weeks = Array.from({ length: 40 }, (_, i) => i + 1);
  const values = weeks.map(w => weeklyData[w] || 0);

  if (engagementChartInstance) engagementChartInstance.destroy();

  const gradient = ctx.createLinearGradient(0, 0, 0, 300);
  gradient.addColorStop(0, "rgba(200,149,74,0.25)");
  gradient.addColorStop(1, "rgba(200,149,74,0)");

  engagementChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: weeks.map(w => `Wk ${w}`),
      datasets: [{
        label: "Total Clicks",
        data: values,
        borderColor: PALETTE.accent,
        backgroundColor: gradient,
        borderWidth: 2.5,
        pointRadius: weeks.map(w => w === 5 ? 7 : 2),
        pointBackgroundColor: weeks.map(w => w === 5 ? PALETTE.warn : PALETTE.accent),
        tension: 0.4,
        fill: true,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#1a2232",
          titleColor: "#e8eaf0",
          bodyColor: "#8a95a8",
          borderColor: "rgba(255,255,255,0.1)",
          borderWidth: 1,
        },
        annotation: {
          annotations: {
            frictionLine: {
              type: "line",
              xMin: 4, xMax: 4,
              borderColor: PALETTE.warn,
              borderWidth: 2,
              borderDash: [6, 3],
              label: {
                display: true,
                content: "⚠ Week 5",
                color: PALETTE.warn,
                backgroundColor: "rgba(200,74,74,0.15)",
                font: { size: 11, weight: "bold" },
                position: "start",
              }
            }
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: PALETTE.muted, font: { size: 10 },
            maxTicksLimit: 10,
          },
          grid: { color: "rgba(255,255,255,0.04)" }
        },
        y: {
          ticks: { color: PALETTE.muted, font: { size: 10 } },
          grid: { color: "rgba(255,255,255,0.04)" }
        }
      }
    }
  });
}

// ---- DISABILITY CHART ----
function renderDisabilityChart(demographics, engagement) {
  const ctx = document.getElementById("disabilityChart").getContext("2d");

  // Build lookup: student → disability
  const disMap = {};
  demographics.forEach(r => { disMap[r.id_student] = r.disability; });

  let yesClicks = 0, noClicks = 0;
  engagement.forEach(r => {
    const clicks = parseInt(r.sum_click) || 0;
    if (disMap[r.id_student] === "Y") yesClicks += clicks;
    else noClicks += clicks;
  });

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["No Disability", "Disability Declared"],
      datasets: [{
        data: [noClicks, yesClicks],
        backgroundColor: [PALETTE.accent2, PALETTE.warn],
        borderWidth: 0,
        hoverOffset: 6,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      cutout: "65%",
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: PALETTE.muted, font: { size: 11 }, padding: 16 }
        },
        tooltip: {
          backgroundColor: "#1a2232",
          bodyColor: "#8a95a8",
        }
      }
    }
  });
}

// ---- AT-RISK CHART ----
function renderAtRiskChart(demographics, engagement) {
  const ctx = document.getElementById("atRiskChart").getContext("2d");

  // Flag at-risk: last recorded week with 0 clicks
  const studentLastActive = {};
  engagement.forEach(r => {
    const w = parseInt(r.week) || 0;
    const c = parseInt(r.sum_click) || 0;
    if (c > 0) {
      studentLastActive[r.id_student] = Math.max(studentLastActive[r.id_student] || 0, w);
    }
  });

  // Count at-risk per week band
  const atRiskByWeek = { "Wk 1-5": 0, "Wk 6-10": 0, "Wk 11-20": 0, "Wk 21+": 0 };
  Object.values(studentLastActive).forEach(lastW => {
    if (lastW <= 5)       atRiskByWeek["Wk 1-5"]++;
    else if (lastW <= 10) atRiskByWeek["Wk 6-10"]++;
    else if (lastW <= 20) atRiskByWeek["Wk 11-20"]++;
    else                  atRiskByWeek["Wk 21+"]++;
  });

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: Object.keys(atRiskByWeek),
      datasets: [{
        label: "At-Risk Students",
        data: Object.values(atRiskByWeek),
        backgroundColor: ["rgba(200,74,74,0.8)", "rgba(200,74,74,0.6)", "rgba(200,149,74,0.5)", "rgba(74,200,122,0.5)"],
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#1a2232",
          bodyColor: "#8a95a8",
          callbacks: { label: ctx => ` ${ctx.parsed.y} students` }
        }
      },
      scales: {
        x: { ticks: { color: PALETTE.muted, font: { size: 11 } }, grid: { display: false } },
        y: { ticks: { color: PALETTE.muted, font: { size: 10 } }, grid: { color: "rgba(255,255,255,0.04)" } }
      }
    }
  });
}

// ---- CONTENT TYPE CHART ----
function renderContentTypeChart(engagement) {
  const ctx = document.getElementById("contentTypeChart").getContext("2d");
  const types = contentTypeEngagement(engagement);
  const sorted = Object.entries(types).sort((a, b) => b[1] - a[1]);
  const labels = sorted.map(e => e[0]);
  const values = sorted.map(e => e[1]);

  const colors = [PALETTE.accent2, PALETTE.accent, PALETTE.success, PALETTE.warn, PALETTE.muted];

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors.slice(0, labels.length),
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#1a2232",
          bodyColor: "#8a95a8",
          callbacks: { label: ctx => ` ${ctx.parsed.x.toLocaleString()} clicks` }
        }
      },
      scales: {
        x: {
          ticks: { color: PALETTE.muted, font: { size: 10 } },
          grid: { color: "rgba(255,255,255,0.04)" }
        },
        y: {
          ticks: { color: PALETTE.muted, font: { size: 12 } },
          grid: { display: false }
        }
      }
    }
  });
}

// ---- ACHIEVER vs AT-RISK CHART ----
function renderAchieverChart(demographics, engagement, outcomes) {
  const ctx = document.getElementById("achieverChart").getContext("2d");

  // Build pass map
  const passMap = {};
  demographics.forEach(r => { passMap[r.id_student] = r.final_result; });

  const highClicks  = { Video: 0, Quiz: 0, Forum: 0, PDF: 0, Other: 0 };
  const atRiskClicks = { Video: 0, Quiz: 0, Forum: 0, PDF: 0, Other: 0 };

  engagement.forEach(r => {
    const result = passMap[r.id_student];
    const type   = r.content_type || "Other";
    const key    = highClicks.hasOwnProperty(type) ? type : "Other";
    const clicks = parseInt(r.sum_click) || 0;
    if (result === "Pass" || result === "Distinction") highClicks[key] += clicks;
    else if (result === "Fail" || result === "Withdrawn") atRiskClicks[key] += clicks;
  });

  const labels = Object.keys(highClicks);

  new Chart(ctx, {
    type: "radar",
    data: {
      labels,
      datasets: [
        {
          label: "High Achievers",
          data: labels.map(k => highClicks[k]),
          borderColor: PALETTE.success,
          backgroundColor: "rgba(74,200,122,0.12)",
          borderWidth: 2,
          pointBackgroundColor: PALETTE.success,
        },
        {
          label: "At-Risk",
          data: labels.map(k => atRiskClicks[k]),
          borderColor: PALETTE.warn,
          backgroundColor: "rgba(200,74,74,0.12)",
          borderWidth: 2,
          pointBackgroundColor: PALETTE.warn,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: PALETTE.muted, font: { size: 11 }, padding: 12 }
        },
        tooltip: { backgroundColor: "#1a2232", bodyColor: "#8a95a8" }
      },
      scales: {
        r: {
          ticks: { color: PALETTE.muted, font: { size: 9 }, backdropColor: "transparent" },
          grid: { color: "rgba(255,255,255,0.08)" },
          pointLabels: { color: PALETTE.text, font: { size: 11 } }
        }
      }
    }
  });
}
