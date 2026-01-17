import json
import sqlite3
from pathlib import Path

DB_PATH = "school.db"
EXPORT_DIR = Path("data/export")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

LABELS = ["A", "B", "C", "D"]

def connect_db():
    return sqlite3.connect(DB_PATH)

def export_exam(exam_id: str):
    conn = connect_db()
    cur = conn.cursor()

    # ===== 1. Load exam + raw_json =====
    cur.execute("""
        SELECT raw_json FROM exams
        WHERE exam_id = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (exam_id,))
    row = cur.fetchone()
    if not row:
        raise ValueError(f"Exam {exam_id} not found")

    raw = json.loads(row[0])
    exam_meta = raw.get("exam", raw.get("metadata", {}))

    # ===== 2. Load questions =====
    cur.execute("""
        SELECT question_id, content, type, difficulty,
               answer, explanation
        FROM questions
        WHERE exam_id = ?
        ORDER BY id
    """, (exam_id,))
    questions_db = cur.fetchall()

    questions = []

    for qid, content, qtype, difficulty, answer, explanation in questions_db:
        q = {
            "id": qid,
            "type": qtype,
            "content": content,
            "difficulty": difficulty,
            "choices": [],
            "explanation": explanation
        }

        # ===== 3. Choices =====
        cur.execute("""
            SELECT choice_index, content
            FROM choices
            WHERE question_id = ?
            ORDER BY choice_index
        """, (qid,))
        choices_db = cur.fetchall()

        for idx, c in choices_db:
            label = LABELS[idx - 1]
            q["choices"].append({
                "label": label,
                "content": c,
                "is_correct": idx == answer
            })

        # ===== 4. Answer key =====
        if answer:
            q["answer_key"] = LABELS[answer - 1]

        questions.append(q)

    conn.close()

    # ===== 5. Build export JSON =====
    export = {
        "exam": {
            "title": exam_meta.get("title"),
            "subject": exam_meta.get("subject"),
            "grade": exam_meta.get("grade"),
            "lesson_code": exam_meta.get("lesson_code"),
            "duration": exam_meta.get("duration"),
            "questions": questions
        }
    }

    out_file = EXPORT_DIR / f"{exam_id}.export.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)

    print(f"📤 Exported → {out_file}")

def main():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT exam_id FROM exams")
    exam_ids = [r[0] for r in cur.fetchall()]
    conn.close()

    for eid in exam_ids:
        export_exam(eid)

if __name__ == "__main__":
    main()
