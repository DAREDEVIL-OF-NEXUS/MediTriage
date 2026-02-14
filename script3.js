document.addEventListener("DOMContentLoaded", () => {
  const dataRaw = localStorage.getItem("predictionData");

  const symptomsUl = document.getElementById("symptomsUl");
  const precUl = document.getElementById("precUl");
  const predBox = document.getElementById("predBox");
  const metaBox = document.getElementById("metaBox");
  const clearBtn = document.getElementById("clearBtn");

  if (!dataRaw) {
    predBox.textContent = "No result found.";
    metaBox.textContent = "Go to Symptom Checker and click Analyze.";
    return;
  }

  const data = JSON.parse(dataRaw);

  const selected = data.selectedSymptoms || [];
  symptomsUl.innerHTML = selected.map(s => `<li>${s}</li>`).join("") || "<li>—</li>";

  predBox.textContent = data.prediction ? String(data.prediction) : "—";

  metaBox.innerHTML = `
    <div><b>Confidence:</b> ${data.confidence ?? "—"}%</div>
    <div><b>Severity:</b> ${data.severity ?? "—"}</div>
  `;

  const precautions = Array.isArray(data.precautions) ? data.precautions : [];
  precUl.innerHTML = precautions.map(p => `<li>${p}</li>`).join("") || "<li>—</li>";

  clearBtn.addEventListener("click", () => {
    localStorage.removeItem("predictionData");
    window.location.href = "checkout.html";
  });
});
