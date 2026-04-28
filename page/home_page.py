import time
import allure
from playwright.sync_api import Page, Locator
from base.base import BasePage, BaseHandle


class HomePage(BasePage):
    """Page object for Home page"""

    def __init__(self, page: Page = None):
        super().__init__(page)

    def find_add_to_cart_button(self, goods_name: str) -> Locator:
        """Find add to cart button for specific goods"""
        goods_name_changed = goods_name.lower().replace(" ", "-")
        locator = f"[data-test='add-to-cart-{goods_name_changed}']"
        return self.get_element(locator)

    def find_cart_icon(self) -> Locator:
        """Find cart icon"""
        return self.get_element("[data-test='shopping-cart-link']")

    def find_cart_badge(self) -> Locator:
        """Find cart badge showing number of items"""
        return self.get_element("[data-test='shopping-cart-badge']")


class HomeHandle(BaseHandle):
    """Handle class for Home page operations"""

    def __init__(self, page: Page = None):
        self.home_page = HomePage(page)

    @allure.step(title="choose a goods and add to cart")
    def add_to_cart_with_goods_name(self, goods_name: str):
        """Add specific goods to cart"""
        self.home_page.find_add_to_cart_button(goods_name).click()

    @allure.step(title="obtain the number of goods in cart")
    def check_number_of_goods_in_cart(self) -> str:
        """Get number of goods in cart"""
        number = self.home_page.find_cart_badge().text_content()
        return str(number)

    @allure.step(title="go to the cart page")
    def click_cart_icon(self):
        """Click cart icon to navigate to cart page"""
        self.click_element(self.home_page.find_cart_icon())


class HomeProxy:
    """Proxy class for Home page business actions"""

    def __init__(self, page: Page = None):
        self.home_handle = HomeHandle(page)

    @allure.step(title="add goods to cart and check number")
    def add_goods_to_cart_and_check_number(self, goods_name: str) -> str:
        """Add goods to cart and return the number of items"""
        self.home_handle.add_to_cart_with_goods_name(goods_name)
        time.sleep(2)
        return self.home_handle.check_number_of_goods_in_cart()