from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class SearchResultsPage(BasePage):
    # Extended fallback locators for result items (posters / links to film pages)
    _result_items_locators = [
        (By.CSS_SELECTOR, "a[href*='/film/']"),
        (By.CSS_SELECTOR, "a[href*='/movies/']"),
        (By.CSS_SELECTOR, "a[href*='/watch']"),
        (By.XPATH, "//a[contains(@href,'/film/')]") ,
        (By.XPATH, "//a[contains(@href,'/movies/')]") ,
        (By.CSS_SELECTOR, "div[class*='Result'] a[href*='/']"),
        (By.CSS_SELECTOR, "section[class*='results'] a[href*='/']"),
        (By.CSS_SELECTOR, "div[class*='card'] a[href*='/']"),
        (By.CSS_SELECTOR, "a.card"),
        (By.XPATH, "//a[img and (contains(@href,'film') or contains(@href,'movie'))]") ,
        (By.XPATH, "//div[@role='link' and .//img]"),
    ]

    _results_container_locators = [
        (By.CSS_SELECTOR, "section[class*='results']"),
        (By.CSS_SELECTOR, "div[class*='results']"),
        (By.XPATH, "//section[contains(@class,'results')]") ,
        (By.XPATH, "//div[contains(@class,'results')]") ,
        (By.CSS_SELECTOR, "div[class*='grid']"),
    ]

    def _wait_for_container(self):
        for by, locator in self._results_container_locators:
            if self.exists(by, locator, timeout=5):
                return True
        return False

    def _gather_results_once(self):
        elements = []
        seen_ids = set()
        for by, locator in self._result_items_locators:
            try:
                found = self.driver.find_elements(by, locator)
                for el in found:
                    if id(el) not in seen_ids:
                        seen_ids.add(id(el))
                        elements.append(el)
            except Exception:
                continue
        return elements

    def wait_for_results(self, minimum: int = 1, timeout: int = 30):
        start = time.time()
        self._wait_for_container()
        results = []
        while time.time() - start < timeout:
            results = self._gather_results_once()
            if len(results) >= minimum:
                break
            try:
                ActionChains(self.driver).scroll_by_amount(0, 600).perform()
            except Exception:
                pass
            time.sleep(1)
        return results

    def _scroll_into_view(self, el):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        except Exception:
            pass

    def _robust_click(self, element):
        self._scroll_into_view(element)
        try:
            element.click()
            return True
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except Exception:
                try:
                    ActionChains(self.driver).move_to_element(element).click().perform()
                    return True
                except Exception:
                    return False

    def open_result_by_title_fragment(self, fragment: str, timeout: int = 30):
        fragment_lower = fragment.lower()
        items = self.wait_for_results(minimum=1, timeout=timeout)
        print(f"[SearchResultsPage] Found {len(items)} result items")
        if not items:
            self.save_screenshot("no_search_results.png")
            self.dump_page_source("no_search_results_source.html")
            raise AssertionError("No search results found")
        # Try find element whose text or aria-label contains fragment
        candidate = None
        for el in items:
            try:
                txt = (el.text or "").lower()
                aria = (el.get_attribute("aria-label") or "").lower()
                title = (el.get_attribute("title") or "").lower()
                if fragment_lower in txt or fragment_lower in aria or fragment_lower in title:
                    candidate = el
                    break
            except Exception:
                continue
        if candidate is None:
            candidate = items[0]  # fallback
        if not self._robust_click(candidate):
            self.save_screenshot("candidate_click_failed.png")
            self.dump_page_source("candidate_click_failed_source.html")
            raise AssertionError("Failed to click search result matching fragment")
        # Switch window if opened in new tab
        try:
            WebDriverWait(self.driver, 5).until(lambda d: len(d.window_handles) >= 1)
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception:
            pass

    # Keep old method for backward compatibility
    def open_first_result(self):
        self.open_result_by_title_fragment(fragment="pickup")
