import os
import sys
import urllib.request


def main():
    port = int(os.environ.get("PORT", "8080"))
    url = f"http://127.0.0.1:{port}/health"
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            if response.status != 200:
                return 1
            return 0 if response.read() == b"ok" else 1
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
