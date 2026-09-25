const TOKEN_KEY = "legalease_token";
let currentUser = null;
let analyses = [];
let documents = [];

const $ = (id) => document.getElementById(id);
const token = () => localStorage.getItem(TOKEN_KEY);

function toast(message) {
  const host = $("toast");
  const item = document.createElement("div");
  item.className = "toast";
  item.textContent = message;
  host.appendChild(item);
  setTimeout(() => item.remove(), 2800);
}

async function api(path, options = {}) {
  const request = { ...options, headers: { ...(options.headers || {}) } };
  if (request.body && typeof request.body !== "string" && !(request.body instanceof FormData)) {
    request.body = JSON.stringify(request.body);
  }
  if (request.body && !(request.body instanceof FormData)) {
    request.headers["Content-Type"] = "application/json";
  }
  if (token()) request.headers.Authorization = `Bearer ${token()}`;

  const response = await fetch(path, request);
  let data = {};
  try { data = await response.json(); } catch (_) {}

  if (!response.ok) {
    const detail = Array.isArray(data.detail)
      ? data.detail.map((x) => x.msg).join(", ")
      : data.detail;
    throw new Error(detail || `Request failed (${response.status})`);
  }
  return data;
}

function showAuth(mode) {
  $("loginForm").classList.toggle("hidden", mode !== "login");
  $("registerForm").classList.toggle("hidden", mode !== "register");
  $("loginTab").classList.toggle("active", mode === "login");
  $("registerTab").classList.toggle("active", mode === "register");
}

async function login(event) {
  event.preventDefault();
  try {
    const data = await api("/api/auth/login", {
      method: "POST",
      body: { email: $("loginEmail").value.trim(), password: $("loginPassword").value },
    });
    localStorage.setItem(TOKEN_KEY, data.access_token);
    await startApp();
  } catch (error) { toast(error.message); }
}

async function register(event) {
  event.preventDefault();
  try {
    const data = await api("/api/auth/register", {
      method: "POST",
      body: {
        name: $("registerName").value.trim(),
        email: $("registerEmail").value.trim(),
        password: $("registerPassword").value,
      },
    });
    localStorage.setItem(TOKEN_KEY, data.access_token);
    await startApp();
  } catch (error) { toast(error.message); }
}

function logout() {
  localStorage.removeItem(TOKEN_KEY);
  currentUser = null;
  analyses = [];
  documents = [];
  $("appScreen").classList.add("hidden");
  $("authScreen").classList.remove("hidden");
  showAuth("login");
}

async function startApp() {
  if (!token()) return logout();
  try {
    currentUser = await api("/api/auth/me");
    $("authScreen").classList.add("hidden");
    $("appScreen").classList.remove("hidden");
    const initial = (currentUser.name || "U")[0].toUpperCase();
    $("sideName").textContent = currentUser.name;
    $("sideEmail").textContent = currentUser.email;
    $("avatar").textContent = initial;
    $("profileAvatar").textContent = initial;
    $("profileName").textContent = currentUser.name;
    $("profileEmail").textContent = currentUser.email;
    await Promise.all([loadAnalyses(), loadDocuments()]);
    navigate("dashboard");
  } catch (error) {
    localStorage.removeItem(TOKEN_KEY);
    $("authScreen").classList.remove("hidden");
    $("appScreen").classList.add("hidden");
    showAuth("login");
    toast("Session expired. Please log in again.");
  }
}

function navigate(view) {
  document.querySelectorAll(".view").forEach((element) => element.classList.add("hidden"));
  const target = $(`${view}View`);
  if (target) target.classList.remove("hidden");
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === view);
  });
  $("pageTitle").textContent = {
    dashboard: "Dashboard", assistant: "AI Assistant", documents: "Documents",
    history: "Analysis History", profile: "Profile",
  }[view] || "LegalEase";
  if (view === "dashboard") renderDashboard();
  if (view === "history") renderHistory();
  if (view === "documents") renderDocuments();
  document.querySelector(".sidebar")?.classList.remove("open");
}

function toggleSidebar() { document.querySelector(".sidebar")?.classList.toggle("open"); }

