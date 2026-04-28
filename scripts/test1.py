import pytest


class Test1:

    @pytest.fixture(autouse=True)
    def setup_method(self, driver_function):
        """Setup for each test method - creates independent browser instance"""
        self.driver = driver_function

    def test_a1(self):
        print("----------1----------")
        self.driver.reload()

    def test_a2(self):
        print("----------2----------")
        self.driver.reload()

    def test_a3(self):
        print("----------3----------")
        self.driver.reload()
