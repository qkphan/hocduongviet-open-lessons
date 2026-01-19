import json
import sqlite3
import sys
from datetime import datetime

RAW_DB_PATH = "data/raw_database.db"


def get_db():
    return sqlite3.connect(RAW_DB_PATH)


def load_raw_exam(conn, raw_exam_uid):
    cur = conn.execute(
        """
        SELECT payload_json, revision_count
        FROM raw_exams
        WHERE raw_exam_uid = ?
        """,
        (raw_exam_uid,),
    )
    row = cur.fetchone()
    if not row:
        raise ValueError("Raw exam not found")

    return json.loads(row[0]), row[1]


def simple_auto_revise(exam_json):
    """
    Placeholder AI revise
    (sau này thay bằng Gemini / GPT)
    """
    for sec in exam_json.get("sections", []):
        if sec.get("type") == "mcq":
            for q in sec.get("questions", []):
                choices = q.get("choices", [])
                correct = [c for c in choices if c.get("is_correct")]
                if len(correct) == 0 and choices:
                    choices[0]["is_correct"] = True
    return exam_json


def revise(raw_exam_uid):
    conn = get_db()
    try:
        exam_json, revision_count = load_raw_exam(conn, raw_exam_uid)
        new_revision = revision_count + 1

        revised_exam = simple_auto_revise(exam_json)

        conn.execute(
            """
            INSERT INTO raw_exam_revisions
            (raw_exam_uid, revision_number, revised_by, payload_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                raw_exam_uid,
                new_revision,
                "system_ai",
                json.dumps(revised_exam, ensure_ascii=False),
            ),
        )

        conn.execute(
            """
            UPDATE raw_exams
            SET payload_json = ?,
                revision_count = ?,
                status = 'RAW_NEW',
                updated_at = ?
            WHERE raw_exam_uid = ?
            """,
            (
                json.dumps(revised_exam, ensure_ascii=False),
                new_revision,
                datetime.utcnow(),
                raw_exam_uid,
            ),
        )

        conn.execute(
            """
            INSERT INTO raw_exam_events
            (raw_exam_uid, event_type, event_message)
            VALUES (?, 'REVISED', 'Auto revised')
            """,
            (raw_exam_uid,),
        )

        conn.commit()
        print(f"[REVISED] {raw_exam_uid} → revision {new_revision}")

    finally:
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python exam_revise.py <raw_exam_uid>")
        sys.exit(1)

    revise(sys.argv[1])
