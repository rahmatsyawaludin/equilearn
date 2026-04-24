// EquiLearn Analytics — Data Layer
// Fetches from Google Sheets via GViz CSV endpoint
// Rahmat Syawaludin · rahmatsyawaludin.github.io/portfolio

const SHEET_ID = "15rcpxlNkPKE_yrALqvxa-mL6HxelD5xFIfBYFWHKwTQ";

const TABS = {
  demographics: "1139693545",
  engagement:   "276917577",
  outcomes:     "1597347938",
  master:       "73304917"
};

function sheetUrl(gid) {
  return `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&gid=${gid}`;
}

// Simple CSV parser
function parseCSV(text) {
  const lines = text.trim().split("\n");
  const headers = lines[0].split(",").map(h => h.replace(/"/g, "").trim());
  return lines.slice(1).map(line => {
    const vals = [];
    let current = "", inQuote = false;
    for (let ch of line) {
      if (ch === '"') { inQuote = !inQuote; }
      else if (ch === "," && !inQuote) { vals.push(current.trim()); current = ""; }
      else { current += ch; }
    }
    vals.push(current.trim());
    const obj = {};
    headers.forEach((h, i) => { obj[h] = vals[i] || ""; });
    return obj;
  });
}

async function fetchTab(gid) {
  const res = await fetch(sheetUrl(gid));
  const text = await res.text();
  return parseCSV(text);
}

// Main data loader
async function loadAllData() {
  const [demographics, engagement, outcomes, master] = await Promise.all([
    fetchTab(TABS.demographics),
    fetchTab(TABS.engagement),
    fetchTab(TABS.outcomes),
    fetchTab(TABS.master)
  ]);
  return { demographics, engagement, outcomes, master };
}

// ---- FALLBACK SAMPLE DATA (if Sheets unavailable) ----
const SAMPLE_DATA = {
  demographics: [
    { id_student:"1001", region:"London Region",       imd_band:"0-10%",  highest_education:"A Level or Equivalent",    disability:"N", final_result:"Pass"      },
    { id_student:"1002", region:"South Region",        imd_band:"10-20%", highest_education:"HE Qualification",         disability:"N", final_result:"Pass"      },
    { id_student:"1003", region:"Midlands Region",     imd_band:"20-30%", highest_education:"Lower Than A Level",       disability:"Y", final_result:"Fail"      },
    { id_student:"1004", region:"North Region",        imd_band:"30-40%", highest_education:"A Level or Equivalent",    disability:"N", final_result:"Pass"      },
    { id_student:"1005", region:"Wales",               imd_band:"40-50%", highest_education:"HE Qualification",         disability:"N", final_result:"Withdrawn" },
    { id_student:"1006", region:"Scotland",            imd_band:"50-60%", highest_education:"A Level or Equivalent",    disability:"N", final_result:"Pass"      },
    { id_student:"1007", region:"Ireland",             imd_band:"60-70%", highest_education:"Lower Than A Level",       disability:"Y", final_result:"Fail"      },
    { id_student:"1008", region:"East Anglian Region", imd_band:"70-80%", highest_education:"Post Graduate Qualification", disability:"N", final_result:"Pass"   },
    { id_student:"1009", region:"North Western Region",imd_band:"80-90%", highest_education:"HE Qualification",         disability:"N", final_result:"Pass"      },
    { id_student:"1010", region:"Yorkshire Region",    imd_band:"90-100%",highest_education:"A Level or Equivalent",    disability:"N", final_result:"Pass"      },
    { id_student:"1011", region:"London Region",       imd_band:"0-10%",  highest_education:"HE Qualification",         disability:"N", final_result:"Fail"      },
    { id_student:"1012", region:"South Region",        imd_band:"10-20%", highest_education:"A Level or Equivalent",    disability:"Y", final_result:"Pass"      },
    { id_student:"1013", region:"Midlands Region",     imd_band:"30-40%", highest_education:"Lower Than A Level",       disability:"N", final_result:"Withdrawn" },
    { id_student:"1014", region:"North Region",        imd_band:"0-10%",  highest_education:"A Level or Equivalent",    disability:"N", final_result:"Fail"      },
    { id_student:"1015", region:"Wales",               imd_band:"20-30%", highest_education:"HE Qualification",         disability:"N", final_result:"Pass"      },
  ],
  engagement: [
    { id_student:"1001", week:"1",  sum_click:"42",  content_type:"Video"  },
    { id_student:"1001", week:"2",  sum_click:"55",  content_type:"Quiz"   },
    { id_student:"1001", week:"3",  sum_click:"61",  content_type:"Forum"  },
    { id_student:"1001", week:"4",  sum_click:"70",  content_type:"PDF"    },
    { id_student:"1001", week:"5",  sum_click:"22",  content_type:"Video"  },
    { id_student:"1001", week:"6",  sum_click:"18",  content_type:"Quiz"   },
    { id_student:"1001", week:"7",  sum_click:"35",  content_type:"Forum"  },
    { id_student:"1001", week:"8",  sum_click:"48",  content_type:"PDF"    },
    { id_student:"1002", week:"1",  sum_click:"30",  content_type:"Video"  },
    { id_student:"1002", week:"2",  sum_click:"38",  content_type:"Quiz"   },
    { id_student:"1002", week:"3",  sum_click:"45",  content_type:"Forum"  },
    { id_student:"1002", week:"4",  sum_click:"52",  content_type:"PDF"    },
    { id_student:"1002", week:"5",  sum_click:"12",  content_type:"Video"  },
    { id_student:"1002", week:"6",  sum_click:"8",   content_type:"Quiz"   },
    { id_student:"1002", week:"7",  sum_click:"25",  content_type:"Forum"  },
    { id_student:"1003", week:"1",  sum_click:"18",  content_type:"PDF"    },
    { id_student:"1003", week:"2",  sum_click:"22",  content_type:"Video"  },
    { id_student:"1003", week:"3",  sum_click:"15",  content_type:"Quiz"   },
    { id_student:"1003", week:"4",  sum_click:"8",   content_type:"Forum"  },
    { id_student:"1003", week:"5",  sum_click:"3",   content_type:"PDF"    },
    { id_student:"1003", week:"6",  sum_click:"0",   content_type:"Video"  },
    { id_student:"1003", week:"7",  sum_click:"0",   content_type:"Quiz"   },
    { id_student:"1004", week:"1",  sum_click:"55",  content_type:"Forum"  },
    { id_student:"1004", week:"2",  sum_click:"62",  content_type:"Video"  },
    { id_student:"1004", week:"3",  sum_click:"71",  content_type:"Quiz"   },
    { id_student:"1004", week:"4",  sum_click:"80",  content_type:"PDF"    },
    { id_student:"1004", week:"5",  sum_click:"35",  content_type:"Forum"  },
    { id_student:"1004", week:"6",  sum_click:"45",  content_type:"Video"  },
    { id_student:"1004", week:"7",  sum_click:"55",  content_type:"Quiz"   },
    { id_student:"1004", week:"8",  sum_click:"65",  content_type:"Forum"  },
  ],
  outcomes: [
    { id_student:"1001", assessment_score:"72", submission_week:"6" },
    { id_student:"1002", assessment_score:"58", submission_week:"6" },
    { id_student:"1003", assessment_score:"31", submission_week:"6" },
    { id_student:"1004", assessment_score:"85", submission_week:"6" },
    { id_student:"1005", assessment_score:"0",  submission_week:"—" },
    { id_student:"1006", assessment_score:"78", submission_week:"6" },
    { id_student:"1007", assessment_score:"42", submission_week:"6" },
    { id_student:"1008", assessment_score:"91", submission_week:"6" },
    { id_student:"1009", assessment_score:"66", submission_week:"6" },
    { id_student:"1010", assessment_score:"74", submission_week:"6" },
  ]
};

// Aggregate helpers used by charts.js
function aggregateByIMD(demographics) {
  const bands = {};
  demographics.forEach(r => {
    const b = r.imd_band || r["imd_band"] || "Unknown";
    bands[b] = (bands[b] || 0) + 1;
  });
  return bands;
}

function passRateByIMD(demographics) {
  const totals = {}, passes = {};
  demographics.forEach(r => {
    const b = r.imd_band || "Unknown";
    totals[b] = (totals[b] || 0) + 1;
    if (r.final_result === "Pass" || r.final_result === "Distinction") {
      passes[b] = (passes[b] || 0) + 1;
    }
  });
  const result = {};
  Object.keys(totals).forEach(b => {
    result[b] = Math.round(((passes[b] || 0) / totals[b]) * 100);
  });
  return result;
}

function weeklyClicks(engagement, filters = {}) {
  const weeks = {};
  engagement.forEach(r => {
    if (filters.education && filters.education !== "all" && r.highest_education !== filters.education) return;
    const w = parseInt(r.week) || 0;
    weeks[w] = (weeks[w] || 0) + (parseInt(r.sum_click) || 0);
  });
  return weeks;
}

function contentTypeEngagement(engagement) {
  const types = {};
  engagement.forEach(r => {
    const t = r.content_type || "Other";
    types[t] = (types[t] || 0) + (parseInt(r.sum_click) || 0);
  });
  return types;
}
