const $ = (id) => document.getElementById(id);
const POLL_MS = 1200;
const COPY = {
  queued: ["Queued", "Waiting to start."],
  running: ["Generating", "Script, footage, voice, subtitles, render. This takes a few minutes."],
  completed: ["Video ready", "Preview it above or download it."],
  failed: ["Generation failed", ""],
  cancelled: ["Cancelled", "Nothing was saved."],
};
const FINAL = ["completed", "failed", "cancelled"];

let jobId = null;
let pollHandle = null;
let lastEvent = 0;

async function api(path, options) {
  const response = await fetch(path, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || `Request failed (${response.status})`);
  return data;
}

function fillSelect(select, items, selected) {
  select.replaceChildren(
    ...items.map((item) => {
      const option = document.createElement("option");
      option.value = item.value ?? item;
      option.textContent = item.label ?? item;
      return option;
    })
  );
  select.value = selected;
}

async function loadConfig() {
  try {
    const cfg = await api("/api/config");
    fillSelect($("model"), cfg.models, cfg.model);
    fillSelect($("voice"), cfg.voices, cfg.voice);
    fillSelect($("position"), cfg.positions, cfg.position);
    fillSelect($("color"), cfg.colors, cfg.color);
    $("configWarning").textContent = cfg.warning;
    $("configWarning").hidden = !cfg.warning;
  } catch (err) {
    $("configWarning").textContent = `Could not reach the server: ${err.message}`;
    $("configWarning").hidden = false;
  }
}

function setPreview(state, line = "", detail = "") {
  $("preview").dataset.state = state;
  $("frame").dataset.state = state;
  $("statusLine").textContent = line;
  $("statusLine").hidden = !line;
  $("statusDetail").textContent = detail;
  $("statusDetail").hidden = !detail;
  const done = state === "done";
  $("video").hidden = !done;
  $("frameText").hidden = done;
  $("download").hidden = !done;
  if (!done) $("video").removeAttribute("src");
}

function appendLog({ message, level }) {
  const row = document.createElement("div");
  row.className = level || "";
  row.textContent = message;
  $("log").appendChild(row);
  $("log").scrollTop = $("log").scrollHeight;
}

function setBusy(busy) {
  $("generate").disabled = busy;
  $("generate").textContent = busy ? "Generating…" : "Generate";
  $("cancel").hidden = !busy;
  $("form").setAttribute("aria-busy", String(busy));
  if (!busy) {
    clearInterval(pollHandle);
    pollHandle = null;
  }
}

async function poll() {
  if (!jobId) return;
  try {
    const { events } = await api(`/api/jobs/${jobId}/events?after=${lastEvent}`);
    events.forEach((event) => {
      appendLog(event);
      lastEvent = Math.max(lastEvent, event.id);
    });
    const { job } = await api(`/api/jobs/${jobId}`);
    const [line, detail] = COPY[job.state] || COPY.running;
    if (job.state === "completed") {
      setPreview("done", line, detail);
      $("video").src = `/api/jobs/${jobId}/download?inline=1`;
      $("download").href = `/api/jobs/${jobId}/download`;
    } else {
      setPreview(job.state, line, job.state === "failed" ? job.errorMessage || detail : detail);
      if (job.state === "running") $("frameText").textContent = "Rendering…";
    }
    if (FINAL.includes(job.state)) setBusy(false);
  } catch {
    /* transient */
  }
}

function readForm() {
  const data = Object.fromEntries(new FormData($("form")));
  data.upload = $("upload").checked;
  data.paragraphs = Number(data.paragraphs) || 1;
  data.threads = navigator.hardwareConcurrency || 2;
  return data;
}

async function generate(event) {
  event.preventDefault();
  const subject = $("subject");
  const empty = !subject.value.trim();
  $("subjectError").hidden = !empty;
  subject.setAttribute("aria-invalid", String(empty));
  if (empty) return subject.focus();

  $("log").replaceChildren();
  $("logWrap").hidden = false;
  $("frameText").textContent = "Starting…";
  lastEvent = 0;
  setBusy(true);
  setPreview("running", ...COPY.queued);
  try {
    const result = await api("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(readForm()),
    });
    jobId = result.jobId;
    pollHandle = setInterval(poll, POLL_MS);
    poll();
  } catch (err) {
    setPreview("failed", COPY.failed[0], err.message);
    setBusy(false);
  }
}

function cancel() {
  if (!jobId) return;
  $("cancel").disabled = true;
  api(`/api/jobs/${jobId}/cancel`, { method: "POST" })
    .catch((err) => setPreview("failed", "Could not cancel", err.message))
    .finally(() => ($("cancel").disabled = false));
}

$("form").addEventListener("submit", generate);
$("cancel").addEventListener("click", cancel);
$("subject").addEventListener("input", () => {
  $("subjectError").hidden = true;
  $("subject").removeAttribute("aria-invalid");
});
loadConfig();
