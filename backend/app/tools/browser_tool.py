from playwright.sync_api import sync_playwright
from datetime import datetime

def open_website(url):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto(url)

        title = page.title()

        content = page.locator("body").inner_text()

        browser.close()

        return {
            "title": title,
            "content": content[:1000]
        }
    
def google_search(search_query):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        # Open Google
        page.goto("https://www.google.com")

        # Fill search box
        page.fill(
            'textarea[name="q"]',
            search_query
        )

        # Press Enter
        page.keyboard.press("Enter")

        # Wait for results
        page.wait_for_timeout(3000)

        # Extract titles
        headings = page.locator("h3").all_inner_texts()

        browser.close()

        return {
            "query": search_query,
            "results": headings[:5]
        }
    
def test_login():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        # Open website
        page.goto(
            "https://www.saucedemo.com"
        )

        # Fill username
        page.fill(
            '#user-name',
            'standard_user'
        )

        # Fill password
        page.fill(
            '#password',
            'secret_sauce'
        )

        # Click login
        page.click(
            '#login-button'
        )

        # Wait for inventory page
        page.wait_for_selector(
            '.inventory_list'
        )

        # Extract page title
        title = page.title()

        # Check inventory page
        success = page.locator(
            '.inventory_list'
        ).is_visible()

        browser.close()

        return {
            "title": title,
            "login_success": success
        }
    
def failed_login_test():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto(
            "https://www.saucedemo.com"
        )

        # WRONG credentials
        page.fill(
            '#user-name',
            'wrong_user'
        )

        page.fill(
            '#password',
            'wrong_password'
        )

        page.click(
            '#login-button'
        )

        # Wait for error
        page.wait_for_selector(
            '[data-test="error"]'
        )

        # Extract error message
        error_message = page.locator(
            '[data-test="error"]'
        ).inner_text()

        # Capture screenshot
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        screenshot_path = (
            f"screenshots/login_failure_{timestamp}.png"
        )

        page.screenshot(
            path=screenshot_path
        )

        browser.close()

        return {
            "login_success": False,
            "error_message": error_message,
            "screenshot": screenshot_path       
        }
    
    
def test_shopping_flow():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        # Open SauceDemo
        page.goto(
            "https://www.saucedemo.com"
        )

        # Login
        page.fill(
            '#user-name',
            'standard_user'
        )

        page.fill(
            '#password',
            'secret_sauce'
        )

        page.click(
            '#login-button'
        )

        # Wait for inventory page
        page.wait_for_selector(
            '.inventory_list'
        )

        # Add first item to cart
        page.click(
            'button[data-test^="add-to-cart"]'
        )

        # Open cart
        page.click(
            '.shopping_cart_link'
        )

        # Capture screenshot
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    
        screenshot_path = (
            f"screenshots/shopping_cart_{timestamp}.png"
        )
    
        page.screenshot(
            path=screenshot_path
        )

        # Validate cart item exists
        cart_item_visible = page.locator(
            '.cart_item'
        ).is_visible()

        browser.close()

        return {
            "shopping_flow_success": cart_item_visible,
            "screenshot": screenshot_path
        }