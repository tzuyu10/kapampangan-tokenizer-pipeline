// Thin fetch wrapper around the Python backend (backend/server.py).
// Change API_BASE if you run the backend on a different host/port.

export const API_BASE = "http://127.0.0.1:8000";

async function request(path, options) {
  const res = await fetch(`${API_BASE}${path}`, options);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || `Request to ${path} failed (${res.status})`);
  }
  return data;
}

export function tokenize(text) {
  return request("/api/tokenize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
}

export function getExamples() {
  return request("/api/examples");
}

export function getHealth() {
  return request("/api/health");
}

export function compareCustom(text) {
  return request("/api/comparison/custom", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
}

export function getTranslationStatus() {
  return request("/api/translation/status");
}

export function compareTranslations(text) {
  return request("/api/translate/compare", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
}
