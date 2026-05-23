def observe_page(page):

    observation = {
        "url": page.url,
        "title": page.title(),
        "has_cart": page.locator(
            ".shopping_cart_link"
        ).count() > 0,
        "has_login_button": page.locator(
            "#login-button"
        ).count() > 0,
        "has_error_message": page.locator(
            "[data-test='error']"
        ).count() > 0
    }

    return observation