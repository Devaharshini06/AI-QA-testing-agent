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
from app.services.observation_service import (
    observe_page
)
from app.services.state_evaluator import (
    evaluate_state
)
from app.services.retry_policy import (
    decide_retry
)
from app.services.replanning_service import (
    generate_recovery_plan
)
from app.services.objective_engine import (
    determine_next_goal
)
from app.services.goal_action_generator import (
    generate_goal_actions
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
                        observation = observe_page(page)
                        evaluation = evaluate_state(
                            observation
                        )
                        next_goal = determine_next_goal(observation)

                        decision = decide_retry(
                            evaluation
                        )
                        if decision["retry"]:

                            results.append(
                                "Retrying action..."
                            )

                            page.wait_for_timeout(2000)

                            page.click(
                                action["selector"],
                                timeout=5000
                            )

                            results.append(
                                "Retry successful"
                            )  
                            retry_observation = observe_page(page)

                            retry_evaluation = evaluate_state(
                                retry_observation
                            )

                            recovery_plan = generate_recovery_plan(
                                task="Browser QA workflow",
                                failed_step=action,
                                evaluation=evaluation
                            )

                            results.append(
                                f"Dynamic recovery plan: {recovery_plan}"
                            )

                            results.append(
                                f"Retry observation: {retry_observation}"
                            )

                            results.append(
                                f"Retry evaluation: {retry_evaluation}"
                            )

                        results.append(
                            f"Decision: {decision}"
                        )
                        results.append(f"Observation: {observation}")
                        results.append(f"Next Objective: {next_goal}")
                        goal_actions = generate_goal_actions(
                            next_goal
                        )

                        if goal_actions:
                        
                            results.append(
                                f"Generated goal actions: {goal_actions}"
                            )

                            for goal_action in goal_actions:
                            
                                try:
                                
                                    if goal_action["type"] == "click":
                                    
                                        page.click(
                                            goal_action["selector"]
                                        )

                                        results.append(
                                            f"Goal click success: {goal_action['selector']}"
                                        )

                                    elif goal_action["type"] == "verify":
                                    
                                        visible = page.locator(
                                            goal_action["selector"]
                                        ).is_visible()

                                        results.append(
                                            f"Goal verification: {visible}"
                                        )

                                    elif goal_action["type"] == "screenshot":
                                    
                                        page.screenshot(
                                            path=goal_action["path"]
                                        )

                                        results.append(
                                            "Goal screenshot saved"
                                        )

                                except Exception as goal_error:
                                
                                    results.append(
                                        f"Goal execution error: {goal_error}"
                                    )
                        results.append(f"State Evaluation: {evaluation}")

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
                        observation = observe_page(page)
                        evaluation = evaluate_state(observation)
                        results.append(f"Post-healing observation: {observation}")
                        results.append(f"Post-healing evaluation: {evaluation}")
                        
                        results.append(
                            "Recovery click success"
                        )
                        next_goal = determine_next_goal(
                            observation
                        )
                        
                        results.append(
                            f"Next objective: {next_goal}"
                        )
                        
                        goal_actions = generate_goal_actions(
                            next_goal
                        )
                        
                        if goal_actions:
                        
                            results.append(
                                f"Generated goal actions: {goal_actions}"
                            )
                        
                            for goal_action in goal_actions:
                            
                                try:
                                
                                    if goal_action["type"] == "click":
                                    
                                        page.click(
                                            goal_action["selector"]
                                        )
                        
                                        results.append(
                                            f"Goal click success: {goal_action['selector']}"
                                        )
                        
                                    elif goal_action["type"] == "verify":
                                    
                                        visible = page.locator(
                                            goal_action["selector"]
                                        ).is_visible()
                        
                                        results.append(
                                            f"Goal verification: {visible}"
                                        )
                        
                                    elif goal_action["type"] == "screenshot":
                                    
                                        page.screenshot(
                                            path=goal_action["path"]
                                        )
                        
                                        results.append(
                                            "Goal screenshot saved"
                                        )
                        
                                except Exception as goal_error:
                                
                                    results.append(
                                        f"Goal execution error: {goal_error}"
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