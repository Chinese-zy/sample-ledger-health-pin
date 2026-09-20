import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOKS_CANDIDATES = [
    os.path.join(ROOT, "books.json"),
    os.path.join(ROOT, "ledger", "books.json"),
]
BOOKS_PATH = next((p for p in BOOKS_CANDIDATES if os.path.exists(p)), BOOKS_CANDIDATES[0])

def books():
    with open(BOOKS_PATH, encoding="utf-8") as handle:
        return json.load(handle)

def load_books():
    data = books()
    version = data.get("version")
    expected = os.environ.get("LEDGER_VERSION", "")
    if not version or not expected or version != expected:
        print(
            f"ledger version mismatch: loaded={version!r} expected={expected!r}",
            file=sys.stderr,
        )
        sys.exit(1)
    return data

LEDGER = None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b"ok"
        elif self.path.startswith("/query"):
            body = json.dumps(LEDGER).encode()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body)

def main():
    global LEDGER
    LEDGER = load_books()
    port = int(os.environ.get("PORT", "8080"))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

if __name__ == "__main__":
    main()
