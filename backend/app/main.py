from fastapi import FastAPI

from app.routes.test_routes import router as test_router
from app.routes.agent_routes import router as agent_router


app = FastAPI(
    title="AI QA Agent"
)

app.include_router(test_router)
app.include_router(agent_router)


@app.get("/")
def home():

    return {
        "message": "AI QA Agent Running"
    }