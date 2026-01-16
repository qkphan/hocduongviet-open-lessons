import json
import os
from pathlib import Path
# from openai import OpenAI
import google.generativeai as genai

# =========================
# PATHS
# =========================
ROOT = Path(__file__).resolve().parents[2]

PROMPT_FILE = ROOT / "tools/prompt/exams/prompt_generate_exam.md"
SCHEMA_FILE = ROOT / "tools/schema/exams/exam_schema.json"
OUTPUT_JSON = Path(__file__).parent / "exam.json"

# =========================
# LOAD FILES
# =========================
prompt_template = PROMPT_FILE.read_text(encoding="utf-8")
schema_text = SCHEMA_FILE.read_text(encoding="utf-8")

prompt = prompt_template.replace("{{SCHEMA}}", schema_text)

# =========================
# OPENAI CLIENT
# =========================
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# =========================
# CALL AI
# =========================
response = client.chat.completions.create(
    # model="gpt-4.1",
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You generate exam JSON only."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

raw_output = response.choices[0].message.content.strip()

# =========================
# SAVE (NO VALIDATION HERE)
# =========================
try:
    data = json.loads(raw_output)
except json.JSONDecodeError as e:
    print("❌ AI output is not valid JSON")
    print(raw_output)
    raise e

OUTPUT_JSON.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"✅ exam.json generated at {OUTPUT_JSON}")
