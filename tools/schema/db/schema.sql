PRAGMA foreign_keys = ON;

-- ===== exams =====
CREATE TABLE exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL,
    lesson_code TEXT NOT NULL,
    duration INTEGER NOT NULL,
    version TEXT,
    source TEXT,
    created_at TEXT
);

-- ===== questions =====
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER NOT NULL,
    qid TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    difficulty TEXT,
    cognitive_level TEXT,
    score REAL,
    answer_key TEXT,
    explanation TEXT,
    rubric TEXT,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
);

-- ===== choices =====
CREATE TABLE choices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    label TEXT NOT NULL,
    content TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
