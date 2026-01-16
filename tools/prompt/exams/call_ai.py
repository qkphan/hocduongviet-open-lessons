# import json
# from openai import OpenAI

# client = OpenAI()

# resp = client.responses.create(
#     # model="gpt-4.1-mini",
#     model="gemini-2.5-flash",
#     input="Generate 10 questions..."
# )

# text = resp.output_text
# with open("ai_raw.json", "w", encoding="utf8") as f:
#     f.write(text)

from openai import OpenAI
from pathlib import Path

client = OpenAI()

prompt = Path("tools/prompt/generate_exam.prompt.txt").read_text()
prompt = prompt.replace("{{N}}", "10")

resp = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

Path("ai_raw.json").write_text(resp.output_text, encoding="utf8")
