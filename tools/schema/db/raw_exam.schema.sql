-- =====================================================
-- RAW DATABASE SCHEMA
-- Purpose: Store raw / failed / revised exams
-- Engine: SQLite
-- =====================================================

PRAGMA foreign_keys = ON;

-- =====================================================
-- 1. RAW EXAMS (MAIN TABLE)
-- =====================================================
CREATE TABLE IF NOT EXISTS raw_exams (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,

    raw_exam_uid        TEXT NOT NULL UNIQUE,      -- raw_2026_01_17_001
    title               TEXT,
    subject             TEXT,                       -- toan, ly, hoa...
    grade               TEXT,                       -- lop10, lop11...
    chapter             TEXT,
    lesson              TEXT,

    source              TEXT NOT NULL,              -- ai | ui | raw_database
    author              TEXT,                       -- teacher / ai_model
    language            TEXT DEFAULT 'vi',

    status              TEXT NOT NULL,              -- RAW_NEW, VALIDATING, PASSED, FAILED, ABANDONED, ARCHIVED
    severity            TEXT,                       -- NONE, SOFT, HARD

    revision_count      INTEGER DEFAULT 0,
    max_revision        INTEGER DEFAULT 2,

    schema_version      TEXT NOT NULL,              -- exam_schema_v1.0
    validated_exam_uid  TEXT,                       -- link sang school.db

    payload_json        TEXT NOT NULL,              -- raw_exam.json (FULL)

    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_raw_exams_status
ON raw_exams(status);

CREATE INDEX IF NOT EXISTS idx_raw_exams_source
ON raw_exams(source);

-- =====================================================
-- 2. RAW EXAM REVISIONS (VERSIONING)
-- =====================================================
CREATE TABLE IF NOT EXISTS raw_exam_revisions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,

    raw_exam_uid        TEXT NOT NULL,
    revision_number     INTEGER NOT NULL,

    revised_by          TEXT,                       -- ai | user | system
    revision_note       TEXT,

    payload_json        TEXT NOT NULL,

    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (raw_exam_uid)
        REFERENCES raw_exams(raw_exam_uid)
        ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_revision_unique
ON raw_exam_revisions(raw_exam_uid, revision_number);

-- =====================================================
-- 3. VALIDATION RESULTS
-- =====================================================
CREATE TABLE IF NOT EXISTS raw_exam_validation (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,

    raw_exam_uid        TEXT NOT NULL,
    revision_number     INTEGER NOT NULL,

    validation_stage    TEXT NOT NULL,              -- schema | rule | pedagogy
    result              TEXT NOT NULL,              -- PASS | FAIL

    error_code          TEXT,                       -- SCHEMA_MISSING_FIELD
    error_message       TEXT,

    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (raw_exam_uid)
        REFERENCES raw_exams(raw_exam_uid)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_validation_exam
ON raw_exam_validation(raw_exam_uid);

-- =====================================================
-- 4. RAW EXAM EVENTS (AUDIT LOG)
-- =====================================================
CREATE TABLE IF NOT EXISTS raw_exam_events (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,

    raw_exam_uid        TEXT NOT NULL,
    event_type          TEXT NOT NULL,              -- CREATED, VALIDATED, REVISED, ARCHIVED, ABANDONED
    event_message       TEXT,

    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (raw_exam_uid)
        REFERENCES raw_exams(raw_exam_uid)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_events_exam
ON raw_exam_events(raw_exam_uid);

-- =====================================================
-- END OF SCHEMA

-- =====================================================
