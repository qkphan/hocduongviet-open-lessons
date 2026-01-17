import json
import os
import sys
from pathlib import Path

from google import genai


# =========================
# ENV
# =========================
ENABLE_AI = os.getenv("ENABLE_AI", "0") == "1"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# =========================
# PATH SETUP
# =========================
ROOT = Path(__file__).resolve().parents[3]

SCHEMA_PATH = ROOT / "tools/schema/exams/exam.schema.json"
PROMPT_PATH = ROOT / "tools/prompt/exams/prompt_generate_exam.md"


# =========================
# FIND exam.json
# =========================
def find_exam_json():
    exams_dir = ROOT / "exams"
    candidates = list(exams_dir.rglob("exam.json"))

    if not candidates:
        print("❌ No exam.json found under exams/")
        sys.exit(1)

    if len(candidates) > 1:
        print("❌ Multiple exam.json found. Only one is allowed.")
        for c in candidates:
            print(" -", c)
        sys.exit(1)

    return candidates[0]


# =========================
# MAIN
# =========================
def main():
    exam_json_path = find_exam_json()

    print(f"📘 Target exam.json: {exam_json_path.relative_to(ROOT)}")

    if not ENABLE_AI:
        print("⏭️ ENABLE_AI=0 → Skip AI generation")
        return

    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY is missing")
        sys.exit(1)

    if not PROMPT_PATH.exists():
        print(f"❌ Prompt not found: {PROMPT_PATH}")
        sys.exit(1)

    if not SCHEMA_PATH.exists():
        print(f"❌ Schema not found: {SCHEMA_PATH}")
        sys.exit(1)

    # =========================
    # LOAD PROMPT + SCHEMA
    # =========================
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    schema_text = SCHEMA_PATH.read_text(encoding="utf-8")

    prompt = prompt_template.replace("{{SCHEMA}}", schema_text)

    print("🤖 Calling Gemini to generate exam.json...")

    # =========================
    # GEMINI CLIENT
    # =========================
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 4096
            }
        )
    except Exception as e:
        print("❌ Gemini API call failed")
        raise e

    raw_output = response.text.strip()

    print("🧠 RAW AI OUTPUT:")
    print(raw_output[:500] + ("..." if len(raw_output) > 500 else ""))
    print("")

    # =========================
    # PARSE JSON
    # =========================
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        print("❌ AI output is NOT valid JSON")
        sys.exit(1)

    # =========================
    # SAVE
    # =========================
    exam_json_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("✅ exam.json generated successfully")


if __name__ == "__main__":
    main()
