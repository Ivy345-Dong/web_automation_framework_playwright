import allure
import pytest
import logging
from utility.driver_factory import DriverFactory
from utility.data_reader import get_enabled_browsers


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption("--headless", action="store_true", default=False, help="run tests in headless mode")


@pytest.fixture(scope="session")
def browser(request):
    """Browser fixture - gets browser from parametrization"""
    return request.param


def pytest_generate_tests(metafunc):
    """Auto-parametrize tests with browsers from environment.yaml
    Uses indirect=True so tests don't need to accept browser parameter"""
    # 只对使用 driver_function 或 driver_class fixture 的测试进行参数化
    if "driver_function" in metafunc.fixturenames or "driver_class" in metafunc.fixturenames:
        enabled_browsers = get_enabled_browsers()
        # 使用 indirect=True，browser 参数不会直接传给测试方法，而是传给 browser fixture
        metafunc.parametrize("browser", enabled_browsers, indirect=True, scope="session")


@pytest.fixture(scope="function")
def driver_function(request, browser):
    """Fixture for function-scoped driver (fresh browser for each test)"""
    headless = request.config.getoption("--headless")
    
    driver = DriverFactory.get_web_driver(browser=browser, headless=headless)
    yield driver
    DriverFactory.quit_web_driver(driver)



@pytest.fixture(scope="class")
def driver_class(request, browser):
    """Fixture for class-scoped driver (shared browser across tests in class)"""
    headless = request.config.getoption("--headless")
    
    driver = DriverFactory.get_web_driver(browser=browser, headless=headless)
    yield driver
    DriverFactory.quit_web_driver(driver)


def setup_logger():
    """Configure logging for the test framework"""
    logger = logging.getLogger('test_framework')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('%(asctime)s [%(levelname)s] %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
        )
        logger.addHandler(handler)

    return logger


logger = setup_logger()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Automatically record the test execution process and failure information
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "setup":
        logger.info(f"test start: {item.nodeid}")

    elif report.when == "call":
        # 从 callspec 获取浏览器信息
        browser = "chromium"  # 默认值
        if hasattr(item, "callspec") and hasattr(item.callspec, "params"):
            browser = item.callspec.params.get("browser", "chromium")
        
        allure.dynamic.title(f"{item.originalname} [{browser.upper()}]")
        allure.dynamic.label("browser", browser)
        allure.dynamic.tag(browser)

        if report.passed:
            logger.info(f"test passed: {item.nodeid}")
        elif report.failed:
            logger.error(f"test failed: {item.nodeid}")
            logger.error(f"error message: {call.excinfo}")

    elif report.when == "teardown":
        logger.info(f"test finished: {item.nodeid}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """Record test setup phase"""
    logger.info(f"prepare to test: {item.name}")
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    """Record test teardown phase"""
    logger.info(f"clean test: {item.name}")
    yield