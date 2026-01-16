import subprocess
import sys

MAX_ITER = 5

def run_exam_validate():
    """
    Run exam_validate.py.
    Return True if valid, False if invalid.
    """
    result = subprocess.run(
        [sys.executable, "exam_validate.py"],
        cwd="engine/exams",
        capture_output=True,
        text=True
    )
    return result.returncode == 0

for i in range(MAX_ITER):
    valid = run_exam_validate()
    if valid:
        print("✅ Exam fixed")
        break

    prompt = build_prompt(
        schema="exam_schema.json",
        invalid_json="exam.json",
        errors="validation_errors.json"
    )

    fixed_json = call_ai(prompt)
    save("exam.json", fixed_json)
else:
    raise RuntimeError("❌ AI failed to fix exam after max iterations")
