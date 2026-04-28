import time
from playwright.sync_api import Page, Locator
from utility.driver_factory import DriverFactory


class BasePage:
    """Base page class for Playwright page objects"""

    def __init__(self, page: Page = None):
        self.page = page if page else DriverFactory.get_web_driver()

    def get_element(self, locator: str) -> Locator:
        """Get element locator with wait"""
        return self.page.locator(locator).first

    def get_element_by_text(self, text: str, exact: bool = False) -> Locator:
        """Get element by text"""
        return self.page.get_by_text(text, exact=exact)

    def wait_for_element(self, locator: str, timeout: int = 10000) -> Locator:
        """Wait for element to be visible"""
        return self.page.wait_for_selector(locator, timeout=timeout)


class BaseHandle:
    """Base handle class for common operations"""

    def __init__(self, page: Page = None):
        self.base_page = BasePage(page)

    def input_text(self, locator: Locator, text: str):
        """Input text into element"""
        locator.clear()
        locator.fill(text)
        time.sleep(1)

    def click_element(self, locator: Locator):
        """Click on element"""
        locator.click()
        time.sleep(1)

    def get_text(self, locator: Locator) -> str:
        """Get text from element"""
        return locator.text_content()

    def is_visible(self, locator: Locator, timeout: int = 5000) -> bool:
        """Check if element is visible"""
        try:
            locator.wait_for(timeout=timeout, state="visible")
            return True
        except:
            return False