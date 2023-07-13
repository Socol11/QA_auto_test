import json
import time


REFRESH = 1


class ActionsForSessionExpiration:
    """Проверка отправки метрик до и после истечения сессии"""

    def __init__(self, driver):
        self.driver = driver

    def read_metrics_after_page_loading(self):
        """Собираем и проверяем метрики сразу после загрузки страницы"""
        body = []
        for request in self.driver.requests:
            if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                body = json.loads(request.body)
                # print(json.loads(request.body))

        print('Загрузка страницы')
        sc = 1
        mc = 1
        for i in body:
            print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
            assert i['mm_meta']['sc'] == sc and i['mm_meta']['mc'] == mc
            mc += 1
        print('-' * 50)
        print('Метрики sc и mc равны 1 - ожидаемый результат')

    def read_metrics_before_session_expired(self):
        """Собираем и проверяем метрики до истечения сессии"""
        sc = 1
        mc = 2
        for i in range(REFRESH):
            self.driver.refresh()
            time.sleep(3)

            for request in self.driver.requests:  # https://api.a.mts.ru/metric-api/api/message/json/v3?
                if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                    body = json.loads(request.body)

            for j in body:
                print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
                assert i['mm_meta']['sc'] == sc and i['mm_meta']['mc'] == mc
                print('Метрики sc = 1 и mc = 2, что соответствуют ожидаемым значениям')

    def read_metrics_after_session_expired(self):
        """Собираем и проверяем метрики после истечения сессии"""
        sc = 2
        mc = 1
        for i in range(REFRESH):
            self.driver.refresh()
            time.sleep(3)

            for request in self.driver.requests:  # https://api.a.mts.ru/metric-api/api/message/json/v3?
                if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                    body = json.loads(request.body)

            for j in body:
                print('sid:', i['mm_meta']['sid'], ' sc:', i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
                assert i['mm_meta']['sc'] == sc and i['mm_meta']['mc'] == mc
                print('Метрики sc = 2 и mc = 1, что соответствует ожидаемым значениям')
