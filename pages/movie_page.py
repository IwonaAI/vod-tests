from selenium.webdriver.common.by import By
from .base_page import BasePage
from .player_component import PlayerComponent
import time
from utils import config

class MoviePage(BasePage):
    _player_root = (By.CSS_SELECTOR, "div[id*='player'], #player, video")
    _play_button_variants = [
        (By.CSS_SELECTOR, "button[aria-label*='Play']"),
        (By.CSS_SELECTOR, "button[class*='play']"),
        (By.CSS_SELECTOR, ".vjs-play-control"),
    ]
    _login_modal_locators = [
      (By.CSS_SELECTOR, "div#popup"),
    ]

    def get_player(self):
        self.find(*self._player_root)
        return PlayerComponent(self.driver)

    def is_login_modal_visible(self) -> bool:
        for by, locator in self._login_modal_locators:
            if self.exists(by, locator, timeout=2):
                return True
        return False

    def wait_for_login_modal(self, timeout: int | None = None):
        effective_timeout = timeout or config.LOGIN_MODAL_TIMEOUT
        start = time.time()
        while time.time() - start < effective_timeout:
            if self.is_login_modal_visible():
                return True
            time.sleep(1)
        self.save_screenshot("login_modal_not_found.png")
        self.dump_page_source("login_modal_not_found_source.html")
        return False
