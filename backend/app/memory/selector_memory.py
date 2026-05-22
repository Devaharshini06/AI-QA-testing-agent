selector_memory = {}

def store_healing(
    failed_selector,
    healed_selector
):

    selector_memory[
        failed_selector
    ] = healed_selector

def get_known_healing(
    failed_selector
):

    return selector_memory.get(
        failed_selector
    )    