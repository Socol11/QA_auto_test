from seleniumwire import webdriver
from actions.actions_for_two_sdk import ActionsForTwoSDK

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


def test_chrome_two_sdk():
    """Проверка работы двух SDK на странице.
    Реализовано с помощью двух кнопок, привязанных к разным SDK.
    Сначала кнопки нажимаем подряд для каждого варианта SDK,
    а затем поочередно"""
    print()
    print('CHROME')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_two_sdk.html")
    time.sleep(3)

    # Загрузка страницы и проверка отправляемых метрик - ожидаем, что их нет для этого действия
    actions_for_two_sdk = ActionsForTwoSDK(driver)
    actions_for_two_sdk.read_metrics_after_page_loading()

    # Клики по кнопке 1, считывание метрик и их проверка
    actions_for_two_sdk = ActionsForTwoSDK(driver)
    actions_for_two_sdk.click_button_1()

    # Клики по кнопке 2, считывание метрик и их проверка
    actions_for_two_sdk = ActionsForTwoSDK(driver)
    actions_for_two_sdk.click_button_2()

    # Поочередные клики по кнопкам 1 и 2, считывание метрик и их проверка
    actions_for_two_sdk = ActionsForTwoSDK(driver)
    actions_for_two_sdk.click_buttons_alternatively()


def test_firefox_two_sdk():
    """Проверка работы двух SDK на странице.
        Реализовано с помощью двух кнопок, привязанных к разным SDK.
        Сначала кнопки нажимаем подряд для каждого варианта SDK,
        а затем поочередно"""
    print()
    print('FIREFOX')
    driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_two_sdk.html")
    time.sleep(3)

    # Загрузка страницы и проверка отправляемых метрик - ожидаем, что их нет для этого действия
    actions_for_two_sdk = ActionsForTwoSDK(driver)
    actions_for_two_sdk.read_metrics_after_page_loading()

    # Клики по кнопке 1, считывание метрик и их проверка
    actions_for_two_sdk = ActionsForTwoSDK(driver)
    actions_for_two_sdk.click_button_1()

    # Клики по кнопке 2, считывание метрик и их проверка
    actions_for_two_sdk = ActionsForTwoSDK(driver)
    actions_for_two_sdk.click_button_2()

    # Поочередные клики по кнопкам 1 и 2, считывание метрик и их проверка
    actions_for_two_sdk = ActionsForTwoSDK(driver)
    actions_for_two_sdk.click_buttons_alternatively()

    driver.quit()


# def test_edge_two_sdk():
#     """Проверка работы двух SDK на странице.
#         Реализовано с помощью двух кнопок, привязанных к разным SDK.
#         Сначала кнопки нажимаем подряд для каждого варианта SDK,
#         а затем поочередно"""
#     print()
#     print('EDGE')
#     driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
#     driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_two_sdk.html")
#     time.sleep(3)
#
#     # Загрузка страницы и проверка отправляемых метрик - ожидаем, что их нет для этого действия
#     actions_for_two_sdk = ActionsForTwoSDK(driver)
#     actions_for_two_sdk.read_metrics_after_page_loading()
#
#     # Клики по кнопке 1, считывание метрик и их проверка
#     actions_for_two_sdk = ActionsForTwoSDK(driver)
#     actions_for_two_sdk.click_button_1()
#
#     # Клики по кнопке 2, считывание метрик и их проверка
#     actions_for_two_sdk = ActionsForTwoSDK(driver)
#     actions_for_two_sdk.click_button_2()
#
#     # Поочередные клики по кнопкам 1 и 2, считывание метрик и их проверка
#     actions_for_two_sdk = ActionsForTwoSDK(driver)
#     actions_for_two_sdk.click_buttons_alternatively()
#
#     driver.quit()
