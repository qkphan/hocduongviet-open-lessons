import json
from pathlib import Path
from rules.schema import validate_schema
from rules.logic import validate_logic
from rules.latex import validate_latex

def validate_file(path: Path):
    errors = []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [errors(
            code="INVALID_JSON",
            file=path.name,
            path="",
            message=str(e),
            expected="valid JSON",
            actual="invalid"
        )]

    exam = data.get("exam")
    if not exam:
        return [error(
            code="MISSING_FIELD",
            file=path.name,
            path="exam",
            message="Missing root field: exam",
            expected="object",
            actual=None
        )]

    errors += validate_schema(exam, path.name)
    errors += validate_logic(exam, path.name)
    errors += validate_latex(exam, path.name)

    return errors

def validate_dir(dir_path: Path):
    all_errors = []

    for file in dir_path.glob("*.json"):
        all_errors.extend(validate_file(file))

    return {
        "valid": len(all_errors) == 0,
        "errors": all_errors
    }

if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1])

    if target.is_dir():
        result = validate_dir(target)
    else:
        result = {
            "valid": True,
            "errors": validate_file(target)
        }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["valid"] else 1)
