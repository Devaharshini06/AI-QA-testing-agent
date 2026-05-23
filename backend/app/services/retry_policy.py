def decide_retry(evaluation):

    if evaluation["status"] == "failure":

        return {
            "retry": True,
            "reason": "Failure detected"
        }

    if evaluation["status"] == "unknown":

        return {
            "retry": True,
            "reason": "Unknown state"
        }

    return {
        "retry": False,
        "reason": "Execution successful"
    }