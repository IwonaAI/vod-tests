from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
from utils import config

class HomePage(BasePage):
    # Removed hardcoded URL; using config.BASE_URL
    # URL = "https://www.vod.film/"

    # Multiple fallback locators for search input
    _search_input_locators = [
        (By.CSS_SELECTOR, "div.input__InputContainer-sc-dbb50d3a-0 input[placeholder='Wyszukuj filmy i seriale...']"),
        (By.CSS_SELECTOR, "input[placeholder='Wyszukuj filmy i seriale...']"),
        (By.XPATH, "//input[@placeholder='Wyszukuj filmy i seriale...']"),
        (By.CSS_SELECTOR, "input[type='search']"),
    ]

    # Multiple fallback locators for search button 'Szukaj'
    _search_button_locators = [
        (By.CSS_SELECTOR, "div.input__ButtonContainer-sc-dbb50d3a-1 button.global__Button-sc-8b79a7a-10"),
        (By.CSS_SELECTOR, "div.input__ButtonContainer-sc-dbb50d3a-1 button"),
        (By.XPATH, "//div[contains(@class,'ButtonContainer')]/button[normalize-space()='Szukaj']"),
        (By.XPATH, "//button[normalize-space()='Szukaj']"),
        (By.XPATH, "//button[contains(.,'Szukaj')]") ,
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "button[aria-label*='Szukaj']"),
        (By.CSS_SELECTOR, "button[title*='Szukaj']"),
    ]

    def go_to(self):
        self.open(config.BASE_URL)
        self.dismiss_overlays()

    def _resolve_input(self):
        for by, locator in self._search_input_locators:
            try:
                return self.find(by, locator)
            except Exception:
                continue
        self.save_screenshot("search_input_not_found.png")
        raise AssertionError("Search input not found with any locator")

    def _resolve_and_type(self, phrase: str):
        input_el = self._resolve_input()
        input_el.clear()
        input_el.send_keys(phrase)
        return input_el

    def _click_search_button_or_enter(self, input_el):
        for by, locator in self._search_button_locators:
            try:
                el = self.find_clickable(by, locator)
                el.click()
                return
            except Exception:
                continue
        # Fallback: ENTER
        try:
            input_el.send_keys(Keys.ENTER)
            return
        except Exception:
            self.save_screenshot("search_button_not_found.png")
            raise AssertionError("Search button not found and ENTER fallback failed")

    def search(self, phrase: str):
        input_el = self._resolve_and_type(phrase)
        self._click_search_button_or_enter(input_el)
