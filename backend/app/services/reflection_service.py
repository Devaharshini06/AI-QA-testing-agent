from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="llama3"
)


def generate_reflection(
    task,
    execution_results,
    recovery_count,
    verification_successes
):

    prompt = f"""
You are an AI QA Reflection Engine.

Analyze this browser automation execution.

TASK:
{task}

EXECUTION RESULTS:
{execution_results}

RECOVERY COUNT:
{recovery_count}

VERIFICATION SUCCESSES:
{verification_successes}

Generate:

1. Reliability score (0-100)
2. Main failures
3. Recovery analysis
4. Optimization suggestions
5. Stability assessment

Keep response concise and professional.
"""

    reflection = llm.invoke(prompt)

    return reflection