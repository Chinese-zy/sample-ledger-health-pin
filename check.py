import json
from pathlib import Path

path = Path(__file__).with_name("books.json")
data = json.loads(path.read_text(encoding="utf-8"))
data["rows"].append({"id": "sample-2", "kind": "sample", "name": "核对写回"})
path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("checked", len(data["rows"]))
