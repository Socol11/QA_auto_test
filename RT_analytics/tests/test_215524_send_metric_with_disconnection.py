from actions.actions_for_disconnection import ActionsForDistonnection

import pytest
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import time
import json

# Для Хром
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Для Мозиллы
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Для Эдж
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


CLICK_BUTTON_AFTER_DISCONNECTION = 3    # Количество кликов после отключения сети
NUMBER_OF_GENERATED_MESSAGES_WHILE_DISCONNECTION = 15    #Количество запросов, создаваемых после отключения сети
BATCH_CLICK_10 = 10    #Число кликов для создания батча


def test_chrome_send_metric_with_disconnection_outqueue_false():
    """Хранение сообщений в Local Storage отключено.

    Отправляем одно сообщение и проверяем, что оно отправлено.
    Затем прерываем сеть.
    Далее пробуем отправлять запросы.
    Проверяем содержимое Local Storage. Ожидаем, что сообщения там не сохраняются.
    """
    print()
    print('CHROME - загрузка страницы')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_with_disconnection_outqueue_false.html")
    time.sleep(1)

    # Делаем контрольный клик перед отключением сети
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.button_click_before_disconnection()

    # Отключаем соединение с Интернетом в браузере
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.network_disconnection()

    # Клики после отключения соединения
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.button_click_after_disconnection()

    # Выводим содержимое Local Storage
    actions_for_disconnection = ActionsForDistonnection(driver)
    local_storage = actions_for_disconnection.view_local_storage()

    assert 'ma_ss' in list(local_storage.keys())[5]
    print('Запросы отсутствуют в Local Storage!')


def test_chrome_send_metric_with_disconnection():
    """Отправка запросов из Local Storage после отключения и последующего включения соединения.
    Время хранения запросов в Local Storage не истекает за время отключения.

    Отправляем одно сообщение, затем прерываем сеть.
    Далее отправляем еще сообщения - они попадают в Local Storage, так как нет соединения.
    Проверяем содержимое Local Storage.
    Затем включаем соединение (ждем около минуты до включения).
    Отправляем одно сообщение - сразу после этого отправляются все сообщения из Local Storage.
    Ждем, пока все отправится. Затем проверяем Local Storage - ожидаем, что там пусто.
    НЕ УДАЛОСЬ ПОКА ПОЙМАТЬ СООБЩЕНИЯ, ОТПРАВЛЯЕМЫЕ ИЗ LOCAL STORAGE. Просто видим, что они исчезли.
    Лучше проверить в Кафке."""
    print()
    print('CHROME - загрузка страницы')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_with_disconnection.html")
    time.sleep(1)

    # Делаем контрольный клик перед отключением сети
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.button_click_before_disconnection()

    #Отключаем соединение с Интернетом в браузере
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.network_disconnection()

    # Клики после отключения соединения
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.button_click_after_disconnection()

    print('Выводим содержимое Local Storage')
    local_storage = driver.execute_script('return window.localStorage;')
    print(local_storage)

    # Включаем соединение
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.network_connection()

    print('Делаем клик после соединения')
    button = driver.find_element(By.CLASS_NAME, "button_1")
    button.click()
    time.sleep(3)

    print('Ловим сообщения')
    for request in driver.requests:  # https://api.a.mts.ru/metric-api/api/message/json/v3?
        if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
            body = json.loads(request.body)

    for i in body:
        print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])

    print('Выводим содержимое Local Storage - ожидаем пустое значение')
    lr = driver.execute_script('return window.localStorage;')
    print(lr)
    # assert len(lr[list(lr.keys())[5]]) == 2
    assert lr[list(lr.keys())[5]] == '[]'
    print('Запросы отсутствуют в Local Storage!')


