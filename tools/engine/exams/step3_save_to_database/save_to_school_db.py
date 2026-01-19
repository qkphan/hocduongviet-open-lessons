import json
import sqlite3
import sys

RAW_DB = "data/raw_database.db"
SCHOOL_DB = "data/school.db"


def save_exam(raw_exam_uid):
    raw_conn = sqlite3.connect(RAW_DB)
    school_conn = sqlite3.connect(SCHOOL_DB)

    try:
        cur = raw_conn.execute(
            """
            SELECT payload_json
            FROM raw_exams
            WHERE raw_exam_uid = ? AND status = 'PASSED'
            """,
            (raw_exam_uid,),
        )
        row = cur.fetchone()
        if not row:
            raise ValueError("Exam not PASSED")

        exam = json.loads(row[0])
        exam_uid = exam["exam_id"]

        school_conn.execute(
            """
            INSERT INTO exams (exam_uid, title, subject, grade, metadata_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                exam_uid,
                exam.get("title"),
                exam.get("subject"),
                exam.get("grade"),
                json.dumps(exam.get("metadata", {}), ensure_ascii=False),
            ),
        )

        for sec in exam["sections"]:
            for q in sec["questions"]:
                q_cur = school_conn.execute(
                    """
                    INSERT INTO questions
                    (exam_uid, section_type, question_text, difficulty, skill)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        exam_uid,
                        sec["type"],
                        q["content"],
                        q.get("difficulty"),
                        q.get("skill"),
                    ),
                )
                q_id = q_cur.lastrowid

                for c in q.get("choices", []):
                    school_conn.execute(
                        """
                        INSERT INTO choices
                        (question_id, content, is_correct)
                        VALUES (?, ?, ?)
                        """,
                        (q_id, c["content"], c.get("is_correct", False)),
                    )

        school_conn.commit()
        raw_conn.execute(
            """
            UPDATE raw_exams
            SET validated_exam_uid = ?
            WHERE raw_exam_uid = ?
            """,
            (exam_uid, raw_exam_uid),
        )
        raw_conn.commit()

        print(f"[SAVED] {exam_uid} → school.db")

    finally:
        raw_conn.close()
        school_conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python save_to_school_db.py <raw_exam_uid>")
        sys.exit(1)

    save_exam(sys.argv[1])
