/**
 * Château AI — Wine Quality Assessment Front-end Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  // 11 Feature Keys
  const features = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol"
  ];

  // Presets definition
  const presets = {
    reserve: {
      fixed_acidity: 8.5,
      volatile_acidity: 0.28,
      citric_acid: 0.52,
      residual_sugar: 1.8,
      chlorides: 0.055,
      free_sulfur_dioxide: 16.0,
      total_sulfur_dioxide: 35.0,
      density: 0.9946,
      pH: 3.30,
      sulphates: 0.82,
      alcohol: 12.8
    },
    table: {
      fixed_acidity: 7.8,
      volatile_acidity: 0.55,
      citric_acid: 0.15,
      residual_sugar: 2.2,
      chlorides: 0.082,
      free_sulfur_dioxide: 14.0,
      total_sulfur_dioxide: 46.0,
      density: 0.9968,
      pH: 3.36,
      sulphates: 0.62,
      alcohol: 10.2
    },
    defect: {
      fixed_acidity: 6.8,
      volatile_acidity: 0.98,
      citric_acid: 0.02,
      residual_sugar: 2.8,
      chlorides: 0.115,
      free_sulfur_dioxide: 8.0,
      total_sulfur_dioxide: 85.0,
      density: 0.9985,
      pH: 3.65,
      sulphates: 0.45,
      alcohol: 9.2
    },
    average: {
      fixed_acidity: 8.32,
      volatile_acidity: 0.53,
      citric_acid: 0.27,
      residual_sugar: 2.54,
      chlorides: 0.087,
      free_sulfur_dioxide: 15.9,
      total_sulfur_dioxide: 46.5,
      density: 0.9967,
      pH: 3.31,
      sulphates: 0.66,
      alcohol: 10.42
    }
  };

  // Two-way synchronization between slider and number input
  features.forEach(feat => {
    const slider = document.getElementById(`slider_${feat}`);
    const numInput = document.getElementById(feat);

    if (slider && numInput) {
      slider.addEventListener("input", (e) => {
        numInput.value = e.target.value;
      });

      numInput.addEventListener("input", (e) => {
        slider.value = e.target.value;
      });
    }
  });

  // Function to apply preset
  function applyPreset(presetData, activeBtnId) {
    features.forEach(feat => {
      const val = presetData[feat];
      const slider = document.getElementById(`slider_${feat}`);
      const numInput = document.getElementById(feat);
      if (slider && numInput && val !== undefined) {
        slider.value = val;
        numInput.value = val;
      }
    });

    document.querySelectorAll(".preset-btn").forEach(btn => btn.classList.remove("active"));
    if (activeBtnId) {
      const targetBtn = document.getElementById(activeBtnId);
      if (targetBtn) targetBtn.classList.add("active");
    }
  }

  // Preset button listeners
  const btnReserve = document.getElementById("btnPresetReserve");
  const btnTable = document.getElementById("btnPresetTable");
  const btnDeficient = document.getElementById("btnPresetDeficient");
  const btnReset = document.getElementById("btnResetDefault");

  if (btnReserve) btnReserve.addEventListener("click", () => applyPreset(presets.reserve, "btnPresetReserve"));
  if (btnTable) btnTable.addEventListener("click", () => applyPreset(presets.table, "btnPresetTable"));
  if (btnDeficient) btnDeficient.addEventListener("click", () => applyPreset(presets.defect, "btnPresetDeficient"));
  if (btnReset) btnReset.addEventListener("click", () => applyPreset(presets.average, "btnResetDefault"));

  // Set default initial preset
  applyPreset(presets.reserve, "btnPresetReserve");

  // Health check on startup
  async function checkHealth() {
    const statusDot = document.getElementById("statusDot");
    const statusText = document.getElementById("statusText");
    try {
      const res = await fetch("/health");
      if (res.ok) {
        const data = await res.json();
        if (data.model_loaded) {
          statusDot.className = "status-dot online";
          statusText.textContent = "ANN Model Online";
        } else {
          statusDot.className = "status-dot pulsing";
          statusText.textContent = "Model Initializing...";
        }
      } else {
        statusDot.className = "status-dot";
        statusText.textContent = "Service Unreachable";
      }
    } catch (e) {
      statusDot.className = "status-dot";
      statusText.textContent = "Backend Offline";
    }
  }
  checkHealth();

  // Handle Form Submission
  const form = document.getElementById("wineForm");
  const btnPredict = document.getElementById("btnPredict");

  // Keyboard shortcut Ctrl + Enter
  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      form.requestSubmit();
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Prepare JSON payload
    const payload = {};
    features.forEach(feat => {
      const input = document.getElementById(feat);
      payload[feat] = parseFloat(input.value);
    });

    // Loading State
    btnPredict.classList.add("loading");
    btnPredict.disabled = true;

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({ detail: "Unknown server error" }));
        throw new Error(errData.detail || "Prediction request failed");
      }

      const result = await response.json();
      renderResult(result);
    } catch (error) {
      alert("Error calculating prediction: " + error.message);
    } finally {
      btnPredict.classList.remove("loading");
      btnPredict.disabled = false;
    }
  });

  // Render prediction result to sidebar
  function renderResult(data) {
    const placeholder = document.getElementById("resultPlaceholder");
    const content = document.getElementById("resultContent");
    const timestamp = document.getElementById("resultTimestamp");

    const verdictBanner = document.getElementById("verdictBanner");
    const verdictIcon = document.getElementById("verdictIcon");
    const verdictTitle = document.getElementById("verdictTitle");
    const verdictTier = document.getElementById("verdictTier");

    const gaugeFill = document.getElementById("gaugeFill");
    const gaugePct = document.getElementById("gaugePct");
    const confidenceVal = document.getElementById("confidenceVal");
    const diagList = document.getElementById("diagList");

    const mAlcohol = document.getElementById("mAlcohol");
    const mPH = document.getElementById("mPH");
    const mVolatile = document.getElementById("mVolatile");
    const mSugar = document.getElementById("mSugar");

    placeholder.classList.add("hidden");
    content.classList.remove("hidden");

    // Set time
    const now = new Date();
    timestamp.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    // Verdict details
    if (data.is_good) {
      verdictBanner.className = "verdict-banner verdict-good";
      verdictIcon.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>`;
      verdictTitle.textContent = "GOOD QUALITY WINE";
      verdictTier.textContent = data.tier || "Premium Selection";
    } else {
      verdictBanner.className = "verdict-banner verdict-bad";
      verdictIcon.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`;
      verdictTitle.textContent = "DEFICIENT QUALITY";
      verdictTier.textContent = data.tier || "Sub-standard Vintage";
    }

    // Gauge bar animation
    const probPct = data.quality_probability_pct;
    gaugeFill.style.width = `${Math.min(Math.max(probPct, 2), 100)}%`;
    gaugePct.textContent = `${probPct.toFixed(1)}%`;
    confidenceVal.textContent = `${data.confidence_pct}% (${data.prediction.toUpperCase()})`;

    // Diagnostics Notes
    diagList.innerHTML = "";
    if (data.insights && data.insights.length > 0) {
      data.insights.forEach(note => {
        const li = document.createElement("li");
        li.textContent = note;
        diagList.appendChild(li);
      });
    } else {
      const li = document.createElement("li");
      li.textContent = "Balanced chemical composition across evaluated markers.";
      diagList.appendChild(li);
    }

    // Metric Chips
    if (data.metrics) {
      mAlcohol.textContent = data.metrics.alcohol_level || "--";
      mPH.textContent = data.metrics.ph_balance || "--";
      mVolatile.textContent = data.metrics.volatile_acidity || "--";
      mSugar.textContent = data.metrics.sugar_level || "--";
    }

    // Gentle scroll to result if on mobile
    if (window.innerWidth < 1180) {
      content.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }
});
