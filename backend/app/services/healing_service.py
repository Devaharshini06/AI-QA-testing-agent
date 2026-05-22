import re

from langchain_ollama import OllamaLLM

from app.memory.selector_memory import (
    get_known_healing,
    store_healing
)

llm = OllamaLLM(
    model="llama3"
)


def heal_selector(
    error_message,
    failed_selector,
    action_type,
    available_elements
):

    # FIRST: Check memory
    known_fix = get_known_healing(
        failed_selector
    )

    if known_fix:

        print(
            f"[MEMORY] Using known fix for {failed_selector}"
        )

        return {
            "selector": known_fix,
            "source": "memory"
        }

    prompt = f"""
You are an AI selector healing system.

A browser selector failed.

ACTION TYPE:
{action_type}

FAILED SELECTOR:
{failed_selector}

AVAILABLE PAGE ELEMENTS:
{available_elements}

ERROR:
{error_message}

Known valid SauceDemo selectors:

#user-name
#password
#login-button
.shopping_cart_link
button[data-test^="add-to-cart"]

RULES:
- Return ONLY ONE selector
- No explanation
- No markdown
- No bullet points
- No sentences
- Output must start with:
# OR . OR button

If action type is "click":
prefer clickable selectors like:
- buttons
- links
- cart icons

Do NOT return:
- username fields
- password fields
- text inputs

Correct selector:
"""

    response = llm.invoke(prompt)

    cleaned = response.strip()

    # Extract selector safely
    match = re.search(
        r"(#\S+|\.\S+|button\[.*?\])",
        cleaned
    )

    if not match:

        return "#login-button"

    healed_selector = match.group()

    # Remove invalid combinations
    healed_selector = healed_selector.replace(
        ".#",
        "#"
    )

    healed_selector = healed_selector.replace(
        "#.",
        "#"
    )

    # Store successful recovery
    store_healing(
        failed_selector,
        healed_selector
    )

    return {
        "selector": healed_selector,
        "source": "llm"
    }