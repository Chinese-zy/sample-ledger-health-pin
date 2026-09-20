import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ledger_candidates = [ROOT / "books.json", ROOT / "ledger" / "books.json"]
ledger_path = next((p for p in ledger_candidates if p.exists()), ledger_candidates[0])

candidates = [
    ROOT / "samples" / "books.json",
    ROOT.parent / "samples" / "books.json",
    Path("/opt/samples/books.json"),
]
samples_path = next((p for p in candidates if p.exists()), candidates[0])

ledger = json.loads(ledger_path.read_text(encoding="utf-8"))

if not ledger.get("version"):
    raise SystemExit("ledger version missing")
if any(row.get("kind") == "sample" for row in ledger.get("rows", [])):
    raise SystemExit("sample rows must not live in the final ledger")

samples = json.loads(samples_path.read_text(encoding="utf-8"))
sample_row = {"id": "sample-2", "kind": "sample", "name": "核对写回"}
if not any(row.get("id") == sample_row["id"] for row in samples.get("rows", [])):
    samples.setdefault("rows", []).append(sample_row)
samples_path.write_text(
    json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("checked", len(ledger["rows"]))
