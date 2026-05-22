import json
import re

from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="llama3"
)


def generate_browser_actions(task):

    prompt = f"""
You are an AI browser automation planner.

Generate ONLY a valid JSON array.

DO NOT explain anything.
DO NOT add markdown.
DO NOT add text before or after JSON.

Known SauceDemo Selectors:

Username input:
#user-name

Password input:
#password

Login button:
#login-button

Cart button:
.shopping_cart_link

Add to cart:
button[data-test^="add-to-cart"]

Available actions:
- open
- fill
- click
- verify
- screenshot

Example:

[
  {{
    "type": "open",
    "url": "https://www.saucedemo.com"
  }},
  {{
    "type": "fill",
    "selector": "#user-name",
    "value": "standard_user"
  }},
  {{
    "type": "fill",
    "selector": "#password",
    "value": "secret_sauce"
  }},
  {{
    "type": "click",
    "selector": "#login-button"
  }},
  {{
    "type": "verify",
    "selector": ".shopping_cart_link"
  }},
  {{
    "type": "screenshot",
    "path": "screenshots/final.png"
  }}
]

User Task:
{task}
"""

    response = llm.invoke(prompt)

    cleaned = response.strip()

    # Extract JSON array safely
    match = re.search(
        r"\[.*\]",
        cleaned,
        re.DOTALL
    )

    if not match:

        raise ValueError(
            "No valid JSON array found"
        )

    json_text = match.group()

    actions = json.loads(json_text)

    return actions