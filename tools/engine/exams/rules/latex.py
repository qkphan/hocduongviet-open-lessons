import re

LATEX_PATTERN = re.compile(r"\$.*?\$")

def validate_latex(exam, file):
    errors = []

    for i, q in enumerate(exam.get("questions", [])):
        content = q.get("content", "")
        if "$" in content and not LATEX_PATTERN.search(content):
            errors.append(error(
                code="LATEX_PARSE_ERROR",
                file=file,
                path=f"exam.questions[{i}].content",
                message="Invalid LaTeX expression",
                expected="Valid LaTeX between $...$",
                actual=content
            ))

    return errors
