const API_BASE = "https://meditriage-dum7.onrender.com";

const symptomList = document.getElementById("symptomList");
const searchBar = document.getElementById("searchBar");
const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");
const selectedCount = document.getElementById("selectedCount");
const statusEl = document.getElementById("status");

let ALL_SYMPTOMS = [];

function updateCount() {
  selectedCount.textContent = document.querySelectorAll(".symptom-card.selected").length;
}

function makeCard(symptom) {
  const card = document.createElement("div");
  card.className = "symptom-card";
  card.dataset.value = symptom;

  card.innerHTML = `
    <div>
      <div class="name">${symptom}</div>
      <div class="tag">tap to select</div>
    </div>
    <div class="checkmark">✓</div>
  `;

  card.addEventListener("click", () => {
    card.classList.toggle("selected");
    updateCount();
  });

  return card;
}

async function loadSymptoms() {
  statusEl.textContent = "Loading symptoms…";

  try {
    const res = await fetch(`${API_BASE}/symptoms`);
    const data = await res.json();

    ALL_SYMPTOMS = data.symptoms || [];
    symptomList.innerHTML = "";

    ALL_SYMPTOMS.forEach(sym => symptomList.appendChild(makeCard(sym)));
    updateCount();

    statusEl.textContent = "";
  } catch (err) {
    console.error(err);
    statusEl.textContent = "❌ Failed to load symptoms. Backend may be sleeping—refresh in 30–60s.";
  }
}

searchBar.addEventListener("input", () => {
  const q = searchBar.value.toLowerCase();
  document.querySelectorAll(".symptom-card").forEach(card => {
    const name = card.dataset.value.toLowerCase();
    card.style.display = name.includes(q) ? "" : "none";
  });
});

clearBtn.addEventListener("click", () => {
  document.querySelectorAll(".symptom-card.selected").forEach(c => c.classList.remove("selected"));
  updateCount();
});

analyzeBtn.addEventListener("click", async () => {
  const selected = Array.from(document.querySelectorAll(".symptom-card.selected"))
    .map(c => c.dataset.value);

  if (selected.length === 0) {
    alert("Please select at least one symptom.");
    return;
  }

  statusEl.textContent = "Analyzing…";
  analyzeBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symptoms: selected })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data?.error || "Server error");

    localStorage.setItem("predictionData", JSON.stringify({
      ...data,
      selectedSymptoms: selected
    }));

    window.location.href = "results.html";
  } catch (err) {
    console.error(err);
    alert("Backend error. If Render is on Free tier, it may take ~50s to wake up. Try again.");
    statusEl.textContent = "";
  } finally {
    analyzeBtn.disabled = false;
  }
});

loadSymptoms();
