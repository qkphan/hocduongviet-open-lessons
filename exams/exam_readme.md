┌──────────────┐
│ GitHub Push  │
└──────┬───────┘
       ↓
┌──────────────────────────┐
│ GitHub Actions Workflow  │
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ examengine.py            │
│  - đọc schema            │
│  - đọc exam_data.json    │  ← AI sinh
│  - shuffle / seed        │
│  - sinh exam_data.tex    │
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ exam_layout.tex          │
│  - input preamble        │
│  - input exam_data.tex   │
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ pdflatex (latex-action)  │
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ builds/                  │
│  exam_A.pdf … exam_H.pdf │
└──────────────────────────┘
