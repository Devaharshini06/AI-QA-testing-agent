def generate_goal_actions(goal):

    if goal == "shopping":

        return [
            {
                "type": "click",
                "selector": "button[data-test^='add-to-cart']"
            },
            {
                "type": "click",
                "selector": ".shopping_cart_link"
            },
            {
                "type": "verify",
                "selector": ".cart_item"
            },
            {
                "type": "screenshot",
                "path": "screenshots/shopping_goal.png"
            }
        ]

    return []