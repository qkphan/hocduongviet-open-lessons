import json
from pathlib import Path
from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[2]
print("path",ROOT)
SCHEMA_FILE = ROOT / "tools/schema/exams/exam_schema.json"
EXAM_FILE = Path(__file__).parent / "exam.json"
ERROR_FILE = Path(__file__).parent / "exam_errors.json"

schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
exam = json.loads(EXAM_FILE.read_text(encoding="utf-8"))

validator = Draft7Validator(schema)

errors = []

for err in validator.iter_errors(exam):
    q_index = None
    if "questions" in err.path:
        q_index = list(err.path)[1]

    errors.append({
        "question_id": exam["questions"][q_index].get("id") if q_index is not None else None,
        "index": q_index,
        "path": "/" + "/".join(map(str, err.path)),
        "type": "schema_error",
        "message": err.message,
        "expected": str(err.schema),
        "severity": "error"
    })

result = {
    "valid": len(errors) == 0,
    "summary": {
        "error": len(errors),
        "warning": 0
    },
    "errors": errors
}

ERROR_FILE.write_text(
    json.dumps(result, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("❌ Exam invalid" if errors else "✅ Exam valid")
