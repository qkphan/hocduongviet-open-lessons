import json
import sqlite3
import sys
import uuid
from datetime import datetime

RAW_DB = "data/raw_database.db"


def ingest(raw_exam_path, source="ui"):
    raw_exam_uid = f"raw_{uuid.uuid4().hex[:8]}"

    with open(raw_exam_path, encoding="utf-8") as f:
        payload = json.load(f)

    conn = sqlite3.connect(RAW_DB)

    conn.execute(
        """
        INSERT INTO raw_exams
        (raw_exam_uid, source, status, schema_version, payload_json, created_at)
        VALUES (?, ?, 'RAW_NEW', 'exam_schema_v1.0', ?, ?)
        """,
        (
            raw_exam_uid,
            source,
            json.dumps(payload, ensure_ascii=False),
            datetime.utcnow(),
        ),
    )

    conn.execute(
        """
        INSERT INTO raw_exam_events
        (raw_exam_uid, event_type, event_message)
        VALUES (?, 'CREATED', 'Raw exam ingested')
        """,
        (raw_exam_uid,),
    )

    conn.commit()
    conn.close()

    print(raw_exam_uid)  # IMPORTANT: output cho GitHub Actions


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest_raw_exam.py <raw_exam.json> [source]")
        sys.exit(1)

    ingest(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "ui")
