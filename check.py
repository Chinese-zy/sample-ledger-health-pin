import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("rows"), list):
        raise ValueError("账本结构非法：缺少 rows")
    return data


def real_rows(data):
    return [row for row in data["rows"] if row.get("kind") != "sample"]


def stamp_version(rows, override=""):
    version = override.strip()
    if not version:
        digest = hashlib.sha256(
            json.dumps(rows, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()
        version = digest[:12]
    return version


def main():
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "ledger" / "books.json"
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    version_override = sys.argv[3] if len(sys.argv) > 3 else ""

    data = load(source)
    rows = real_rows(data)
    if not rows:
        raise ValueError("真账为空，拒绝产出")

    checked = dict(data)
    checked["rows"] = rows
    checked["version"] = stamp_version(rows, version_override)

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(checked, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (output.parent / f"{output.stem}.version").write_text(
            checked["version"] + "\n", encoding="utf-8"
        )

    print("checked", len(rows), "rows; version", checked["version"])


if __name__ == "__main__":
    main()
