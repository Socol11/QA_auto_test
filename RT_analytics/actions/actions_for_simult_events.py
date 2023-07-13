import json
import time


# Number of page refreshes in the browser
REFRESH = 3

class ActionsForSimultEvents:
    """Проверка параллельных ивентов на web странице"""

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
            print('test:', i['test'], 'ts:', i['mm_meta']['ts'], 'sid:', i['mm_meta']['sid'], ' sc:',
                  i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
            assert i['mm_meta']['sc'] == sc and i['mm_meta']['mc'] == mc
            mc += 1
        print('-' * 50)
        print('Метрики sc и mc имеют нормальный инкремент')

    def read_metrics_while_refreshing_page(self):
        """Собираем и проверяем метрики после каждого обновления страницы"""
        sc = 1
        mc = 6
        for i in range(REFRESH):
            self.driver.refresh()
            time.sleep(1)
            print()
            print('Обновление страницы', i + 1)

            for request in self.driver.requests:  # https://api.a.mts.ru/metric-api/api/message/json/v3?
                if request.method == 'POST' and 'https://api-mm-uat.bd-cloud.mts.ru/metric-api/api/message/json/v3?' in request.url:
                    body = json.loads(request.body)

            for i in body:
                print('test:', i['test'], 'ts:', i['mm_meta']['ts'], 'sid:', i['mm_meta']['sid'], ' sc:',
                      i['mm_meta']['sc'], ' mc:', i['mm_meta']['mc'])
                assert i['mm_meta']['sc'] == sc and i['mm_meta']['mc'] == mc
                mc += 1

            print('-' * 50)
            print('Метрики sc и mc имеют нормальный инкремент')
