import json
from datetime import datetime
from pathlib import Path

def normalize_exam(input_path, output_path, source="ai"):
    raw = json.loads(Path(input_path).read_text(encoding="utf-8"))

    normalized = {
        "meta": {
            "version": "1.0.0",
            "source": source,
            "created_at": datetime.utcnow().isoformat() + "Z"
        },
        "exam": raw["exam"]
    }

    Path(output_path).write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"✅ Normalized → {output_path}")

if __name__ == "__main__":
    import sys
    normalize_exam(sys.argv[1], sys.argv[2])