def test_chrome_send_1_message_with_disconnection_time_expired():
    """Проверяем, что сообщение удаляется из Local Storage, если исчерпаны попытки его отправки при отключенной сети.

    Отправляем одно сообщение (mc = 1), затем прерываем сеть.
    Далее отправляем одно сообщение (mc = 2) - оно попадает в Local Storage, так как нет соединения.
    Проверяем содержимое Local Storage. Сообщение должно храниться, но при этом начались попытки его отправки (5 попыток
        через каждые 3 секунды).
    Далее ждем в течение maxConnectionAttempts*reconnectTimeout/1000 - 1 секунда (параметры SDK из html-файла,
        определяющие число попыток и частоту попыток отправки)
    Проверяем содержимое Local Storage. Сообщение должно сохраниться.
    Ждем еще 2 секунды и проверяем Local Storage.
    Сообщение с mc = 2 должно исчезнуть из Local Storage.
    Затем включаем соединение и ждем, пока оно установится.
    Далее делаем клик по кнопке и ловим уходящие запросы.
    Параметр mc последнего клика равен 3.
    (Можно проверить в Кафке и убедиться, что для данного sid нет сообщения с mc = 2, но есть сообщения с mc = 1 и 3.)
    """
    print()
    print('CHROME - загрузка страницы')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_with_disconnection_time_expired.html")
    time.sleep(1)

    # Делаем контрольный клик перед отключением сети
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.button_click_before_disconnection()

    #Отключаем соединение с Интернетом в браузере
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.network_disconnection()

    print('Клик по кнопке')
    button = driver.find_element(By.CLASS_NAME, "button_1")
    button.click()

    print('Выводим содержимое Local Storage')
    local_storage = driver.execute_script('return window.localStorage;')
    print(local_storage)

    print('Ожидаем 11 секунд - чтобы не успели пройти все попытки отправки сообщений из Local Storage')
    time.sleep(11)

    print('Выводим содержимое Local Storage - ожидаем, что сообщение еще хранится')
    lr = driver.execute_script('return window.localStorage;')
    print(lr)

    assert len(lr[list(lr.keys())[5]]) > 2
    print('Запрос хранится в Local Storage!')

    print('Ожидаем еще 4 секунды - чтобы прошли все попытки отправки сообщения из Local Storage')
    time.sleep(4)

    print('Выводим содержимое Local Storage - ожидаем, что Local Storage пустой')
    lr = driver.execute_script('return window.localStorage;')
    print(lr)

    # assert len(lr[list(lr.keys())[5]]) == 2
    assert lr[list(lr.keys())[5]] == '[]'
    print('Запрос удален из Local Storage!')


def test_chrome_send_1_batch_with_disconnection_time_expired():
    """Проверяем, что батч удаляется из Local Storage, если исчерпаны попытки его отправки при отключенной сети.

    Отправляем один батч (mc = 1-10), затем прерываем сеть.
    Далее отправляем один батч (mc = 11-20) - он попадает в Local Storage, так как нет соединения.
    Проверяем содержимое Local Storage. Батч должен храниться, но при этом начались попытки его отправки (5 попыток
        через каждые 3 секунды).
    Далее ждем в течение maxConnectionAttempts*reconnectTimeout/1000 - 1 секунда (параметры SDK из html-файла,
        определяющие число попыток и частоту попыток отправки)
    Проверяем содержимое Local Storage. Батч должен сохраниться.
    Ждем еще 4 секунды и проверяем Local Storage.
    Батч должен исчезнуть из Local Storage.
    (Можно проверить в Кафке и убедиться, что для данного sid нет сообщений с mc = 11-20, но есть сообщения с mc = 1-10.)
    """
    print()
    print('CHROME - загрузка страницы')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_with_disconnection_batching_true.html")
    time.sleep(1)

    # Клики по кнопке для создания батча
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.button_click_for_sending_batch()

    #Отключаем соединение с Интернетом в браузере
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.network_disconnection()

    print('Подключение разорвано! Делаем отправку сообщений в батч.')
    for i in range(BATCH_CLICK_10):
        print("Клик по кнопке")
        button = driver.find_element(By.CLASS_NAME, "button_1")
        button.click()
        time.sleep(1)

    print('Выводим содержимое Local Storage')
    local_storage = driver.execute_script('return window.localStorage;')
    print(local_storage)

    print('Ожидаем 11 секунд - чтобы не успели пройти все попытки отправки батча из Local Storage')
    time.sleep(11)

    print('Выводим содержимое Local Storage - ожидаем, что батч еще хранится')
    lr = driver.execute_script('return window.localStorage;')
    print(lr)

    assert len(lr[list(lr.keys())[5]]) > 2
    print('Батч хранится в Local Storage!')

    print('Ожидаем еще 4 секунды - чтобы прошли все попытки отправки батча из Local Storage')
    time.sleep(4)

    print('Выводим содержимое Local Storage - ожидаем, что Local Storage пустой')
    lr = driver.execute_script('return window.localStorage;')
    print(lr)

    assert len(lr[list(lr.keys())[5]]) == 2
    print('Батч удален из Local Storage!')

