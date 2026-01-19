PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_uid TEXT UNIQUE NOT NULL,
    title TEXT,
    subject TEXT,
    grade TEXT,
    metadata_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_uid TEXT NOT NULL,
    section_type TEXT,
    question_text TEXT,
    difficulty TEXT,
    skill TEXT,
    FOREIGN KEY (exam_uid) REFERENCES exams(exam_uid)
);

CREATE TABLE IF NOT EXISTS choices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    content TEXT,
    is_correct BOOLEAN,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
