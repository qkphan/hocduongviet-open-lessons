#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from errors import make_error
from registry import SECTION_RULES


# -------------------------
# FILE LEVEL
# -------------------------
def validate_file(path: Path):
    errors = []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [make_error(
            code="INVALID_JSON",
            file=path.name,
            path="",
            message=str(e),
            expected="valid JSON",
            actual="invalid",
            severity="error"
        )]

    # -------------------------
    # META
    # -------------------------
    if "meta" not in data or not isinstance(data["meta"], dict):
        errors.append(make_error(
            code="MISSING_FIELD",
            file=path.name,
            path="meta",
            message="Missing or invalid meta section",
            severity="error"
        ))
    else:
        if "title" not in data["meta"]:
            errors.append(make_error(
                code="MISSING_FIELD",
                file=path.name,
                path="meta.title",
                message="Missing exam title",
                severity="warning"
            ))

    # -------------------------
    # SECTIONS
    # -------------------------
    if "sections" not in data or not isinstance(data["sections"], list):
        errors.append(make_error(
            code="INVALID_FIELD",
            file=path.name,
            path="sections",
            message="sections must be an array",
            severity="error"
        ))
        return errors

    if not data["sections"]:
        errors.append(make_error(
            code="EMPTY_SECTIONS",
            file=path.name,
            path="sections",
            message="Exam has no sections",
            severity="warning"
        ))
        return errors

    # -------------------------
    # SECTION LEVEL
    # -------------------------
    for si, sec in enumerate(data["sections"]):
        sec_path = f"sections[{si}]"

        if not isinstance(sec, dict):
            errors.append(make_error(
                code="INVALID_SECTION",
                file=path.name,
                path=sec_path,
                message="Section must be an object",
                severity="error"
            ))
            continue

        sec_type = sec.get("type")
        if not sec_type:
            errors.append(make_error(
                code="MISSING_FIELD",
                file=path.name,
                path=f"{sec_path}.type",
                message="Missing section type",
                severity="error"
            ))
            continue

        if "questions" not in sec or not isinstance(sec["questions"], list):
            errors.append(make_error(
                code="INVALID_FIELD",
                file=path.name,
                path=f"{sec_path}.questions",
                message="questions must be an array",
                severity="error"
            ))
            continue

        if not sec["questions"]:
            errors.append(make_error(
                code="EMPTY_QUESTIONS",
                file=path.name,
                path=f"{sec_path}.questions",
                message="Section has no questions",
                severity="warning"
            ))
            continue

        # -------------------------
        # DISPATCH BY TYPE
        # -------------------------
        rule = SECTION_RULES.get(sec_type)
        if not rule:
            errors.append(make_error(
                code="UNKNOWN_SECTION_TYPE",
                file=path.name,
                path=f"{sec_path}.type",
                message=f"Unsupported section type: {sec_type}",
                severity="error"
            ))
            continue

        errors.extend(rule.validate(sec, path.name, sec_path))

    return errors


# -------------------------
# PATH LEVEL
# -------------------------
def validate_path(path: Path):
    errors = []

    if path.is_file():
        errors.extend(validate_file(path))

    elif path.is_dir():
        exam_files = list(path.rglob("schema/exam.json"))

        if not exam_files:
            errors.append(make_error(
                code="NO_EXAM_FOUND",
                file="__collection__",
                path=str(path),
                message="No schema/exam.json found recursively"
            ))
            return errors

        for f in exam_files:
            errors.extend(validate_file(f))

        return errors


    else:
        errors.append(make_error(
            code="PATH_NOT_FOUND",
            file="__collection__",
            path="",
            message=f"Path not found: {path}",
            severity="error"
        ))

    return errors


# -------------------------
# CLI
# -------------------------
def main():
    if len(sys.argv) != 2:
        print("usage: exam_validate.py <path>")
        sys.exit(2)

    path = Path(sys.argv[1])
    errors = validate_path(path)

    valid = not any(e["severity"] == "error" for e in errors)

    print(json.dumps({
        "valid": valid,
        "errors": errors
    }, ensure_ascii=False, indent=2))

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
