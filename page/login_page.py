import allure
from playwright.sync_api import Page, Locator
from base.base import BasePage, BaseHandle


class LoginPage(BasePage):
    """Page object for Login page"""

    def __init__(self, page: Page = None):
        super().__init__(page)

    def find_username_input(self) -> Locator:
        """Find username input field"""
        return self.get_element("#user-name")

    def find_password_input(self) -> Locator:
        """Find password input field"""
        return self.get_element("#password")

    def find_login_button(self) -> Locator:
        """Find login button"""
        return self.get_element("#login-button")


class LoginHandle(BaseHandle):
    """Handle class for Login page operations"""

    def __init__(self, page: Page = None):
        self.login_page = LoginPage(page)

    @allure.step(title="input username")
    def input_username(self, username: str):
        """Input username"""
        self.input_text(self.login_page.find_username_input(), username)

    @allure.step(title="input password")
    def input_password(self, password: str):
        """Input password"""
        self.input_text(self.login_page.find_password_input(), password)

    @allure.step(title="click login button")
    def click_login_button(self):
        """Click login button"""
        self.click_element(self.login_page.find_login_button())


class LoginProxy:
    """Proxy class for Login page business actions"""

    def __init__(self, page: Page = None):
        self.login_handle = LoginHandle(page)

    @allure.step(title="login with username and password")
    def login(self, username: str, password: str):
        """Perform login with username and password"""
        self.login_handle.input_username(username)
        self.login_handle.input_password(password)
        self.login_handle.click_login_button()