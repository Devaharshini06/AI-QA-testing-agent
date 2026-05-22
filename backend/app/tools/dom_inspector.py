def extract_interactive_elements(page):

    elements = page.locator(
        "button, input, a"
    ).evaluate_all(
        """
        elements => elements.map(el => ({
            tag: el.tagName,
            text: el.innerText,
            id: el.id,
            class: el.className,
            type: el.type
        }))
        """
    )

    return elements