#
def test_chrome_max_number_of_stored_messages():
    """Проверка максимального количества хранимых в Local Storage запросов

    Отправляем одно сообщение, затем прерываем сеть.
    Далее отправляем более 10 сообщений - они попадают в Local Storage, так как нет соединения.
    Проверяем содержимое Local Storage. Сообщения должны храниться - но только 10 шт - удаляются более ранние.
    Затем включаем соединение и ждем, пока оно установится.
    Далее делаем клик по кнопке и проверяем содержимое Local Storage - ожидаем, что там пусто - все сообщения отправлены.
    При этом важно, чтобы mc последнего клика соответствовал порядку сообщений в целом.
    """
    print()
    print('CHROME - загрузка страницы')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_with_disconnection.html")
    time.sleep(1)

    # Делаем контрольный клик перед отключением сети
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.button_click_before_disconnection()

    # Отключаем соединение с Интернетом в браузере
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.network_disconnection()

    for i in range(NUMBER_OF_GENERATED_MESSAGES_WHILE_DISCONNECTION):
        print('Клик по кнопке', i+1)
        button = driver.find_element(By.CLASS_NAME, "button_1")
        button.click()
        time.sleep(1)

    time.sleep(3)

    print('Выводим содержимое Local Storage')
    local_storage = driver.execute_script('return window.localStorage;')
    print(local_storage)

    # Включаем соединение
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.network_connection()

    print('Делаем клик после соединения')
    button = driver.find_element(By.CLASS_NAME, "button_1")
    button.click()
    time.sleep(10)

    print('Ловим сообщения')
    for request in driver.requests:  # https://api.a.mts.ru/metric-api/api/message/json/v3?
        if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
            body = json.loads(request.body)

    for i in body:
        print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])

    print('Выводим содержимое Local Storage - ожидаем пустое значение')
    lr = driver.execute_script('return window.localStorage;')
    print(lr)
    time.sleep(3)


def test_chrome_batching():
    """
    Отправляем одно сообщение, затем прерываем сеть.
    Далее отправляем более 10 сообщений - они попадают в Local Storage, так как нет соединения.
    Проверяем содержимое Local Storage. Сообщения должны храниться - но только 10 шт - удаляются более ранние.
    Затем включаем соединение и ждем, пока оно установится.
    Далее делаем клик по кнопке и проверяем содержимое Local Storage - ожидаем, что там пусто - все сообщения отправлены.
    При этом важно, чтобы mc последнего клика соответствовал порядку сообщений в целом.
    """
    print()
    print('CHROME - загрузка страницы')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("file:///Users/rvpomazan1/PycharmProjects/3574_webSDK_loss/pages/index_metric_with_disconnection.html")
    time.sleep(1)

    # Делаем контрольный клик перед отключением сети
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.button_click_before_disconnection()

    # Отключаем соединение с Интернетом в браузере
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.network_disconnection()

    for i in range(NUMBER_OF_GENERATED_MESSAGES_WHILE_DISCONNECTION):
        print('Клик по кнопке')
        button = driver.find_element(By.CLASS_NAME, "button_1")
        button.click()
        time.sleep(1)

    time.sleep(3)

    print('Выводим содержимое Local Storage')
    local_storage = driver.execute_script('return window.localStorage;')
    print(local_storage)

    # Включаем соединение
    actions_for_disconnection = ActionsForDistonnection(driver)
    actions_for_disconnection.network_connection()

    print('Делаем клик после соединения')
    button = driver.find_element(By.CLASS_NAME, "button_1")
    button.click()
    time.sleep(10)

    print('Ловим сообщения')
    for request in driver.requests:  # https://api.a.mts.ru/metric-api/api/message/json/v3?
        if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
            body = json.loads(request.body)

    for i in body:
        print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])

    print('Выводим содержимое Local Storage - ожидаем пустое значение')
    lr = driver.execute_script('return window.localStorage;')
    print(lr)
    time.sleep(3)
