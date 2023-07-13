import json
import time

from selenium.webdriver.common.by import By


CLICK_BUTTON_AFTER_DISCONNECTION = 3    # Количество кликов после отключения сети
NUMBER_OF_GENERATED_MESSAGES_WHILE_DISCONNECTION = 15    #Количество запросов, создаваемых после отключения сети
BATCH_CLICK_10 = 10    #Число кликов для создания батча

class ActionsForDistonnection:
    """Выполняем разлиные действия на веб-странице: клик по кнопке, отключение сети и т.д."""

    def __init__(self, driver):
        self.driver = driver

    def button_click_before_disconnection(self):
        """Выполняется контрольный клик по кнопке перед отключением сети.
        Затем собираются параметры из тела запроса, отправленного этим кликом."""

        print('Клик по кнопке перед оключением сети')
        button = self.driver.find_element(By.CLASS_NAME, "button_1")
        button.click()
        time.sleep(3)
        body = []
        for request in self.driver.requests:
            if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                body = json.loads(request.body)
                # print(json.loads(request.body))

        for i in body:
            print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])

    def button_click_for_sending_batch(self):
        """Несколько кликов для отправки батча нужного размера"""

        print('Делаем 10 кликов по кнопке перед оключением сети')
        for i in range(BATCH_CLICK_10):
            print("Клик по кнопке")
            button = self.driver.find_element(By.CLASS_NAME, "button_1")
            button.click()
            time.sleep(1)
        body = []
        for request in self.driver.requests:
            if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                body = json.loads(request.body)
                print(json.loads(request.body))

        for i in body:
            print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])

    def network_disconnection(self):
        """Отключаем соединение с Интернетом в браузере"""

        print('Отключаем соединение')
        self.driver.set_network_conditions(offline=True,
                                      latency=5,
                                      download_throughput=0,
                                      upload_throughput=0)
        time.sleep(3)

    def button_click_after_disconnection(self):
        """Выполняем клики по кнопке после отключения сети"""

        for i in range(CLICK_BUTTON_AFTER_DISCONNECTION):
            print('Клик по кнопке')
            button = self.driver.find_element(By.CLASS_NAME, "button_1")
            button.click()
            time.sleep(1)

        time.sleep(1)

    def view_local_storage(self):
        print('Выводим содержимое Local Storage')
        local_storage = self.driver.execute_script('return window.localStorage;')
        print(local_storage)
        return local_storage

    def network_connection(self):
        """Включаем соединение с Интернетом и ждем, пока оно установится"""

        print('Включаем соединение и ждем 60 секунд пока оно установится')
        self.driver.set_network_conditions(offline=False,
                                      latency=5,
                                      download_throughput=500 * 1024,
                                      upload_throughput=500 * 1024)

        time.sleep(60)

