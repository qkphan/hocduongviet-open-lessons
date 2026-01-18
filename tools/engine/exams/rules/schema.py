def validate_schema(exam, file):
    errors = []

    if "title" not in exam:
        errors.append(error(
            code="MISSING_FIELD",
            file=file,
            path="exam.title",
            message="Missing field: title",
            expected="string",
            actual=None
        ))

    if "questions" in exam and not isinstance(exam["questions"], list):
        errors.append(error(
            code="INVALID_TYPE",
            file=file,
            path="exam.questions",
            message="questions must be an array",
            expected="array",
            actual=type(exam["questions"]).__name__
        ))

    return errors
