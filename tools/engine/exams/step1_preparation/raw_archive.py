def archive_raw_exam(json_path, source):
    raw_exam = load_json(json_path)

    if "raw_exam_uid" not in raw_exam:
        raw_exam_uid = generate_raw_exam_uid(raw_exam)
        raw_exam["raw_exam_uid"] = raw_exam_uid
    else:
        raw_exam_uid = raw_exam["raw_exam_uid"]

    insert_into_raw_database(
        raw_exam_uid=raw_exam_uid,
        subject=raw_exam["metadata"]["subject"],
        grade=raw_exam["metadata"]["grade"],
        source=source,
        payload=raw_exam
    )

    return raw_exam_uid
