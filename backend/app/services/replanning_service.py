from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="llama3"
)


def generate_recovery_plan(
    task,
    failed_step,
    evaluation
):

    prompt = f"""
You are an autonomous AI QA replanning engine.

The original workflow encountered a failure.

TASK:
{task}

FAILED STEP:
{failed_step}

EVALUATION:
{evaluation}

Generate a SHORT alternative recovery strategy.

Keep response concise.
"""

    response = llm.invoke(prompt)

    return response