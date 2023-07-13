from seleniumwire import webdriver
from actions.actions_for_session_expiration import ActionsForSessionExpiration

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
import json

# Number of page refreshes in the browser
REFRESH = 1


def test_chrome_before_session_expired():
    """Проверяем метрики mc и sc до истечения таймаута сессии.
    mc меняется, sc - не меняется, так как сессия та же"""
    print()
    print('CHROME')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric1.html")
    time.sleep(3)

    actions_for_session_expiration = ActionsForSessionExpiration(driver)
    actions_for_session_expiration.read_metrics_after_page_loading()

    time.sleep(1790)

    actions_for_session_expiration = ActionsForSessionExpiration(driver)
    actions_for_session_expiration.read_metrics_before_session_expired()


def test_chrome_after_session_expired():
    """Проверяем метрики mc и sc после истечения таймаута сессии.
    mc начинается с единицы, sc увеличивается на 1"""
    print()
    print('CHROME')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric1.html")
    time.sleep(3)

    actions_for_session_expiration = ActionsForSessionExpiration(driver)
    actions_for_session_expiration.read_metrics_after_page_loading()

    time.sleep(1810)

    actions_for_session_expiration = ActionsForSessionExpiration(driver)
    actions_for_session_expiration.read_metrics_after_session_expired()


# def test_firefox_before_session_expires():
#     """Проверяем метрики mc и sc до истечения таймаута сессии.
#     mc меняется, sc - не меняется, так как сессия та же"""
#     print()
#     print('FIREFOX')
#     driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()))
#     driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric1.html")
#     time.sleep(1)
#     body = []
#     for request in driver.requests:
#         if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
#             body = json.loads(request.body)
#             # print(json.loads(request.body))
#
#     for i in body:
#         print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
#
#     time.sleep(1790)
#
#     for i in range(REFRESH):
#         driver.refresh()
#         time.sleep(1)
#
#         for request in driver.requests:    # https://api.a.mts.ru/metric-api/api/message/json/v3?
#             if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
#                 body = json.loads(request.body)
#
#         for i in body:
#             print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
#
#     driver.quit()
#
#
# def test_firefox_after_session_expires():
#     """Проверяем метрики mc и sc после истечения таймаута сессии.
#     mc начинается с единицы, sc увеличивается на 1"""
#     print()
#     print('FIREFOX')
#     driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()))
#     driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric1.html")
#     time.sleep(1)
#     body = []
#     for request in driver.requests:
#         if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
#             body = json.loads(request.body)
#             # print(json.loads(request.body))
#
#     for i in body:
#         print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
#
#     time.sleep(1810)
#
#     for i in range(REFRESH):
#         driver.refresh()
#         time.sleep(1)
#
#         for request in driver.requests:    # https://api.a.mts.ru/metric-api/api/message/json/v3?
#             if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
#                 body = json.loads(request.body)
#
#         for i in body:
#             print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
#
#     driver.quit()
#
#
# def test_edge_before_session_expires():
#     """Проверяем метрики mc и sc до истечения таймаута сессии.
#     mc меняется, sc - не меняется, так как сессия та же"""
#     print()
#     print('EDGE')
#     driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
#     driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric1.html")
#     time.sleep(1)
#     body = []
#     for request in driver.requests:
#         if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
#             body = json.loads(request.body)
#             # print(json.loads(request.body))
#
#     for i in body:
#         print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
#
#     time.sleep(1790)
#
#     for i in range(REFRESH):
#         driver.refresh()
#         time.sleep(1)
#
#         for request in driver.requests:    # https://api.a.mts.ru/metric-api/api/message/json/v3?
#             if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
#                 body = json.loads(request.body)
#
#         for i in body:
#             print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
#
#     driver.quit()
#
#
# def test_edge_after_session_expires():
#     """Проверяем метрики mc и sc после истечения таймаута сессии.
#     mc начинается с единицы, sc увеличивается на 1"""
#     print()
#     print('EDGE')
#     driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
#     driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric1.html")
#     time.sleep(1)
#     body = []
#     for request in driver.requests:
#         if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
#             body = json.loads(request.body)
#             # print(json.loads(request.body))
#
#     for i in body:
#         print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
#
#     time.sleep(1810)
#
#     for i in range(REFRESH):
#         driver.refresh()
#         time.sleep(1)
#
#         for request in driver.requests:    # https://api.a.mts.ru/metric-api/api/message/json/v3?
#             if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
#                 body = json.loads(request.body)
#
#         for i in body:
#             print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
#
#     driver.quit()
