import allure
from playwright.sync_api import Page, Locator


def is_element_present(page: Page, text: str, timeout: int = 10000) -> bool:
    """
    Check if an element with the given text exists on the page.
    Uses Playwright's wait for functionality for stability.
    """
    try:
        page.get_by_text(text, exact=False).first.wait_for(timeout=timeout, state="visible")
        return True
    except Exception as e:
        # Attach screenshot only on failure
        allure.attach(
            page.screenshot(),
            name=f"Element '{text}' not found",
            attachment_type=allure.attachment_type.PNG
        )
        return False