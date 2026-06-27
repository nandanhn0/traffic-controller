const lanes = ["north", "south", "east", "west"];

function buildLaneInputs() {
  const container = document.getElementById("lane-inputs");
  container.innerHTML = "";
  lanes.forEach((lane) => {
    const wrapper = document.createElement("label");
    wrapper.innerHTML = `
      ${lane}
      <input id="lane-${lane}" type="number" min="0" value="3" />
    `;
    container.appendChild(wrapper);
  });
}

function collectPayload() {
  const incoming_traffic = {};
  lanes.forEach((lane) => {
    const input = document.getElementById(`lane-${lane}`);
    incoming_traffic[lane] = Number(input.value || 0);
  });
  const selected = document.getElementById("emergency-lane").value;
  return {
    incoming_traffic,
    emergency_lanes: selected ? [selected] : [],
  };
}

async function refreshState() {
  const response = await fetch("/api/state");
  const data = await response.json();
  document.getElementById("state-output").textContent = JSON.stringify(data, null, 2);
}

async function runStep() {
  await fetch("/api/step", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(collectPayload()),
  });
  await refreshState();
}

async function resetController() {
  await fetch("/api/reset", { method: "POST" });
  await refreshState();
}

function init() {
  buildLaneInputs();
  document.getElementById("step-btn").addEventListener("click", runStep);
  document.getElementById("reset-btn").addEventListener("click", resetController);
  refreshState();
}

init();
