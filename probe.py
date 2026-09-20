import os
import sys
import urllib.request

port = os.environ.get("PORT", "8080")
url = f"http://127.0.0.1:{port}/health"

try:
    with urllib.request.urlopen(url, timeout=2) as response:
        if response.status != 200 or response.read() != b"ok":
            sys.exit(1)
except Exception:
    sys.exit(1)
