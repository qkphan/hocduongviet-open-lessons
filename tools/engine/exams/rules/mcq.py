from errors import make_error


class MCQRule:
    def validate(self, section, filename, sec_path):
        errors = []
        seen_ids = set()

        for qi, q in enumerate(section["questions"]):
            q_path = f"{sec_path}.questions[{qi}]"

            if not isinstance(q, dict):
                errors.append(make_error(
                    code="INVALID_QUESTION",
                    file=filename,
                    path=q_path,
                    message="Question must be object",
                    severity="error"
                ))
                continue

            qid = q.get("id")
            if not qid:
                errors.append(make_error(
                    code="MISSING_FIELD",
                    file=filename,
                    path=f"{q_path}.id",
                    message="Missing question id",
                    severity="error"
                ))
            elif qid in seen_ids:
                errors.append(make_error(
                    code="DUPLICATE_ID",
                    file=filename,
                    path=f"{q_path}.id",
                    message=f"Duplicate question id: {qid}",
                    severity="error"
                ))
            else:
                seen_ids.add(qid)

            if "choices" not in q or not isinstance(q["choices"], list):
                errors.append(make_error(
                    code="INVALID_FIELD",
                    file=filename,
                    path=f"{q_path}.choices",
                    message="choices must be array",
                    severity="error"
                ))
                continue

            correct = [c for c in q["choices"] if c.get("correct") is True]
            if len(correct) != 1:
                errors.append(make_error(
                    code="INVALID_ANSWER",
                    file=filename,
                    path=f"{q_path}.choices",
                    message="MCQ must have exactly one correct choice",
                    severity="error"
                ))

        return errors
    
    def validate_mcq(sec, filename, sec_path):
        errors = []

        for qi, q in enumerate(sec["questions"]):
            qpath = f"{sec_path}.questions[{qi}]"

            # choices must be array of strings
            if not isinstance(q.get("choices"), list):
                errors.append(make_error(
                    code="INVALID_FIELD",
                    file=filename,
                    path=f"{qpath}.choices",
                    message="choices must be an array"
                ))
                continue

            if not all(isinstance(c, str) for c in q["choices"]):
                errors.append(make_error(
                    code="INVALID_FIELD",
                    file=filename,
                    path=f"{qpath}.choices",
                    message="each choice must be a string"
                ))

            # correct must be integer index
            correct = q.get("correct")
            if not isinstance(correct, int):
                errors.append(make_error(
                    code="INVALID_FIELD",
                    file=filename,
                    path=f"{qpath}.correct",
                    message="correct must be an integer index"
                ))
            elif not (0 <= correct < len(q["choices"])):
                errors.append(make_error(
                    code="OUT_OF_RANGE",
                    file=filename,
                    path=f"{qpath}.correct",
                    message="correct index out of range"
                ))

        return errors

