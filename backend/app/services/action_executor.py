from playwright.sync_api import sync_playwright
from datetime import datetime
from app.services.healing_service import (
    heal_selector
)
from app.tools.dom_inspector import (
    extract_interactive_elements
)
from app.services.fault_injection import (
    maybe_inject_failure
)

def execute_actions(actions):

    results = []
    recovery_count = 0
    verification_success = 0

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        for action in actions:
    
            action_type = action["type"]
            action = maybe_inject_failure(action)

            try:

                # OPEN URL
                if action_type == "open":

                    page.goto(
                        action["url"]
                    )

                    results.append(
                        f"Opened {action['url']}"
                    )

                # FILL INPUT
                elif action_type == "fill":

                    page.fill(
                        action["selector"],
                        action["value"]
                    )

                    results.append(
                        f"Filled {action['selector']}"
                    )

                # CLICK BUTTON
                elif action_type == "click":

                    try:
                    
                        page.click(
                            action["selector"],
                            timeout=5000
                        )

                        results.append(
                            f"Clicked {action['selector']}"
                        )

                    except Exception as click_error:
                    
                        results.append(
                            f"Click failed: {action['selector']}"
                        )

                        available_elements = (
                            extract_interactive_elements(page)
                        )

                        healing_result = heal_selector(
                            str(click_error),
                            action["selector"],
                            action_type,
                            available_elements
                        )
                        
                        healed_selector = healing_result[
                            "selector"
                        ]
                        
                        healing_source = healing_result[
                            "source"
                        ]
                        
                        results.append(
                            f"Healed via {healing_source}: {healed_selector}"
                        )
                        
                        # Small stabilization delay
                        page.wait_for_timeout(1000)
                        
                        # Retry click
                        page.click(
                            healed_selector,
                            timeout=5000
                        )
                        
                        results.append(
                            "Recovery click success"
                        )
                        
                        recovery_count += 1
                # VERIFY ELEMENT
                elif action_type == "verify":

                    visible = page.locator(
                        action["selector"]
                    ).is_visible()

                    results.append(
                        f"Verification: {visible}"
                    )
                    if visible:
                        verification_success += 1

                # SCREENSHOT
                elif action_type == "screenshot":

                    page.screenshot(
                        path=action["path"]
                    )

                    results.append(
                        "Screenshot saved"
                    )

            except Exception as e:

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )
                
                screenshot_path = (
                    f"screenshots/error_state_{timestamp}.png"
                )

                page.screenshot(
                    path=screenshot_path
                )

                results.append(
                    f"Error: {str(e)}"
                )

                results.append(
                    f"Failure screenshot: {screenshot_path}"
                )
        # Final execution screenshot
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        final_screenshot = (
            f"screenshots/final_execution_{timestamp}.png"
        )

        page.screenshot(
            path=final_screenshot
        )

        results.append(
            f"Final screenshot: {final_screenshot}"
        ) 

        results.append(
            f"Total recoveries: {recovery_count}"
        )
        results.append(
            f"Verification successes: {verification_success}"
        )
        browser.close()

    return results