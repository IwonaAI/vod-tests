from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PlayerComponent:
    _play_button = (By.CSS_SELECTOR, "button[aria-label*='Play'], button[class*='play'], .vjs-play-control")
    _pause_button = (By.CSS_SELECTOR, "button[aria-label*='Pause'], .vjs-play-control.vjs-playing")
    _video_tag = (By.CSS_SELECTOR, "video")

    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.timeout = timeout

    def _click_first_existing(self, locators):
        for by, locator in locators:
            try:
                el = WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable((by, locator))
                )
                el.click()
                return True
            except Exception:
                continue
        return False

    def play(self):
        # Some players require hover to reveal controls
        try:
            video = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(self._video_tag)
            )
            ActionChains(self.driver).move_to_element(video).perform()
        except Exception:
            pass
        self._click_first_existing([self._play_button])

    def pause(self):
        self._click_first_existing([self._pause_button])

    def is_playing(self) -> bool:
        try:
            video = self.driver.find_element(*self._video_tag)
            return video.get_attribute("paused") == "false"
        except Exception:
            return False

