import pytest
from seleniumwire import webdriver

# Для Хром
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Для Мозиллы
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture
def page_web_sdk_chrome():
    print()
    print('CHROME')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.close()


@pytest.fixture
def page_web_sdk_firefox():
    print()
    print('FIREFOX')
    driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.close()