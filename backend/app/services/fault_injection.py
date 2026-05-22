import random


def maybe_inject_failure(action):

    if action["type"] != "click":
        return action

    # 30% failure injection chance
    # inject_failure = random.random() < 0.3
    inject_failure = True

    if inject_failure:

        action["selector"] = (
            "#login-submit"
        )

        action["fault_injected"] = True

    return action