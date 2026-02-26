const $ = (sel) => document.querySelector(sel);

function apiBase() {
  return ($("#apiBase").value || "http://localhost:8000").replace(/\/+$/, "");
}

function setStatus(msg, isError = false) {
  const el = $("#status");
  el.textContent = msg || "";
  el.classList.toggle("error", isError);
}

async function apiFetch(path, options = {}) {
  const url = apiBase() + path;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch {}

  if (!res.ok) {
    const detail = (data && (data.detail || data.message))
      ? (data.detail || data.message)
      : text;
    throw new Error(`${res.status} ${res.statusText}${detail ? ` — ${detail}` : ""}`);
  }

  return data;
}

function toNullIfEmpty(s) {
  const t = (s ?? "").trim();
  return t === "" ? null : t;
}

function numOrNull(s) {
  const t = (s ?? "").trim();
  if (t === "") return null;
  const n = Number(t);
  return Number.isFinite(n) ? n : null;
}

let clientsCache = [];

async function loadClients() {
  setStatus("Loading clients...");
  const clients = await apiFetch("/clients/");
  clientsCache = Array.isArray(clients) ? clients : [];
  renderClientSelect();
  renderClientsTable();
  setStatus(`Loaded ${clientsCache.length} client(s).`);
}

function renderClientSelect() {
  const sel = $("#clientSelect");
  sel.innerHTML = "";

  if (clientsCache.length === 0) {
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = "No clients yet";
    sel.appendChild(opt);
    sel.disabled = true;
    return;
  }

  sel.disabled = false;
  for (const c of clientsCache) {
    const opt = document.createElement("option");
    opt.value = String(c.id);
    opt.textContent = `#${c.id} — ${c.first_name} ${c.last_name} (${c.email})`;
    sel.appendChild(opt);
  }
}

function renderClientsTable() {
  const tbody = $("#clientsTable tbody");
  tbody.innerHTML = "";

  const q = ($("#clientFilter").value || "").toLowerCase().trim();
  const rows = clientsCache.filter((c) => {
    if (!q) return true;
    const hay = `${c.first_name} ${c.last_name} ${c.email}`.toLowerCase();
    return hay.includes(q);
  });

  for (const c of rows) {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${c.id}</td>
      <td>${escapeHtml(`${c.first_name} ${c.last_name}`)}</td>
      <td>${escapeHtml(c.email)}</td>
      <td>$${Number(c.hourly_rate).toFixed(2)}</td>
      <td><button data-client-id="${c.id}" class="mini">Summary</button></td>
    `;

    tbody.appendChild(tr);
  }

  tbody.querySelectorAll("button[data-client-id]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = Number(btn.getAttribute("data-client-id"));
      await loadClientSummary(id);
    });
  });
}

async function loadGlobalSummary() {
  setStatus("Loading global summary...");
  const summary = await apiFetch("/summary");
  $("#summaryBox").textContent = JSON.stringify(summary, null, 2);
  setStatus("Loaded global summary.");
}

async function loadClientSummary(clientId) {
  setStatus(`Loading summary for client ${clientId}...`);
  const summary = await apiFetch(`/clients/${clientId}/summary`);
  $("#summaryBox").textContent = JSON.stringify(summary, null, 2);
  setStatus(`Loaded client ${clientId} summary.`);
}

async function handleCreateClient(e) {
  e.preventDefault();
  setStatus("Creating client...");

  const fd = new FormData(e.target);
  const payload = {
    first_name: (fd.get("first_name") || "").trim(),
    last_name: (fd.get("last_name") || "").trim(),
    email: (fd.get("email") || "").trim(),
    phone: toNullIfEmpty(fd.get("phone")),
    subject: toNullIfEmpty(fd.get("subject")),
    hourly_rate: Number(fd.get("hourly_rate")),
  };

  if (!payload.first_name || !payload.last_name || !payload.email || !Number.isFinite(payload.hourly_rate)) {
    setStatus("Please fill first name, last name, email, and hourly rate.", true);
    return;
  }

  await apiFetch("/clients/", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  e.target.reset();
  await loadClients();
  setStatus("Client created.");
}

async function handleCreateSession(e) {
  e.preventDefault();
  setStatus("Logging session...");

  const fd = new FormData(e.target);
  const clientId = Number(fd.get("client_id"));

  const payload = {
    client_id: clientId,
    date: (fd.get("date") || "").trim(),
    duration_hours: Number(fd.get("duration_hours")),
    topic: toNullIfEmpty(fd.get("topic")),
    notes: toNullIfEmpty(fd.get("notes")),
  };

  if (!Number.isFinite(payload.client_id) || !payload.date || !Number.isFinite(payload.duration_hours)) {
    setStatus("Please select a client and fill date + duration.", true);
    return;
  }

  await apiFetch("/sessions/", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  e.target.reset();
  await loadClients();
  await loadGlobalSummary();
  setStatus("Session logged.");
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

window.addEventListener("DOMContentLoaded", async () => {
  $("#clientForm").addEventListener("submit", async (e) => {
    try { await handleCreateClient(e); }
    catch (err) { setStatus(String(err.message || err), true); }
  });

  $("#sessionForm").addEventListener("submit", async (e) => {
    try { await handleCreateSession(e); }
    catch (err) { setStatus(String(err.message || err), true); }
  });

  $("#refreshBtn").addEventListener("click", async () => {
    try {
      await loadClients();
      await loadGlobalSummary();
    } catch (err) {
      setStatus(String(err.message || err), true);
    }
  });

  $("#loadClientsBtn").addEventListener("click", async () => {
    try { await loadClients(); }
    catch (err) { setStatus(String(err.message || err), true); }
  });

  $("#loadGlobalSummaryBtn").addEventListener("click", async () => {
    try { await loadGlobalSummary(); }
    catch (err) { setStatus(String(err.message || err), true); }
  });

  $("#loadClientSummaryBtn").addEventListener("click", async () => {
    try {
      const sel = $("#clientSelect");
      const id = Number(sel.value);
      if (!Number.isFinite(id)) throw new Error("No client selected.");
      await loadClientSummary(id);
    } catch (err) {
      setStatus(String(err.message || err), true);
    }
  });

  $("#clientFilter").addEventListener("input", () => renderClientsTable());

  try {
    await loadClients();
    await loadGlobalSummary();
  } catch (err) {
    setStatus(
      `Could not reach API. Is backend running at ${apiBase()}? (${String(err.message || err)})`,
      true
    );
  }
});