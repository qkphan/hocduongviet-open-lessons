import json
import os
from pathlib import Path
from google import genai

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
# GEMINI CLIENT
# =========================
# client = genai.Client(
#     api_key=os.environ["GEMINI_API_KEY"]
# )
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# CALL AI (GEMINI)
# =========================
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents=prompt
# )
response = model.generate_content(prompt)
raw_output = response.text.strip()

print("===== RAW AI OUTPUT =====")
print(raw_output)
print("=========================")

# =========================
# PARSE JSON
# =========================
try:
    data = json.loads(raw_output)
except json.JSONDecodeError as e:
    print("❌ AI output is not valid JSON")
    raise e

# =========================
# SAVE
# =========================
OUTPUT_JSON.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"✅ exam.json generated at {OUTPUT_JSON}")
