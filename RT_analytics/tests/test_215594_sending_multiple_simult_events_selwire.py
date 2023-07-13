from seleniumwire import webdriver
from actions.actions_for_simult_events import ActionsForSimultEvents

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


def test_chrome_multiple_simult_events():
    """Отправка нескольких одновременных ивентов.
    Отправляются при загрузке страницы и при каждом обновлении.
    При отправке должен меняться только параметр mc."""
    print()
    print('CHROME')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_simult_events.html")
    time.sleep(1)

    #Собираем метрики после загрузки страницы
    actions_for_simult_events = ActionsForSimultEvents(driver)
    actions_for_simult_events.read_metrics_after_page_loading()

    #Обновляем страницу и собираем метрики для каждого обновления
    actions_for_simult_events = ActionsForSimultEvents(driver)
    actions_for_simult_events.read_metrics_while_refreshing_page()


def test_firefox_multiple_simult_events():
    """Отправка нескольких одновременных ивентов.
    Отправляются при загрузке страницы и при каждом обновлении.
    При отправке должен меняться только параметр mc."""
    print()
    print('FIREFOX')
    driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_simult_events.html")
    time.sleep(1)

    # Собираем метрики после загрузки страницы
    actions_for_simult_events = ActionsForSimultEvents(driver)
    actions_for_simult_events.read_metrics_after_page_loading()

    # Обновляем страницу и собираем метрики для каждого обновления
    actions_for_simult_events = ActionsForSimultEvents(driver)
    actions_for_simult_events.read_metrics_while_refreshing_page()

    driver.quit()


def test_edge_multiple_simult_events():
    """Отправка нескольких одновременных ивентов.
    Отправляются при загрузке страницы и при каждом обновлении.
    При отправке должен меняться только параметр mc."""
    print()
    print('EDGE')
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_simult_events.html")
    time.sleep(1)

    # Собираем метрики после загрузки страницы
    actions_for_simult_events = ActionsForSimultEvents(driver)
    actions_for_simult_events.read_metrics_after_page_loading()

    # Обновляем страницу и собираем метрики для каждого обновления
    actions_for_simult_events = ActionsForSimultEvents(driver)
    actions_for_simult_events.read_metrics_while_refreshing_page()

    driver.quit()
