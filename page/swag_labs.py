import time
import allure
from playwright.sync_api import Page, Locator
from base.base import BasePage, BaseHandle


class SwagLabs(BasePage):
    """Page object for Swag Labs"""

    def __init__(self, page: Page = None):
        super().__init__(page)

    def find_menu_button(self) -> Locator:
        """Find menu button"""
        return self.get_element("#react-burger-menu-btn")

    def find_logout_button(self) -> Locator:
        """Find logout button"""
        return self.get_element("#logout_sidebar_link")


class SwagLabsHandle(BaseHandle):
    """Handle class for Swag Labs operations"""

    def __init__(self, page: Page = None):
        self.swag_labs_page = SwagLabs(page)

    @allure.step(title="click menu button")
    def click_menu_button(self):
        """Click menu button"""
        self.click_element(self.swag_labs_page.find_menu_button())

    @allure.step(title="click logout button")
    def click_logout_button(self):
        """Click logout button"""
        self.click_element(self.swag_labs_page.find_logout_button())


class SwagLabsProxy:
    """Proxy class for Swag Labs business actions"""

    def __init__(self, page: Page = None):
        self.swag_labs_handle = SwagLabsHandle(page)

    @allure.step(title="logout from swag labs")
    def logout(self):
        """Perform logout"""
        self.swag_labs_handle.click_menu_button()
        time.sleep(2)
        self.swag_labs_handle.click_logout_button()