-- ===============================
-- school.db schema
-- ===============================

PRAGMA foreign_keys = ON;

-- ===============================
-- 1. Exams
-- ===============================
CREATE TABLE exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 12),
    lesson_code TEXT NOT NULL,
    duration INTEGER NOT NULL CHECK (duration >= 5),

    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 2. Questions
-- ===============================
CREATE TABLE questions (
    id TEXT PRIMARY KEY,           -- ví dụ: Q1, Q2...
    exam_id INTEGER NOT NULL,

    type TEXT NOT NULL CHECK (
        type IN ('mcq', 'tfq', 'shortAns', 'essayq', 'advanceessq')
    ),

    content TEXT NOT NULL,

    difficulty TEXT NOT NULL CHECK (
        difficulty IN ('easy', 'medium', 'hard')
    ),

    cognitive_level TEXT CHECK (
        cognitive_level IN (
            'remember',
            'understand',
            'apply',
            'analyze',
            'evaluate'
        )
    ),

    score REAL NOT NULL CHECK (score >= 0),

    answer_key TEXT,     -- cho mcq, tfq, shortAns
    explanation TEXT,    -- giải thích
    rubric TEXT,         -- cho essay / advanceessq

    FOREIGN KEY (exam_id)
        REFERENCES exams(id)
        ON DELETE CASCADE
);

-- ===============================
-- 3. Choices (MCQ / TFQ)
-- ===============================
CREATE TABLE choices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    question_id TEXT NOT NULL,

    label TEXT NOT NULL CHECK (
        label GLOB '[A-Z]' OR label IN ('True', 'False')
    ),

    content TEXT NOT NULL,
    is_correct INTEGER NOT NULL CHECK (is_correct IN (0, 1)),

    FOREIGN KEY (question_id)
        REFERENCES questions(id)
        ON DELETE CASCADE
);

-- ===============================
-- 4. Indexes (tối ưu)
-- ===============================
CREATE INDEX idx_questions_exam
    ON questions(exam_id);

CREATE INDEX idx_choices_question
    ON choices(question_id);
