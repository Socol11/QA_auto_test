import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Number of clicks by buttons
CLICK_BUTTON_1 = 3
CLICK_BUTTON_2 = 3
CLICK_BUTTON_ALTERNATIVELY = 3


class ActionsForTwoSDK:
    """Проверка ивентов для двух разных SDK на web странице"""

    def __init__(self, driver):
        self.driver = driver

    def read_metrics_after_page_loading(self):
        """Загрузка страницы и проверка отправляемых метрик - ожидаем, что их нет для этого действия"""
        print()
        print('ЗАГРУЗКА СТРАНИЦЫ')
        body = []
        for request in self.driver.requests:
            if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                body = json.loads(request.body)
                # print(json.loads(request.body))

        for i in body:
            print('test:', i['test'], 'ts:', i['mm_meta']['ts'], 'sid:', i['mm_meta']['sid'], ' sc:',
                  i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])

    def click_button_1(self):
        """Клики по кнопке 1, считывание метрик и их проверка"""
        print()
        print('КЛИКИ ПО КНОПКЕ 1')

        sc = 1
        mc = 1
        for i in range(CLICK_BUTTON_1):
            button = self.driver.find_element(By.CLASS_NAME, "button_1")
            button.click()
            time.sleep(3)

            for request in self.driver.requests:  # https://api.a.mts.ru/metric-api/api/message/json/v3?
                if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                    body = json.loads(request.body)

            for i in body:
                print('test:', i['test'], 'ts:', i['mm_meta']['ts'], 'sid:', i['mm_meta']['sid'], ' sc:',
                      i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
                assert i['mm_meta']['sc'] == sc and i['mm_meta']['mc'] == mc

            mc += 1

    def click_button_2(self):
        """Клики по кнопке 2, считывание метрик и их проверка"""
        print()
        print('КЛИКИ ПО КНОПКЕ 2')

        sc = 1
        mc = 1
        for i in range(CLICK_BUTTON_2):
            button = self.driver.find_element(By.CLASS_NAME, "button_2")
            button.click()
            time.sleep(3)

            for request in self.driver.requests:  # https://api.a.mts.ru/metric-api/api/message/json/v3?
                if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                    body = json.loads(request.body)

            for i in body:
                print('test:', i['test'], 'ts:', i['mm_meta']['ts'], 'sid:', i['mm_meta']['sid'], ' sc:',
                      i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
                assert i['mm_meta']['sc'] == sc and i['mm_meta']['mc'] == mc

            mc += 1

    def click_buttons_alternatively(self):
        """Поочередные клики по кнопкам 1 и 2, считывание их метрик и их проверка"""
        print()
        print('ПООЧЕРЕДНЫЕ КЛИКИ ПО КНОПКАМ 1 И 2')

        sc = 1
        mc_1 = CLICK_BUTTON_1 + 1
        mc_2 = CLICK_BUTTON_2 + 1
        for i in range(CLICK_BUTTON_ALTERNATIVELY):
            button = self.driver.find_element(By.CLASS_NAME, "button_1")
            button.click()
            time.sleep(3)

            for request in self.driver.requests:  # https://api.a.mts.ru/metric-api/api/message/json/v3?
                if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                    body = json.loads(request.body)

            for i in body:
                print('test:', i['test'], 'ts:', i['mm_meta']['ts'], 'sid:', i['mm_meta']['sid'], ' sc:',
                      i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
                assert i['mm_meta']['sc'] == sc and i['mm_meta']['mc'] == mc_1

            mc_1 += 1

            button = self.driver.find_element(By.CLASS_NAME, "button_2")
            button.click()
            time.sleep(3)

            for request in self.driver.requests:  # https://api.a.mts.ru/metric-api/api/message/json/v3?
                if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                    body = json.loads(request.body)

            for i in body:
                print('test:', i['test'], 'ts:', i['mm_meta']['ts'], 'sid:', i['mm_meta']['sid'], ' sc:',
                      i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
                assert i['mm_meta']['sc'] == sc and i['mm_meta']['mc'] == mc_2

            mc_2 += 1
