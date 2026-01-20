import json
import sqlite3
import sys
from datetime import datetime
from jsonschema import validate, ValidationError

# =====================================================
# CONFIG
# =====================================================
RAW_DB_PATH = "data/raw_database.db"
EXAM_SCHEMA_PATH = "tools/schema/exams/raw_exam.schema.json"

MAX_REVISION_DEFAULT = 2

# =====================================================
# DB UTILS
# =====================================================
def get_db():
    return sqlite3.connect(RAW_DB_PATH)


def log_event(conn, raw_exam_uid, event_type, message=""):
    conn.execute(
        """
        INSERT INTO raw_exam_events (raw_exam_uid, event_type, event_message)
        VALUES (?, ?, ?)
        """,
        (raw_exam_uid, event_type, message),
    )


def save_validation_result(
    conn,
    raw_exam_uid,
    revision_number,
    stage,
    result,
    error_code=None,
    error_message=None,
):
    conn.execute(
        """
        INSERT INTO raw_exam_validation
        (raw_exam_uid, revision_number, validation_stage, result, error_code, error_message)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            raw_exam_uid,
            revision_number,
            stage,
            result,
            error_code,
            error_message,
        ),
    )


# =====================================================
# LOADERS
# =====================================================
def load_schema():
    with open(EXAM_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_raw_exam(conn, raw_exam_uid):
    cur = conn.execute(
        """
        SELECT payload_json, revision_count, max_revision
        FROM raw_exams
        WHERE raw_exam_uid = ?
        """,
        (raw_exam_uid,),
    )
    row = cur.fetchone()
    if not row:
        raise ValueError(f"Raw exam not found: {raw_exam_uid}")

    payload_json, revision_count, max_revision = row
    return json.loads(payload_json), revision_count, max_revision


# =====================================================
# VALIDATORS
# =====================================================
def schema_validate_exam(exam_json, schema):
    try:
        validate(instance=exam_json, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)


def rule_validate_exam(exam_json):
    """
    Hard-coded rule validation (step 2.2)
    Return: (pass: bool, severity: SOFT|HARD, message)
    """

    errors = []

    sections = exam_json.get("sections", [])

    if not sections:
        return False, "HARD", "No sections defined"

    for sec in sections:
        sec_type = sec.get("type")
        questions = sec.get("questions", [])

        if not questions:
            errors.append(f"Empty section: {sec_type}")

        if sec_type == "mcq":
            for q in questions:
                choices = q.get("choices", [])
                correct = [c for c in choices if c.get("is_correct")]

                if len(correct) != 1:
                    errors.append(
                        f"MCQ must have exactly 1 correct answer: {q.get('id')}"
                    )

    if not errors:
        return True, None, None

    # Severity heuristic
    if any("exactly 1 correct" in e for e in errors):
        return False, "SOFT", "; ".join(errors)

    return False, "HARD", "; ".join(errors)


# =====================================================
# MAIN PIPELINE
# =====================================================
def validate_pipeline(raw_exam_uid):
    conn = get_db()
    conn.row_factory = sqlite3.Row

    try:
        exam_json, revision_count, max_revision = load_raw_exam(conn, raw_exam_uid)
        schema = load_schema()

        log_event(conn, raw_exam_uid, "VALIDATING", "Start validation")

        # -------------------------------
        # 1. SCHEMA VALIDATION
        # -------------------------------
        schema_ok, schema_error = schema_validate_exam(exam_json, schema)

        if not schema_ok:
            save_validation_result(
                conn,
                raw_exam_uid,
                revision_count,
                "schema",
                "FAIL",
                "SCHEMA_ERROR",
                schema_error,
            )

            conn.execute(
                """
                UPDATE raw_exams
                SET status = 'FAILED_VALIDATE', severity = 'HARD'
                WHERE raw_exam_uid = ?
                """,
                (raw_exam_uid,),
            )

            log_event(conn, raw_exam_uid, "FAILED", "Schema validation failed")
            conn.commit()
            return "FAIL_HARD"

        save_validation_result(
            conn,
            raw_exam_uid,
            revision_count,
            "schema",
            "PASS",
        )

        # -------------------------------
        # 2. RULE VALIDATION
        # -------------------------------
        rule_ok, severity, rule_error = rule_validate_exam(exam_json)

        if not rule_ok:
            save_validation_result(
                conn,
                raw_exam_uid,
                revision_count,
                "rule",
                "FAIL",
                "RULE_ERROR",
                rule_error,
            )

            if severity == "SOFT" and revision_count < max_revision:
                conn.execute(
                    """
                    UPDATE raw_exams
                    SET status = 'NEEDS_REVISE',
                        severity = 'SOFT'
                    WHERE raw_exam_uid = ?
                    """,
                    (raw_exam_uid,),
                )

                log_event(
                    conn,
                    raw_exam_uid,
                    "NEEDS_REVISE",
                    "Rule validation failed (soft)",
                )
                conn.commit()
                return "FAIL_SOFT"

            else:
                conn.execute(
                    """
                    UPDATE raw_exams
                    SET status = 'ABANDONED',
                        severity = 'HARD'
                    WHERE raw_exam_uid = ?
                    """,
                    (raw_exam_uid,),
                )

                log_event(
                    conn,
                    raw_exam_uid,
                    "ABANDONED",
                    "Rule validation failed (hard)",
                )
                conn.commit()
                return "FAIL_HARD"

        save_validation_result(
            conn,
            raw_exam_uid,
            revision_count,
            "rule",
            "PASS",
        )

        # -------------------------------
        # 3. PASSED
        # -------------------------------
        conn.execute(
            """
            UPDATE raw_exams
            SET status = 'PASSED',
                severity = 'NONE',
                updated_at = ?
            WHERE raw_exam_uid = ?
            """,
            (datetime.utcnow(), raw_exam_uid),
        )

        log_event(conn, raw_exam_uid, "PASSED", "Exam validated successfully")
        conn.commit()
        return "PASS"

    finally:
        conn.close()


# =====================================================
# CLI
# =====================================================
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python exam_validate.py <raw_exam_uid>")
        sys.exit(1)

    raw_exam_uid = sys.argv[1]
    result = validate_pipeline(raw_exam_uid)
    print(f"[VALIDATION RESULT] {raw_exam_uid}: {result}")