async function loadAnalyses() {
  analyses = await api("/api/analysis");
  renderDashboard();
  renderHistory();
}

async function loadDocuments() {
  documents = await api("/api/documents");
  renderDashboard();
  renderDocuments();
}

function renderDashboard() {
  $("statAnalyses").textContent = analyses.length;
  $("statDocuments").textContent = documents.length;
  $("recentAnalyses").innerHTML = analyses.slice(0, 4).map((item) => `
    <div class="list-item"><b>${esc(item.title)}</b><small>${esc(item.category)} • ${date(item.created_at)}</small></div>
  `).join("") || `<div class="list-item"><small>No analyses yet.</small></div>`;
}

async function analyzeIssue(event) {
  event.preventDefault();
  const button = $("analyzeButton");
  button.disabled = true;
  button.textContent = "Analyzing...";
  $("aiStatus").textContent = "Working";
  $("aiResponse").classList.remove("empty");
  $("aiResponse").textContent = "Preparing response...";
  try {
    const item = await api("/api/analysis", {
      method: "POST",
      body: {
        title: $("analysisTitle").value.trim(),
        category: $("analysisCategory").value,
        issue: $("analysisIssue").value.trim(),
      },
    });
    $("aiResponse").textContent = item.response;
    $("aiStatus").textContent = "Complete";
    analyses = [item, ...analyses.filter((x) => x.id !== item.id)];
    renderDashboard();
    renderHistory();
  } catch (error) {
    $("aiResponse").textContent = error.message;
    $("aiStatus").textContent = "Error";
  } finally {
    button.disabled = false;
    button.textContent = "Analyze with LegalEase ✦";
  }
}

function renderHistory() {
  $("historyList").innerHTML = analyses.map((item) => `
    <article class="history-item">
      <b>${esc(item.title)}</b>
      <small>${esc(item.category)} • ${date(item.created_at)}</small>
      <p>${esc(item.response)}</p>
    </article>
  `).join("") || `<div class="card"><p>No analysis history yet.</p></div>`;
}

function renderDocuments() {
  const selected = $("docId").value;
  $("documentList").innerHTML = documents.map((doc) => `
    <button class="document-item ${String(doc.id) === String(selected) ? "active" : ""}" onclick="openDocument(${doc.id})">
      <b>${esc(doc.title)}</b><small>Updated ${date(doc.updated_at)}</small>
    </button>
  `).join("") || `<div class="list-item"><small>No documents yet.</small></div>`;
}

function newDocument() {
  navigate("documents");
  $("docId").value = "";
  $("docTitle").value = "";
  $("docContent").value = "";
  renderDocuments();
  $("docTitle").focus();
}

function openDocument(id) {
  const doc = documents.find((item) => item.id === id);
  if (!doc) return;
  $("docId").value = doc.id;
  $("docTitle").value = doc.title;
  $("docContent").value = doc.content;
  renderDocuments();
}

async function saveDocument() {
  const id = $("docId").value;
  const payload = { title: $("docTitle").value.trim() || "Untitled Document", content: $("docContent").value };
  try {
    let saved;
    if (id) {
      saved = await api(`/api/documents/${id}`, { method: "PUT", body: payload });
      documents = documents.map((doc) => doc.id === Number(id) ? saved : doc);
    } else {
      saved = await api("/api/documents", { method: "POST", body: payload });
      documents = [saved, ...documents];
      $("docId").value = saved.id;
    }
    renderDocuments();
    renderDashboard();
    toast("Document saved");
  } catch (error) { toast(error.message); }
}

async function deleteCurrentDocument() {
  const id = $("docId").value;
  if (!id) return toast("Select a document first");
  if (!confirm("Delete this document?")) return;
  try {
    await api(`/api/documents/${id}`, { method: "DELETE" });
    documents = documents.filter((doc) => doc.id !== Number(id));
    newDocument();
    renderDashboard();
    toast("Document deleted");
  } catch (error) { toast(error.message); }
}

function date(value) {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? "Unknown date" : parsed.toLocaleString();
}

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;",
  }[character]));
}

window.addEventListener("DOMContentLoaded", () => token() ? startApp() : showAuth("login"));
