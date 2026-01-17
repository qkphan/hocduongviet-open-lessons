import json
from jsonschema import validate, ValidationError
from pathlib import Path

SCHEMA_PATH = Path("tools/schema/exams/exam.data.schema.json")

def validate_exam(json_path):
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    try:
        validate(instance=data, schema=schema)
        return {"ok": True, "errors": []}
    except ValidationError as e:
        return {
            "ok": False,
            "errors": [{
                "message": e.message,
                "path": list(e.path)
            }]
        }

if __name__ == "__main__":
    import sys
    result = validate_exam(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
