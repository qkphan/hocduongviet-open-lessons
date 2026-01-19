def make_error(
    *,
    code,
    file,
    path,
    message,
    expected=None,
    actual=None,
    severity="error"
):
    return {
        "code": code,
        "file": file,
        "path": path,
        "message": message,
        "expected": expected,
        "actual": actual,
        "severity": severity
    }
