"""Zero-dependency HTTP API for the (unmodified) Kapampangan MorphBPE tokenizer.

Built on Python's standard library only (http.server) — no pip install
required, matching the philosophy of kapampangan_morphbpe_runtime itself
("pure standard library, no pip install, no internet"). This also means it
runs the same way on any machine with Python 3.11+, with zero dependency
surface to go wrong before a thesis defense.

Run with:  python server.py            (see the root README.md for details)
Serves on: http://127.0.0.1:8000
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent / "tokenizer"))

import trace_service  # noqa: E402
import comparison_service  # noqa: E402

HOST = "127.0.0.1"
PORT = 8000

# Allow the Vite dev server (default port 5173) — and a couple of common
# alternates — to call this API from the browser.
ALLOWED_ORIGINS = {
    "http://localhost:5173",
    "http://127.0.0.1:5173",
}


class Handler(BaseHTTPRequestHandler):
    server_version = "KapampanganTokenizerAPI/1.0"

    def _cors_origin(self) -> str:
        origin = self.headers.get("Origin", "")
        return origin if origin in ALLOWED_ORIGINS else "*"

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", self._cors_origin())
        self.send_header("Vary", "Origin")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:  # quieter default logging
        print(f"[server] {self.address_string()} - {fmt % args}")

    def do_OPTIONS(self) -> None:  # CORS preflight
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", self._cors_origin())
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Vary", "Origin")
        self.end_headers()

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        try:
            if path == "/api/health":
                self._send_json(
                    200,
                    {
                        "status": "ok",
                        "vocabulary_size": trace_service.TOKENIZER.vocabulary_size,
                        "artifact": "morphbpe-penalty8",
                    },
                )
            elif path == "/api/examples":
                self._send_json(200, trace_service.examples())
            else:
                self._send_json(404, {"error": f"not found: {path}"})
        except Exception as exc:  # pragma: no cover - defensive
            self._send_json(500, {"error": str(exc)})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path not in ("/api/tokenize", "/api/comparison/custom"):
            self._send_json(404, {"error": f"not found: {path}"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length) if length else b"{}"
            data = json.loads(raw_body.decode("utf-8") or "{}")
            text = data.get("text", "")
            if not isinstance(text, str):
                raise ValueError("`text` must be a string")
            if path == "/api/tokenize":
                result = trace_service.analyze(text)
            else:
                result = comparison_service.custom_compare(text)
            self._send_json(200, result)
        except Exception as exc:
            self._send_json(400, {"error": str(exc)})


def main() -> None:
    passed, total = trace_service.verify_fidelity()
    print(f"[startup] trace/encode parity check: {passed}/{total} words passed")
    scoring_passed, scoring_total = comparison_service.verify_scoring_fidelity()
    print(f"[startup] scoring-explain parity check: {scoring_passed}/{scoring_total} cases passed")
    print(f"[startup] tokenizer artifact loaded: morphbpe-penalty8 "
          f"(vocab size {trace_service.TOKENIZER.vocabulary_size})")
    print(f"[startup] comparison artifacts loaded: plain-bpe "
          f"(vocab size {comparison_service.PLAIN.vocabulary_size}), "
          f"unigram-lm-6080 (vocab size {comparison_service.UNI.vocabulary_size})")
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"[startup] serving on http://{HOST}:{PORT}  (Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[shutdown] stopping server")
        httpd.shutdown()


if __name__ == "__main__":
    main()
