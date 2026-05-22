from fastapi import APIRouter
from app.tools.browser_tool import google_search
from app.tools.browser_tool import open_website
from app.tools.browser_tool import test_login

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)


@router.get("/open")

def test_browser():

    result = open_website(
        "https://example.com"
    )

    return result

@router.get("/search")

def test_search(query: str):

    result = google_search(query)

    return result

@router.get("/login-test")

def login_test():

    result = test_login()

    return result