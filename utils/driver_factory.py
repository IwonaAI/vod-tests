import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Allow disabling SSL verification for webdriver-manager in corporate MITM environments
if os.getenv("DISABLE_DRIVER_SSL", "0") == "1":
    os.environ["WDM_SSL_VERIFY"] = "0"


def _headless_flag() -> bool:
    return os.getenv("HEADLESS", "0") in ("1", "true", "True")


def create_driver():
    browser = os.getenv("BROWSER", "chrome").lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])  # reduce noise
        if _headless_flag():
            options.add_argument("--headless=new")
        # Corporate proxy certificate issues workaround
        if os.getenv("IGNORE_CERT_ERRORS", "1") == "1":
            options.add_argument("--ignore-certificate-errors")

        manual_path = os.getenv("CHROMEDRIVER_PATH")
        if manual_path and os.path.exists(manual_path):
            return webdriver.Chrome(service=ChromeService(manual_path), options=options)
        try:
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        except Exception as e:
            # Fallback: try without webdriver-manager (selenium manager) or raise clearer message
            try:
                return webdriver.Chrome(options=options)
            except Exception:
                raise RuntimeError(f"Chrome driver initialization failed (network/SSL?). Set CHROMEDRIVER_PATH or DISABLE_DRIVER_SSL=1. Original error: {e}")

    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if _headless_flag():
            options.add_argument("-headless")
        manual_path = os.getenv("GECKODRIVER_PATH")
        if manual_path and os.path.exists(manual_path):
            return webdriver.Firefox(service=FirefoxService(manual_path), options=options)
        try:
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        except Exception as e:
            try:
                return webdriver.Firefox(options=options)
            except Exception:
                raise RuntimeError(f"Firefox driver initialization failed. Provide GECKODRIVER_PATH. Original error: {e}")

    if browser == "edge":
        options = webdriver.EdgeOptions()
        if _headless_flag():
            options.add_argument("--headless=new")
        manual_path = os.getenv("EDGEDRIVER_PATH")
        if manual_path and os.path.exists(manual_path):
            return webdriver.Edge(service=EdgeService(manual_path), options=options)
        try:
            return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        except Exception as e:
            try:
                return webdriver.Edge(options=options)
            except Exception:
                raise RuntimeError(f"Edge driver initialization failed. Provide EDGEDRIVER_PATH. Original error: {e}")

    raise ValueError(f"Unsupported browser: {browser}")
