import requests


class TestFromFile:
    """Создание новых локаций, сохранение их в файл и проверка их наличия по записям в файле"""

    def __init__(self):
        pass

    def create_locations(self):
        """Создание новых локаций и запись их place_id в файл"""

        post_url = 'https://rahulshettyacademy.com/maps/api/place/add/json?key=qaclick123'
        json_for_create_new_locations = {
                                            "location": {

                                                "lat": -38.383494,

                                                "lng": 33.427362

                                            }, "accuracy": 50,

                                            "name": "Frontline house",

                                            "phone_number": "(+91) 983 893 3937",

                                            "address": "29, side layout, cohen 09",

                                            "types": [

                                                "shoe park",

                                                "shop"

                                            ],

                                            "website": "http://google.com",

                                            "language": "French-IN"

                                        }

        print('СОЗДАЁМ НОВЫЕ ЛОКАЦИИ')

        for i in range(1, 6):
            result_post = requests.post(post_url, json=json_for_create_new_locations)
            place_id = result_post.json().get('place_id')
            assert 200 == result_post.status_code
            print(f'Создана {i}-ая локация. Place_id = {place_id}.')

            fa = open('file.txt', 'a')  # параметр 'a' - запись новых данных в конец файла
            fa.write(place_id + '\n')
            fa.close()

        print()

    def read_locations(self):
        """Чтение локаций из файла и проверка их наличия на сервере"""

        fr = open('file.txt', 'r')
        text = fr.read().split('\n')[:-1]
        fr.close()
        # print(text)

        print('ПРОВЕРЯЕМ, ЧТО НОВЫЕ ЛОКАЦИИ СУЩЕСТВУЮТ')

        for place_id in text:
            get_url = 'https://rahulshettyacademy.com/maps/api/place/get/json?key=qaclick123' + '&place_id=' + str(place_id)
            # print(get_url)
            get_result = requests.get(get_url)
            assert get_result.status_code == 200
            print(f'Данные для place_id = {place_id} существуют.')


post = TestFromFile()
post.create_locations()
post.read_locations()
