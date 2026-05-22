from fastapi import APIRouter

from app.agents.qa_graph import qa_graph


router = APIRouter(
    prefix="/agent",
    tags=["AI Agent"]
)


@router.get("/execute")

def execute_agent(task: str):

    result = qa_graph.invoke({
        "task": task
    })

    return result