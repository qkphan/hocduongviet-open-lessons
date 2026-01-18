from errors import make_error

def validate_mcq(sec, filename, sec_path):
    errors = []

    questions = sec.get("questions", [])

    for qi, q in enumerate(questions):
        qpath = f"{sec_path}.questions[{qi}]"

        # --- content ---
        if not isinstance(q.get("content"), str):
            errors.append(make_error(
                code="INVALID_FIELD",
                file=filename,
                path=f"{qpath}.content",
                message="content must be a string"
            ))

        # --- choices ---
        choices = q.get("choices")
        if not isinstance(choices, list):
            errors.append(make_error(
                code="INVALID_FIELD",
                file=filename,
                path=f"{qpath}.choices",
                message="choices must be an array of strings"
            ))
            continue

        if len(choices) < 2:
            errors.append(make_error(
                code="INVALID_FIELD",
                file=filename,
                path=f"{qpath}.choices",
                message="must have at least 2 choices"
            ))

        for ci, c in enumerate(choices):
            if not isinstance(c, str):
                errors.append(make_error(
                    code="INVALID_FIELD",
                    file=filename,
                    path=f"{qpath}.choices[{ci}]",
                    message="each choice must be a string"
                ))

        # --- correct index ---
        correct = q.get("correct")
        if not isinstance(correct, int):
            errors.append(make_error(
                code="INVALID_FIELD",
                file=filename,
                path=f"{qpath}.correct",
                message="correct must be an integer index"
            ))
        elif not (0 <= correct < len(choices)):
            errors.append(make_error(
                code="OUT_OF_RANGE",
                file=filename,
                path=f"{qpath}.correct",
                message="correct index out of range"
            ))

    return errors
