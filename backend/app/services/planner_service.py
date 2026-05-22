from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="llama3"
)


def generate_test_plan(task):

    prompt = f"""
    You are an AI QA Test Planner.

    Generate a short browser testing plan.

    User Task:
    {task}

    Return steps only.

    Example:

    1. Open website
    2. Login
    3. Add item to cart
    4. Open cart
    5. Verify item
    """

    response = llm.invoke(prompt)

    return response