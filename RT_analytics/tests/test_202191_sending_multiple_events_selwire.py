from seleniumwire import webdriver
from actions.actions_for_multiple_events import ActionsForMultipleEvents

# Для Хром
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Для Мозиллы
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Для Эдж
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import time


def test_chrome_multiple_events():
    """Отправлка нескольких ивентов - обновляем страницу несколько раз.
    Первый ивент отправляется при загрузке страницы.
    mc - должен увеличиваться на 1 для каждой отправки (при обновлении страницы)."""
    print()
    print('CHROME')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric1.html")
    # driver.get("http://127.0.0.1:8080/metric/index_metric1.html")
    time.sleep(3)

    # Читаем и проверяем метрики sc и mc для первого запроса
    actions_for_multiple_events = ActionsForMultipleEvents(driver)
    actions_for_multiple_events.read_metrics_after_page_loading()

    # Читаем и проверяем метрики sc и mc для новых запросов при обновлении страницы
    actions_for_multiple_events = ActionsForMultipleEvents(driver)
    actions_for_multiple_events.read_metrics_while_refreshing_page()


def test_firefox_multiple_events():
    """Отправлка нескольких ивентов - обновляем страницу несколько раз.
    Первый ивент отправляется при загрузке страницы.
    mc - должен увеличиваться на 1 для каждой отправки."""
    print()
    print('FIREFOX')
    driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric1.html")
    time.sleep(1)

    # Читаем и проверяем метрики sc и mc для первого запроса
    actions_for_multiple_events = ActionsForMultipleEvents(driver)
    actions_for_multiple_events.read_metrics_after_page_loading()

    # Читаем и проверяем метрики sc и mc для новых запросов при обновлении страницы
    actions_for_multiple_events = ActionsForMultipleEvents(driver)
    actions_for_multiple_events.read_metrics_while_refreshing_page()

    driver.quit()


def test_edge_multiple_events():
    """Отправлка нескольких ивентов - обновляем страницу несколько раз.
    Первый ивент отправляется при загрузке страницы.
    mc - должен увеличиваться на 1 для каждой отправки."""
    print()
    print('EDGE')
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric1.html")
    time.sleep(1)

    # Читаем и проверяем метрики sc и mc для первого запроса
    actions_for_multiple_events = ActionsForMultipleEvents(driver)
    actions_for_multiple_events.read_metrics_after_page_loading()

    # Читаем и проверяем метрики sc и mc для новых запросов при обновлении страницы
    actions_for_multiple_events = ActionsForMultipleEvents(driver)
    actions_for_multiple_events.read_metrics_while_refreshing_page()

    driver.quit()
