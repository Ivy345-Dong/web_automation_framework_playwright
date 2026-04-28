import time
import allure
from playwright.sync_api import Page, Locator
from base.base import BasePage, BaseHandle


class CartPage(BasePage):
    """Page object for Cart page"""

    def __init__(self, page: Page = None):
        super().__init__(page)

    def find_remove_button(self, goods_name: str) -> Locator:
        """Find remove button for specific goods"""
        goods_name_changed = goods_name.lower().replace(" ", "-")
        locator = f"[data-test='remove-{goods_name_changed}']"
        return self.get_element(locator)


class CartHandle(BaseHandle):
    """Handle class for Cart page operations"""

    def __init__(self, page: Page = None):
        self.cart_page = CartPage(page)

    @allure.step(title="choose a goods and remove from cart")
    def remove_from_cart_with_goods_name(self, goods_name: str):
        """Remove specific goods from cart"""
        self.click_element(self.cart_page.find_remove_button(goods_name))


class CartProxy:
    """Proxy class for Cart page business actions"""

    def __init__(self, page: Page = None):
        self.cart_handle = CartHandle(page)

    @allure.step(title="remove goods from cart and check number")
    def remove_goods_from_cart(self, goods_name: str):
        """Remove goods from cart"""
        self.cart_handle.remove_from_cart_with_goods_name(goods_name)
        time.sleep(2)