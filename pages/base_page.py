from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.timeout = timeout

    def open(self, url: str):
        self.driver.get(url)

    def find(self, by: By, locator: str):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def find_clickable(self, by: By, locator: str):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((by, locator))
        )

    def finds(self, by: By, locator: str):
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located((by, locator))
        )
        return self.driver.find_elements(by, locator)

    def click(self, by: By, locator: str):
        self.find_clickable(by, locator).click()

    def type(self, by: By, locator: str, text: str, clear_first: bool = True):
        el = self.find_clickable(by, locator)
        if clear_first:
            el.clear()
        el.send_keys(text)

    def wait_visible(self, by: By, locator: str):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((by, locator))
        )

    def wait_invisible(self, by: By, locator: str):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.invisibility_of_element_located((by, locator))
        )

    def exists(self, by: By, locator: str, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            return True
        except Exception:
            return False

    def click_first_present(self, locators, timeout: int = None) -> bool:
        """Try a list of (By, locator) tuples, click first clickable. Returns True if clicked."""
        t = timeout or self.timeout
        for by, locator in locators:
            try:
                el = WebDriverWait(self.driver, t).until(EC.element_to_be_clickable((by, locator)))
                el.click()
                return True
            except Exception:
                continue
        return False

    def dismiss_overlays(self):
        """Attempt to close cookie consent / marketing overlays if present. Non-fatal."""
        candidates = [
            (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"),  # OneTrust common
            (By.CSS_SELECTOR, "button[aria-label*='Accept']"),
            (By.XPATH, "//button[contains(.,'Akceptuj') or contains(.,'Accept')]"),
            (By.CSS_SELECTOR, "button.cookie-accept"),
            (By.CSS_SELECTOR, "div.cookie-modal button.primary"),
        ]
        self.click_first_present(candidates, timeout=3)

    def save_screenshot(self, name: str = "screenshot.png"):
        """Best-effort screenshot capture."""
        try:
            self.driver.save_screenshot(name)
        except Exception:
            pass

    def dump_page_source(self, name: str = "page_source.html"):
        """Writes current page source to a file for debugging when locators fail."""
        try:
            with open(name, "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
        except Exception:
            pass
