-- ===============================
-- RAW EXAM DATABASE SCHEMA (v2 - pipeline aligned)
-- ===============================

PRAGMA foreign_keys = ON;

-- ===============================
-- TABLE: raw_exams
-- ===============================
CREATE TABLE IF NOT EXISTS raw_exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- business uid
    raw_exam_uid TEXT NOT NULL UNIQUE,

    -- source of ingestion
    source TEXT NOT NULL DEFAULT 'ui',
    -- ui | ai | import | api | pipeline

    -- lifecycle
    status TEXT NOT NULL,
    -- RAW_NEW
    -- VALIDATING
    -- NEEDS_REVISE
    -- PASSED
    -- FAILED_VALIDATE
    -- ABANDONED

    severity TEXT NOT NULL DEFAULT 'NONE',
    -- NONE | SOFT | HARD

    schema_version TEXT NOT NULL,

    -- revision control
    revision_count INTEGER NOT NULL DEFAULT 0,
    max_revision INTEGER NOT NULL DEFAULT 2,

    -- full original payload
    payload_json TEXT NOT NULL,

    -- timestamps
    created_at TEXT NOT NULL,
    updated_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_raw_exams_uid
ON raw_exams(raw_exam_uid);

CREATE INDEX IF NOT EXISTS idx_raw_exams_status
ON raw_exams(status);

-- ===============================
-- TABLE: raw_exam_events (audit log)
-- ===============================
CREATE TABLE IF NOT EXISTS raw_exam_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    raw_exam_uid TEXT NOT NULL,

    event_type TEXT NOT NULL,
    -- CREATED
    -- VALIDATING
    -- NEEDS_REVISE
    -- PASSED
    -- FAILED
    -- ABANDONED
    -- AI_REVISED

    event_message TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (raw_exam_uid)
        REFERENCES raw_exams(raw_exam_uid)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_raw_exam_events_uid
ON raw_exam_events(raw_exam_uid);

-- ===============================
-- TABLE: raw_exam_validation
-- ===============================
CREATE TABLE IF NOT EXISTS raw_exam_validation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    raw_exam_uid TEXT NOT NULL,
    revision_number INTEGER NOT NULL,

    validation_stage TEXT NOT NULL,
    -- schema | rule

    result TEXT NOT NULL,
    -- PASS | FAIL

    error_code TEXT,
    error_message TEXT,

    created_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (raw_exam_uid)
        REFERENCES raw_exams(raw_exam_uid)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_raw_exam_validation_uid
ON raw_exam_validation(raw_exam_uid);
