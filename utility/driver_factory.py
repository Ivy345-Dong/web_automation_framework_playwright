import tkinter as tk
import logging
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from utility.data_reader import get_env_url


class DriverFactory:
    _logger = logging.getLogger('test_framework')
    _playwright = None
    _browser = {}
    _context = {}

    @classmethod
    def _get_screen_resolution(cls):
        """Get screen resolution using tkinter"""
        try:
            root = tk.Tk()
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            root.destroy()
            cls._logger.info(f"Detected screen resolution: {width}x{height}")
            return {"width": width, "height": height}
        except Exception as e:
            cls._logger.warning(f"Failed to detect screen resolution: {e}, using default 1280x720")
            return {"width": 1280, "height": 800}

    @classmethod
    def get_web_driver(cls, browser="chrome", headless=False):
        """
        Get Playwright browser instance
        Supports: chrome, firefox, edge, webkit (safari)
        """
        if cls._playwright is None:
            cls._playwright = sync_playwright().start()


        browser_type, channel = cls._get_browser_type(browser)
        
        launch_options = {
            "headless": headless,
            "args": [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-extensions",
                "--disable-default-apps",
                "--disable-background-networking",
                "--disable-sync",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-client-side-phishing-detection",
                "--disable-component-update",
                "--safebrowsing-disable-auto-update",
                "--disable-web-security",
                "--incognito",
                "--safebrowsing-disable-download-protection",
                "--safebrowsing-disable-extension-blacklist"
            ]
        }
        
        if channel:
            launch_options["channel"] = channel


        cls._browser = browser_type.launch(**launch_options)
        viewport = cls._get_screen_resolution()
        cls._context = cls._browser.new_context(viewport=viewport)
        page = cls._context.new_page()
        
        page.goto(get_env_url())
        return page

    @classmethod
    def _get_browser_type(cls, browser):
        """Get browser type and channel based on browser name"""
        browser_mapping = {
            "chrome": (cls._playwright.chromium, "chrome"),
            "chromium": (cls._playwright.chromium, None),
            "firefox": (cls._playwright.firefox, None),
            "edge": (cls._playwright.chromium, "msedge"),
            "webkit": (cls._playwright.webkit, None),
            "safari": (cls._playwright.webkit, None)
        }
        
        if isinstance(browser, list):
            browser = browser[0] if browser else "chrome"
        
        if browser not in browser_mapping:
            raise ValueError(f"Unsupported browser: {browser}")
        
        return browser_mapping[browser]

    @classmethod
    def quit_web_driver(cls, driver):
        """Quit browser and cleanup resources"""
        try:
            if driver:
                driver.close()
            if cls._context:
                cls._context.close()
            if cls._browser:
                cls._browser.close()
            if cls._playwright:
                cls._playwright.stop()
        except Exception as e:
            cls._logger.warning(f"Error quitting driver: {e}")
        finally:
            cls._playwright = None
            cls._browser = None
            cls._context = None