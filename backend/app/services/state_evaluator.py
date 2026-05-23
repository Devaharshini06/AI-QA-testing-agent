def evaluate_state(observation):

    # Login success
    if (
        observation["has_cart"]
        and not observation["has_login_button"]
    ):

        return {
            "status": "success",
            "reason": "Login successful"
        }

    # Login failure
    if observation["has_error_message"]:

        return {
            "status": "failure",
            "reason": "Login error detected"
        }

    # Unknown state
    return {
        "status": "unknown",
        "reason": "Unable to determine state"
    }