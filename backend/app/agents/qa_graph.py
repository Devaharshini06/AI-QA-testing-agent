from typing import TypedDict
# from urllib import response

from langgraph.graph import StateGraph, END

from langchain_ollama import OllamaLLM
from app.services.report_service import generate_test_report
from app.tools.browser_tool import test_login
from app.tools.browser_tool import (
    test_login, failed_login_test, test_shopping_flow
)
from app.services.planner_service import generate_test_plan
from app.services.action_executor import (
    execute_actions
)
from app.services.action_generator import (
    generate_browser_actions
)
from app.services.reflection_service import (
    generate_reflection
)

# Local LLM
llm = OllamaLLM(
    model="llama3"
)


# Graph State
class QAState(TypedDict):

    task: str
    route: str
    result: dict
    report: str
    plan: str


# Node 1
def classify_task(state):

    task = state["task"]

    prompt = f"""
        You are an AI QA routing agent.

        Your job is to classify user testing tasks.

        AVAILABLE ROUTES:

        1. login_test
        Use ONLY for:
        - successful login testing
        - valid login workflow
        - normal authentication

        2. failed_login_test
        Use ONLY for:
        - failed login
        - invalid credentials
        - wrong password
        - login failure
        - authentication failure

        3. shopping_test
        Use ONLY for:
        - shopping cart
        - add to cart
        - checkout
        - inventory workflows

        4. dynamic_shopping
        Use for shopping related tasks that require dynamic action execution.

        5. autonomous_execution
        Use for tasks that don't fit other routes but can be executed via autonomous action generation and execution.

        6. unknown
        Use if no route matches.

        USER TASK:
        {task}

        Return ONLY ONE route name.

        Examples:

        Task: test successful login
        Route: login_test

        Task: test failed login
        Route: failed_login_test

        Task: test invalid password
        Route: failed_login_test

        Task: test shopping cart
        Route: shopping_test

        Task: autonomously test login workflow
        Route: autonomous_execution
        """

    response = llm.invoke(prompt)

    cleaned = response.strip().lower()

    valid_routes = [
        "login_test",
        "shopping_test",
        "failed_login_test",
        "dynamic_shopping",
        "autonomous_execution"
    ]

    route = "unknown"

    for valid_route in valid_routes:

        if valid_route in cleaned:
            route = valid_route
            break

    plan = generate_test_plan(task)

    return {
        "task": task,
        "route": route,
        "result": {},
        "report": "",
        "plan": plan
    }


# Node 2
def login_test_node(state):

    result = test_login()

    report = generate_test_report(
        state["task"],
        result
    )

    return {
        "task": state["task"],
        "route": "login_test",
        "result": result,
        "report": report,
        "plan": state["plan"]
    }

def shopping_test_node(state):

    result = test_shopping_flow()

    report = generate_test_report(
        state["task"],
        result
    )

    return {
        "task": state["task"],
        "route": "shopping_test",
        "result": result,
        "report": report,
        "plan": state["plan"]
    }

def dynamic_shopping_node(state):

    actions = [

        {
            "type": "open",
            "url": "https://www.saucedemo.com"
        },

        {
            "type": "fill",
            "selector": "#user-name",
            "value": "standard_user"
        },

        {
            "type": "fill",
            "selector": "#password",
            "value": "secret_sauce"
        },

        {
            "type": "click",
            "selector": "#login-button"
        },

        {
            "type": "click",
            "selector":
                'button[data-test^="add-to-cart"]'
        },

        {
            "type": "click",
            "selector":
                ".shopping_cart_link"
        },

        {
            "type": "verify",
            "selector": ".cart_item"
        },

        {
            "type": "screenshot",
            "path":
                "screenshots/dynamic_cart.png"
        }
    ]

    result = execute_actions(actions)

    report = generate_test_report(
        state["task"],
        result
    )

    return {
        "task": state["task"],
        "route": "dynamic_shopping",
        "result": result,
        "report": report,
        "plan": state["plan"]
    }

def failed_login_node(state):

    result = failed_login_test()

    report = generate_test_report(
        state["task"],
        result
    )

    return {
        "task": state["task"],
        "route": "failed_login_test",
        "result": result,
        "report": report,
        "plan": state["plan"]
    }

def autonomous_execution_node(state):

    actions = generate_browser_actions(
        state["task"]
    )

    result = execute_actions(actions)

    report = generate_test_report(
        state["task"],
        result
    )

    # Metrics
    recovery_count = len([
        r for r in result
        if "Recovery" in r
    ])

    verification_successes = len([
        r for r in result
        if "Verification: True" in r
    ])

    # Reflection Engine
    reflection = generate_reflection(
        task=state["task"],
        execution_results=result,
        recovery_count=recovery_count,
        verification_successes=verification_successes
    )

    return {
        "task": state["task"],
        "route": "autonomous_execution",
        "result": result,
        "report": report,
        "reflection": reflection,
        "plan": actions
    }

# Router
def router(state):

    route = state["route"].strip()

    if route == "login_test":
        return "login_test"

    if route == "shopping_test":
        return "shopping_test"

    if route == "failed_login_test":
        return "failed_login_test"

    if route == "dynamic_shopping":
        return "dynamic_shopping"
    
    if route == "autonomous_execution":
        return "autonomous_execution"

    return END


# Build Graph
graph = StateGraph(QAState)

graph.add_node(
    "classifier",
    classify_task
)

graph.add_node(
    "login_test",
    login_test_node
)

graph.add_node(
    "failed_login_test",
    failed_login_node
)

graph.add_node(
    "shopping_test",
    shopping_test_node
)

graph.add_node(
    "dynamic_shopping",
    dynamic_shopping_node
)

graph.add_node(
    "autonomous_execution",
    autonomous_execution_node
)

graph.set_entry_point(
    "classifier"
)

graph.add_conditional_edges(
    "classifier",
    router,
    {
        "login_test": "login_test",
        "shopping_test": "shopping_test",
        "failed_login_test": "failed_login_test",
        "dynamic_shopping": "dynamic_shopping",
        "autonomous_execution": "autonomous_execution",
        END: END
    }
)

graph.add_edge(
    "login_test",
    END
)
graph.add_edge(
    "shopping_test",
    END
)
graph.add_edge(
    "failed_login_test",
    END
)
graph.add_edge(
    "dynamic_shopping",
    END
)
graph.add_edge(
    "autonomous_execution",
    END
)
qa_graph = graph.compile()