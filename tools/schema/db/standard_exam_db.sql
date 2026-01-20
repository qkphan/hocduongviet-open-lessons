PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- =====================================================
-- 1. EXAMS (METADATA)
-- =====================================================
CREATE TABLE exams (
    exam_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 12),
    duration INTEGER NOT NULL CHECK (duration >= 5),
    author TEXT,
    version TEXT,
    total_points REAL
);

-- =====================================================
-- 2. EXAM CONFIG
-- =====================================================
CREATE TABLE exam_config (
    exam_id TEXT PRIMARY KEY,
    shuffle_sections BOOLEAN DEFAULT 0,
    shuffle_questions BOOLEAN DEFAULT 0,
    shuffle_choices BOOLEAN DEFAULT 0,
    show_points BOOLEAN DEFAULT 1,
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE
);

-- =====================================================
-- 3. SECTIONS
-- =====================================================
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    exam_id TEXT NOT NULL,
    type TEXT NOT NULL CHECK (
        type IN ('mcq', 'tfq', 'short_answer', 'essay')
    ),
    title TEXT NOT NULL,
    description TEXT,
    position INTEGER,
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE
);

CREATE INDEX idx_sections_exam ON sections(exam_id);

-- =====================================================
-- 4. QUESTIONS (BASE)
-- =====================================================
CREATE TABLE questions (
    question_id TEXT PRIMARY KEY,
    section_id TEXT NOT NULL,
    type TEXT NOT NULL CHECK (
        type IN ('mcq', 'tfq', 'short_answer', 'essay')
    ),
    content TEXT NOT NULL,
    points REAL NOT NULL CHECK (points >= 0),
    content_domain TEXT,
    cognitive_level TEXT CHECK (
        cognitive_level IN (
            'remember',
            'understand',
            'apply',
            'analyze',
            'evaluate',
            'create'
        )
    ),
    FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE
);

CREATE INDEX idx_questions_section ON questions(section_id);

-- =====================================================
-- 5. MCQ CHOICES
-- =====================================================
CREATE TABLE choices (
    choice_id TEXT PRIMARY KEY,
    question_id TEXT NOT NULL,
    content TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

CREATE INDEX idx_choices_question ON choices(question_id);

-- =====================================================
-- 6. TRUE / FALSE SUB-QUESTIONS
-- =====================================================
CREATE TABLE sub_questions (
    sub_question_id TEXT PRIMARY KEY,
    question_id TEXT NOT NULL,
    content TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

CREATE INDEX idx_sub_questions_question ON sub_questions(question_id);

-- =====================================================
-- 7. SHORT ANSWER ACCEPTED ANSWERS
-- =====================================================
CREATE TABLE short_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

CREATE INDEX idx_short_answers_question ON short_answers(question_id);

-- =====================================================
-- 8. ESSAY RUBRIC CRITERIA
-- =====================================================
CREATE TABLE rubric_criteria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    description TEXT NOT NULL,
    points REAL NOT NULL CHECK (points >= 0),
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

CREATE INDEX idx_rubric_question ON rubric_criteria(question_id);

-- =====================================================
-- 9. EXAM CONTENT DOMAINS (M:N)
-- =====================================================
CREATE TABLE exam_domains (
    exam_id TEXT NOT NULL,
    domain TEXT NOT NULL,
    PRIMARY KEY (exam_id, domain),
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE
);

-- =====================================================
-- 10. EXAM TARGET COMPETENCIES (M:N)
-- =====================================================
CREATE TABLE exam_competencies (
    exam_id TEXT NOT NULL,
    competency TEXT NOT NULL,
    PRIMARY KEY (exam_id, competency),
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE
);

-- =====================================================
-- 11. EXAM COGNITIVE LEVELS (M:N)
-- =====================================================
CREATE TABLE exam_cognitive_levels (
    exam_id TEXT NOT NULL,
    cognitive_level TEXT NOT NULL CHECK (
        cognitive_level IN (
            'remember',
            'understand',
            'apply',
            'analyze',
            'evaluate',
            'create'
        )
    ),
    PRIMARY KEY (exam_id, cognitive_level),
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE
);

COMMIT;
