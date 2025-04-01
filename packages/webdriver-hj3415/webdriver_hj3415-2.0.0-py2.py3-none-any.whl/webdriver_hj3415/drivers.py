import random

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

# 브라우저별 관리자 (webdriver_manager)
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Selenium 서비스
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService

# Selenium Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from utils_hj3415 import setup_logger

mylogger=setup_logger(__name__, 'INFO')


COMMON_USER_AGENTS = [
    # --- Chrome (Windows) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/110.0.5481.100 Safari/537.36",

    # --- Chrome (Mac) ---
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/111.0.5563.64 Safari/537.36",

    # --- Firefox (Windows) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) "
    "Gecko/20100101 Firefox/108.0",

    # --- Firefox (Linux) ---
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) "
    "Gecko/20100101 Firefox/109.0",

    # --- Edge (Windows) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/110.0.5481.100 Safari/537.36 "
    "Edg/110.0.1587.49",

    # --- Safari (Mac) ---
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/16.1 Safari/605.1.15",

    # --- Safari (iPhone iOS) ---
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/16.0 Mobile/15E148 Safari/604.1",

    # --- Chrome (Android) ---
    "Mozilla/5.0 (Linux; Android 13; SM-S908N) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/110.0.5481.65 Mobile Safari/537.36",

    # --- Opera (Windows) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/110.0.5481.77 Safari/537.36 OPR/96.0.4693.80",

    # --- Older Edge (Windows) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/92.0.902.62 Safari/537.36 "
    "Edg/92.0.902.62",
]

def get_random_user_agent() -> str:
    """랜덤 User-Agent 하나 반환"""
    return random.choice(COMMON_USER_AGENTS)


def get(browser: str = "chrome", **kwargs) -> WebDriver:
    """
    통합 WebDriver 생성 함수
    :param browser: 'chrome', 'firefox', 'edge', 'safari', 'chromium'
    :param kwargs: headless=True/False, driver_version=None, geolocation=False 등
    """
    browser = browser.lower()
    if browser == "chrome":
        return get_chrome(**kwargs)
    elif browser == "firefox":
        return get_firefox(**kwargs)
    elif browser == "edge":
        return get_edge(**kwargs)
    elif browser == "safari":
        return get_safari(**kwargs)
    elif browser == "chromium":
        return get_chromium(**kwargs)
    else:
        raise ValueError(f"Unsupported browser type: {browser}")


def get_chrome(driver_version: str = None,
               temp_dir: str = '',
               headless: bool = True,
               geolocation: bool = False) -> WebDriver:
    """Chrome WebDriver를 반환"""
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")

    # Random User-Agent
    chrome_options.add_argument(f"--user-agent={get_random_user_agent()}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # prefs 설정
    prefs = {}
    if geolocation:
        prefs.update({
            'profile.default_content_setting_values': {
                'notifications': 1,
                'geolocation': 1
            },
            'profile.managed_default_content_settings': {
                'geolocation': 1
            }
        })
    if temp_dir:
        prefs.update({
            'download.default_directory': temp_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        })

    if prefs:
        chrome_options.add_experimental_option('prefs', prefs)

    service = ChromeService(ChromeDriverManager(driver_version=driver_version).install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    mylogger.info(f"Chrome driver obtained successfully. headless={headless}, geolocation={geolocation}")
    return driver


def get_firefox(headless: bool = True) -> WebDriver:
    """Firefox WebDriver 반환"""
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("general.useragent.override", get_random_user_agent())

    firefox_options = FirefoxOptions()
    if headless:
        firefox_options.add_argument("-headless")
    firefox_options.profile = firefox_profile

    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)
    mylogger.info(f"Firefox driver obtained successfully. headless={headless}")
    return driver


def get_edge() -> WebDriver:
    """Edge WebDriver 반환"""
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    mylogger.info("Edge driver obtained successfully.")
    return driver


def get_safari() -> WebDriver:
    """Safari WebDriver 반환"""
    # Safari는 headless 모드를 지원하지 않음
    # 사파리 설정(개발자 > 원격자동화 허용) 필요
    driver = webdriver.Safari()
    mylogger.info("Safari driver obtained successfully.")
    return driver


def get_chromium(headless: bool = True) -> WebDriver:
    """Chromium WebDriver 반환"""
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-agent={get_random_user_agent()}")

    service = ChromeService("/usr/bin/chromedriver")  # 크롬드라이버 위치 직접 지정
    driver = webdriver.Chrome(service=service, options=chrome_options)
    mylogger.info(f"Chromium driver obtained successfully. headless={headless}")
    return driver