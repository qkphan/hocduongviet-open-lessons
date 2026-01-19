import json
import sqlite3
from pathlib import Path

DB_PATH = "school.db"
EXAM_DIR = Path("data/exams")

def connect_db():
    return sqlite3.connect(DB_PATH)

def import_exam(json_path: Path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    meta = data.get("metadata", {})
    questions = data.get("questions", [])

    conn = connect_db()
    cur = conn.cursor()

    # insert exam
    cur.execute("""
        INSERT INTO exams (
            exam_id, version, created_by, source, license,
            json_source, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        meta.get("exam_id"),
        meta.get("version"),
        meta.get("created_by"),
        meta.get("source"),
        meta.get("license"),
        json_path.name,
        json.dumps(data, ensure_ascii=False)
    ))

    # insert questions
    for q in questions:
        cur.execute("""
            INSERT INTO questions (
                exam_id, question_id, content,
                type, difficulty, answer, explanation
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            meta.get("exam_id"),
            q.get("id"),
            q.get("content"),
            q.get("type"),
            q.get("difficulty"),
            q.get("answer"),
            q.get("explanation")
        ))

        # insert choices
        for idx, choice in enumerate(q.get("choices", []), start=1):
            cur.execute("""
                INSERT INTO choices (
                    question_id, choice_index, content
                ) VALUES (?, ?, ?)
            """, (
                q.get("id"),
                idx,
                choice
            ))

    conn.commit()
    conn.close()
    print(f"✅ Imported: {json_path.name}")

def main():
    files = list(EXAM_DIR.glob("exam.*.json"))

    if not files:
        print("⚠️ No exam JSON files found")
        return

    for json_file in files:
        import_exam(json_file)

if __name__ == "__main__":
    main()
