-- =====================================================
-- RAW EXAM INGEST DATABASE (SQLite)
-- =====================================================

PRAGMA foreign_keys = ON;

-- =====================================================
-- TABLE: raw_exams
-- =====================================================
CREATE TABLE IF NOT EXISTS raw_exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- UID bên ngoài (pipeline, GitHub Actions, AI)
    raw_exam_uid TEXT NOT NULL UNIQUE,

    -- JSON gốc sinh từ AI / UI
    payload_json TEXT NOT NULL,

    -- Versioning
    revision_count INTEGER NOT NULL DEFAULT 0,
    max_revision INTEGER NOT NULL DEFAULT 2,

    -- Validation state machine
    status TEXT NOT NULL DEFAULT 'NEW',
    severity TEXT DEFAULT 'NONE',

    -- Metadata nhẹ để filter nhanh (optional)
    schema_version TEXT,
    subject TEXT,
    grade INTEGER,

    -- Audit
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

-- =====================================================
-- TABLE: raw_exam_validation
-- =====================================================
CREATE TABLE IF NOT EXISTS raw_exam_validation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    raw_exam_uid TEXT NOT NULL,
    revision_number INTEGER NOT NULL,

    validation_stage TEXT NOT NULL,
    -- schema | rule | pedagogy | scoring

    result TEXT NOT NULL,
    -- PASS | FAIL

    error_code TEXT,
    error_message TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (raw_exam_uid)
        REFERENCES raw_exams(raw_exam_uid)
        ON DELETE CASCADE
);

-- =====================================================
-- TABLE: raw_exam_events
-- =====================================================
CREATE TABLE IF NOT EXISTS raw_exam_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    raw_exam_uid TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_message TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (raw_exam_uid)
        REFERENCES raw_exams(raw_exam_uid)
        ON DELETE CASCADE
);

-- =====================================================
-- INDEXES (performance + debug)
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_raw_exams_status
ON raw_exams(status);

CREATE INDEX IF NOT EXISTS idx_raw_exams_subject_grade
ON raw_exams(subject, grade);

CREATE INDEX IF NOT EXISTS idx_raw_exam_validation_uid
ON raw_exam_validation(raw_exam_uid);

CREATE INDEX IF NOT EXISTS idx_raw_exam_events_uid
ON raw_exam_events(raw_exam_uid);
