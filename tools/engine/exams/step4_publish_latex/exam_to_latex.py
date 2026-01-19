import sqlite3
import sys
from pathlib import Path

SCHOOL_DB = "data/school.db"
OUTPUT_DIR = "exams/export"


def export_exam(exam_uid):
    conn = sqlite3.connect(SCHOOL_DB)
    cur = conn.execute(
        "SELECT title FROM exams WHERE exam_uid = ?", (exam_uid,)
    )
    exam = cur.fetchone()
    if not exam:
        raise ValueError("Exam not found")

    title = exam[0]
    out = Path(OUTPUT_DIR)
    out.mkdir(parents=True, exist_ok=True)

    tex = [r"\documentclass{article}", r"\begin{document}", f"\\section*{{{title}}}"]

    q_cur = conn.execute(
        """
        SELECT id, section_type, question_text
        FROM questions
        WHERE exam_uid = ?
        """,
        (exam_uid,),
    )

    for q_id, sec, text in q_cur.fetchall():
        tex.append(r"\subsection*{" + sec + "}")
        tex.append(text)

        c_cur = conn.execute(
            "SELECT content FROM choices WHERE question_id = ?", (q_id,)
        )
        choices = c_cur.fetchall()
        if choices:
            tex.append(r"\begin{itemize}")
            for c in choices:
                tex.append(r"\item " + c[0])
            tex.append(r"\end{itemize}")

    tex.append(r"\end{document}")

    tex_path = out / f"{exam_uid}.tex"
    tex_path.write_text("\n".join(tex), encoding="utf-8")
    print(f"[LATEX] {tex_path}")

    conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python exam_to_latex.py <exam_uid>")
        sys.exit(1)

    export_exam(sys.argv[1])
