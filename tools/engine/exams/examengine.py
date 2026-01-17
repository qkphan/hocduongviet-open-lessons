#!/usr/bin/env python3
"""
examengine.py
----------------
Compiler: Exam JSON  -> exam_data.tex
ROLE: DATA → TEX (NO layout, NO styling)
"""

import json
import os
from pathlib import Path

# ==============================
# CONFIG
# ==============================
ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "tools" / "schema" / "exams"
EXAM_JSON = ROOT / "exam.json"
OUTPUT_TEX = ROOT / "exam_data.tex"

# ==============================
# HELPERS
# ==============================

def tex_escape(s: str) -> str:
    """Escape minimal LaTeX special chars."""
    if s is None:
        return ""
    return (
        s.replace("\\", "\\textbackslash{}").replace("%", "\\%")
         .replace("&", "\\&").replace("_", "\\_")
         .replace("#", "\\#").replace("$", "\\$")
    )


def w(f, line=""):
    f.write(line + "\n")

# ==============================
# META → TEX
# ==============================

def emit_meta(f, meta: dict):
    w(f, "% ===== META =====")
    for k, v in meta.items():
        cmd = f"\\newcommand\\Exam{ k.capitalize() }{{{tex_escape(v)}}}"
        w(f, cmd)
    w(f)

# ==============================
# SECTIONS
# ==============================

def emit_mcq(f, q):
    w(f, f"\\begin{{examquestion}}{{{q['correct'] + 1}}}")
    w(f, f"  \\questiontext{{{tex_escape(q['content'])}}}")
    for c in q['choices']:
        w(f, f"  \\smartanswer{{{tex_escape(c)}}}")
    w(f, "\\end{examquestion}")
    w(f)


def emit_true_false(f, q):
    w(f, f"\\paragraph*{{Câu {q['id']}.}} {tex_escape(q['stem'])}")
    for i, stmt in enumerate(q['statements']):
        ans = "Đúng" if q['answers'][i] else "Sai"
        w(f, f"({chr(97+i)}) {tex_escape(stmt)}\\hfill [{ans}]")
    w(f, "\\medskip")


def emit_short_answer(f, q):
    w(f, f"\\paragraph*{{Câu {q['id']}.}} {tex_escape(q['stem'])}")
    for i, sub in enumerate(q['subquestions'], 1):
        w(f, f"({i}) {tex_escape(sub)}\\\\")
    w(f, "\\medskip")


def emit_essay(f, q):
    w(f, f"\\paragraph*{{Câu {q['id']}.}} {tex_escape(q['content'])}")
    w(f, "\\vspace{4cm}")
    w(f)


def emit_advanced_essay(f, q):
    w(f, f"\\paragraph*{{Câu {q['id']}.}} {tex_escape(q['content'])}")
    for i, part in enumerate(q['parts'], 1):
        w(f, f"({i}) {tex_escape(part)}\\\\")
    w(f, "\\vspace{4cm}")
    w(f)

# ==============================
# MAIN
# ==============================

def main():
    if not EXAM_JSON.exists():
        raise FileNotFoundError("exam.json not found")

    with open(EXAM_JSON, encoding="utf-8") as f:
        data = json.load(f)

    with open(OUTPUT_TEX, "w", encoding="utf-8") as f:
        w(f, "% AUTO-GENERATED — DO NOT EDIT")
        w(f)

        emit_meta(f, data['meta'])

        for sec in data['sections']:
            w(f, f"\\section*{{{tex_escape(sec['title'])}}}")

            for q in sec['questions']:
                t = sec['type']
                if t == "multiple_choice":
                    emit_mcq(f, q)
                elif t == "true_false":
                    emit_true_false(f, q)
                elif t == "short_answer":
                    emit_short_answer(f, q)
                elif t == "essay":
                    emit_essay(f, q)
                elif t == "advanced_essay":
                    emit_advanced_essay(f, q)
                else:
                    raise ValueError(f"Unknown question type: {t}")

    print("✅ exam_data.tex generated")


if __name__ == "__main__":
    main()
