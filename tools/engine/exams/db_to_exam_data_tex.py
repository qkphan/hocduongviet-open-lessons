import sqlite3
from pathlib import Path

DB_PATH = "school.db"
OUT_TEX = Path("exam_data.tex")

LABELS = ["A", "B", "C", "D"]

def tex_escape(s: str) -> str:
    if not s:
        return ""
    return s.replace("&", r"\&")

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT question_id, content, type, answer, explanation
        FROM questions
        ORDER BY id
    """)
    questions = cur.fetchall()

    tex = []
    tex.append("% AUTO-GENERATED FROM school.db")
    tex.append("\\begin{enumerate}")

    for qid, content, qtype, answer, explanation in questions:
        tex.append("")
        tex.append(f"\\item {content}")

        # ===== MCQ / TFQ =====
        if qtype in ("mcq", "tfq"):
            cur.execute("""
                SELECT choice_index, content
                FROM choices
                WHERE question_id = ?
                ORDER BY choice_index
            """, (qid,))
            choices = cur.fetchall()

            tex.append("\\begin{choices}")
            for idx, c in choices:
                if answer == idx:
                    tex.append(f"  \\item[\\textbf{{{LABELS[idx-1]}.}}] {c}")
                else:
                    tex.append(f"  \\item {c}")
            tex.append("\\end{choices}")

        # ===== Short answer =====
        elif qtype == "shortAns":
            tex.append("\\shortanswer{}")

        # ===== Essay =====
        elif qtype in ("essayq", "advanceessq"):
            tex.append("\\essay{}")

        # ===== Explanation =====
        if explanation:
            tex.append(f"\\loigiai{{{explanation}}}")

    tex.append("\\end{enumerate}")

    OUT_TEX.write_text("\n".join(tex), encoding="utf-8")
    conn.close()

    print("✅ Generated exam_data.tex from DB")

if __name__ == "__main__":
    main()
