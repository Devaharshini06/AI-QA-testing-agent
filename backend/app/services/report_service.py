from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="llama3"
)


def generate_test_report(task, result):

    prompt = f"""
    You are an AI QA Engineer.

    Analyze the following automated test result.

    User Task:
    {task}

    Test Result:
    {result}

    Generate:
    1. Test Summary
    2. Success/Failure Analysis
    3. Possible Issues
    4. Severity Level

    Keep response professional and concise.
    """

    response = llm.invoke(prompt)

    return response