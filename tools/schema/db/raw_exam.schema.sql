-- ===============================
-- RAW EXAM DATABASE SCHEMA
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
    -- RAW_NEW | VALIDATED | REJECTED | NORMALIZED | ARCHIVED

    schema_version TEXT NOT NULL,

    -- full original payload
    payload_json TEXT NOT NULL,

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
    -- CREATED | VALIDATED | ERROR | AI_REVISED | NORMALIZED

    event_message TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (raw_exam_uid)
        REFERENCES raw_exams(raw_exam_uid)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_raw_exam_events_uid
ON raw_exam_events(raw_exam_uid);
