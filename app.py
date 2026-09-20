import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
LEDGER_PATH = os.path.join(ROOT, "books.json")
VERSION_ANCHOR = os.path.join(ROOT, "books.version")


def expected_version():
    override = os.environ.get("LEDGER_VERSION", "").strip()
    if override:
        return override
    try:
        with open(VERSION_ANCHOR, encoding="utf-8") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def load_books():
    with open(LEDGER_PATH, encoding="utf-8") as handle:
        data = json.load(handle)
    version = str(data.get("version", "")).strip()
    if not version:
        raise RuntimeError("账本缺少 version，拒绝启动")
    expected = expected_version()
    if not expected:
        raise RuntimeError("缺少构建时账本版本锚点，拒绝启动")
    if version != expected:
        raise RuntimeError(
            f"账本版本不匹配: 镜像要求 {expected!r}, 实际 {version!r}"
        )
    if any(row.get("kind") == "sample" for row in data.get("rows", [])):
        raise RuntimeError("最终账本中混入样例数据，拒绝启动")
    return data


BOOKS = None


def books():
    return BOOKS

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b"ok"
        elif self.path.startswith("/query"):
            body = json.dumps(books()).encode()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body)

def main():
    global BOOKS
    BOOKS = load_books()
    port = int(os.environ.get("PORT", "8080"))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("startup failed:", exc)
        raise SystemExit(1)
