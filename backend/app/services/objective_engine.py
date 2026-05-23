def determine_next_goal(observation):

    # Not logged in yet
    if observation["has_login_button"]:

        return "login"

    # Logged in successfully
    if observation["has_cart"]:

        return "shopping"

    return "unknown"