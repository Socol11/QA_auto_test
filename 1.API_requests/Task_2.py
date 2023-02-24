import requests


class DeletePlaces:


    def __init__(self):
        pass

    def delete_place(self):
        """Выбираем удаляемые объекты из файла и удаляем их с сервера"""

        # Читаем place_id из файла
        fr = open('file.txt', 'r')
        place_ids = fr.read().split('\n')[:-1]

        # Выбираем 2 и 4 place_id по условию задачи
        place_ids_24 = [x for x in place_ids if place_ids.index(x) in [1, 3]]
        fr.close()
        print('ВЫБИРАЕМ ОБЪЕКТЫ И УДАЛЯЕМ ИХ С СЕРВЕРА')
        print('-' * 20)
        print(f'Выбраны для удаления: {place_ids_24}')

        # Удаляем выбранные place_id с сервера
        del_url = 'https://rahulshettyacademy.com/maps/api/place/delete/json?key=qaclick123'
        for place_id in place_ids_24:
            json_del = {"place_id": place_id}
            result_del = requests.delete(del_url, json=json_del)
            assert 200 == result_del.status_code
            print(f'Порядок! Статус код для {place_id} = 200!')
            check_delete = result_del.json()
            print(check_delete)
            check_delete_info = check_delete.get('status')
            assert check_delete_info == "OK"
            print(f'Удаление {place_id} прошло успешно!')
            print()

        print('-'*20)

    def select_existing_places(self):
        """Читает place_id из файла file.txt и проверяет, какие из них существуют на сервере.
        Записывает существующие на сервере place_id в новый файл file_existing_places.txt"""

        # Читаем сохраненные ранее place_id из файла
        fr = open('file.txt', 'r')
        place_ids = fr.read().split('\n')[:-1]

        # Проверяем, какие place_id есть на сервере
        for place_id in place_ids:
            get_url = 'https://rahulshettyacademy.com/maps/api/place/get/json?key=qaclick123' + '&place_id=' + place_id
            result_get = requests.get(get_url)
            if result_get.status_code == 200:
                print(f'Place_id {place_id} существует на сервере! Записываем в файл.')
                fa = open('file_existing_places.txt', 'a')
                fa.write(place_id + '\n')
                fa.close()

        print(f'Файл успешно записан!')


places = DeletePlaces()
places.delete_place()
places.select_existing_places()
