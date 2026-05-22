from app.tools.browser_tool import test_login


def qa_agent(user_task):

    task = user_task.lower()

    # Login testing route
    if "login" in task:

        result = test_login()

        return {
            "task": user_task,
            "action": "Executed login test",
            "result": result
        }

    return {
        "task": user_task,
        "action": "No matching test workflow found"
    }