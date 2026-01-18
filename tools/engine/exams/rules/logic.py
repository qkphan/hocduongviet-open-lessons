def validate_logic(exam, file):
    errors = []

    questions = exam.get("questions", [])
    if isinstance(questions, list) and len(questions) == 0:
        errors.append(error(
            code="EMPTY_ARRAY",
            file=file,
            path="exam.questions",
            message="Exam must have at least one question",
            expected="non-empty array",
            actual=[]
        ))

    return errors
