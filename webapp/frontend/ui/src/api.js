// Thin fetch wrapper around the Python backend (backend/server.py).
// Change API_BASE if you run the backend on a different host/port.

export const API_BASE = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

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

export function getInitialMetrics() {
  return request("/api/performance/initial");
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

export function translatePlainBpe(text) {
  return request("/api/translate", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, condition: "plain_bpe" }),
  });
}

export function translateAdapted(text, condition) {
 return request('/api/translate', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text,condition})});
}
export function tokenizeAdapted(text, condition) {
 return request('/api/tokenize/adapted', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text,condition})});
}
