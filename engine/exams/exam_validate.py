# engine/exams/exam_validate.py
import json
import sys
from jsonschema import Draft7Validator

SCHEMA_PATH = "tools/schema/exams/exam_schema.json"
DATA_PATH = "exams/toan/lop11/ham-so-mu-va-logarit/content/exam_data.json"
ERROR_OUTPUT = "exams/toan/lop11/ham-so-mu-va-logarit/content/validation_errors.json"


def run_exam_validate():
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)

    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    if errors:
        error_report = []
        for e in errors:
            error_report.append({
                "path": "/".join(map(str, e.path)),
                "message": e.message
            })

        with open(ERROR_OUTPUT, "w", encoding="utf-8") as f:
            json.dump(error_report, f, indent=2, ensure_ascii=False)

        print("❌ Exam data schema validation FAILED")
        print(f"→ Errors written to {ERROR_OUTPUT}")
        sys.exit(1)

    print("✅ Exam data schema validation PASSED")
    sys.exit(0)


if __name__ == "__main__":
    run_exam_validate()
