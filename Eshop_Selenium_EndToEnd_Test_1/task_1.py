import time

from selenium import webdriver
# Для Хром
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

"""Запускаем браузер"""

# Этот код нужен, чтобы Chrome не закрывался сразу после открытия
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
base_url = 'https://www.saucedemo.com/'
driver.get(base_url)
driver.maximize_window()

"""Заполняем форму регистрации и заходим на сайт"""

print("Заполняем форму регистрации и заходим на сайт")
login_standard_user = 'standard_user'
password_all = 'secret_sauce'

# Задаём переменную для поля имени пользователя:
user_name = driver.find_element(by=By.XPATH, value='//input[@id="user-name"]')
user_name.send_keys(login_standard_user)
print('Input login')

# Задаём переменную для поля пароля
password = driver.find_element(by=By.XPATH, value='//input[@id="password"]')
password.send_keys(password_all)
print('Input password')
time.sleep(1)

# Нажимаем кнопку отправки формы
button_login = driver.find_element(by=By.XPATH, value='//input[@id="login-button"]')
button_login.click()
print('Click login button')
time.sleep(1)
print()

"""Информация по первому товару: название и цена"""

print('Добавляем товары в корзину')
# Сохраняем название и цену
prodict_1 = driver.find_element(by=By.XPATH, value='//a[@id="item_4_title_link"]')
value_product_1 = prodict_1.text
print(value_product_1)

price_product_1 = driver.find_element(by=By.XPATH, value='//*[@id="inventory_container"]/div/div[1]/div[2]/div[2]/div')
value_price_product_1 = price_product_1.text
print(value_price_product_1)

# Добавляем товар в корзину
select_product_1 = driver.find_element(by=By.XPATH, value='//button[@id="add-to-cart-sauce-labs-backpack"]')
select_product_1.click()
print('Товар "sauce-labs-backpack" добавлен в корзину')
time.sleep(1)

"""Информация по второму товару: название и цена"""

# Сохраняем название и цену
prodict_2 = driver.find_element(by=By.XPATH, value='//a[@id="item_5_title_link"]')
value_product_2 = prodict_2.text
print(value_product_2)

price_product_2 = driver.find_element(by=By.XPATH, value='//*[@id="inventory_container"]/div/div[4]/div[2]/div[2]/div')
value_price_product_2 = price_product_2.text
print(value_price_product_2)

# Добавляем товар в корзину
select_product_2 = driver.find_element(by=By.XPATH, value='//button[@id="add-to-cart-sauce-labs-fleece-jacket"]')
select_product_2.click()
print('Товар "sauce-labs-fleece-jacket" добавлен в корзину')
time.sleep(1)
print()

# Входим в корзину через кнопку корзины в верхнем правом углу
print('Входим в корзину')
cart = driver.find_element(by=By.XPATH, value='//a[@class="shopping_cart_link"]')
cart.click()
print('Вход в корзину выполнен')
time.sleep(1)

# Сохраняем информацию о продуктах в корзине: названия и цены
cart_prodict_1 = driver.find_element(by=By.XPATH, value='//a[@id="item_4_title_link"]')
value_cart_product_1 = cart_prodict_1.text
print(value_cart_product_1)
assert value_product_1 == value_cart_product_1
print('Названия товара 1 совпадают!')
cart_price_product_1 = driver.find_element(by=By.XPATH,
                                           value='//*[@id="cart_contents_container"]/div/div[1]/div[3]/div[2]/div[2]/div')
value_cart_price_product_1 = cart_price_product_1.text
print(value_cart_price_product_1)
assert value_price_product_1 == value_cart_price_product_1
print('Цены товара 1 совпадают!')

cart_prodict_2 = driver.find_element(by=By.XPATH, value='//a[@id="item_5_title_link"]')
value_cart_product_2 = cart_prodict_2.text
print(value_cart_product_2)
assert value_product_2 == value_cart_product_2
print('Названия товара 2 совпадают!')
cart_price_product_2 = driver.find_element(by=By.XPATH,
                                           value='//*[@id="cart_contents_container"]/div/div[1]/div[4]/div[2]/div[2]/div')
value_cart_price_product_2 = cart_price_product_2.text
print(value_cart_price_product_2)
assert value_price_product_2 == value_cart_price_product_2
print('Цены товара 2 совпадают!')
time.sleep(1)
print()

# Переходим на страницу оплаты, кликаем кнопку Checkout
print('Переходим на страницу оплаты')
checkout = driver.find_element(by=By.XPATH, value='//button[@id="checkout"]')
checkout.click()
print('Переход на страницу оплаты выполнен!')
time.sleep(1)
print()

"""Вводим информацию о пользователе"""

print("Вводим информацию о пользователе")
first_name = driver.find_element(by=By.XPATH, value='//input[@id="first-name"]')
first_name.send_keys('John')
print('Имя пользователя введено')
last_name = driver.find_element(by=By.XPATH, value='//input[@id="last-name"]')
last_name.send_keys('Holiday')
print('Фамилия пользователя введена')
postal_code = driver.find_element(by=By.XPATH, value='//input[@id="postal-code"]')
postal_code.send_keys(123456)
print('Почтовый код пользователя введён')
# Жмём кнопку Continue
continue_button = driver.find_element(by=By.XPATH, value='//input[@id="continue"]')
continue_button.click()
print('Данные пользователя введены!')
print('Переход на финишную страницу выполнен.')
print()

"""Финишная страница"""

print('Сравниваем названия и цены на финишной странице')
# Сравниваем название и цену товаров 1 и 2 на первой и на финишной странице
finish_prodict_1 = driver.find_element(by=By.XPATH, value='//a[@id="item_4_title_link"]/div')
value_finish_product_1 = finish_prodict_1.text
print(value_finish_product_1)
assert value_product_1 == value_finish_product_1
print('Названия товара 1 на первой и финишной страницах совпадают!')
finish_price_product_1 = driver.find_element(by=By.XPATH,
                                             value='//*[@id="checkout_summary_container"]/div/div[1]/div[3]/div[2]/div[2]/div')
value_finish_price_product_1 = finish_price_product_1.text
print(value_finish_price_product_1)
assert value_price_product_1 == value_finish_price_product_1
print('Цены товара 1 на первой и финишной страницах совпадают!')

finish_prodict_2 = driver.find_element(by=By.XPATH, value='//a[@id="item_5_title_link"]/div')
value_finish_product_2 = finish_prodict_2.text
print(value_finish_product_2)
assert value_product_2 == value_finish_product_2
print('Названия товара 2 на первой и финишной страницах совпадают!')
finish_price_product_2 = driver.find_element(by=By.XPATH,
                                             value='//*[@id="checkout_summary_container"]/div/div[1]/div[4]/div[2]/div[2]/div')
value_finish_price_product_2 = finish_price_product_2.text
print(value_finish_price_product_2)
assert value_price_product_2 == value_finish_price_product_2
print('Цены товара 2 на первой и финишной страницах совпадают!')
print()

# Сравниваем общую сумму покупок с данными на странице
print('Сравниваем общую сумму покупок с данными на странице')
summary_price = driver.find_element(by=By.XPATH, value='//*[@id="checkout_summary_container"]/div/div[2]/div[6]')
value_summary_price = summary_price.text
print(value_summary_price)
total_sum = float(value_summary_price[13:])
summ = float(value_price_product_1[1:]) + float(value_price_product_2[1:])
assert total_sum == summ
print(f'Общая сумма покупок корректна и равна {total_sum}!')
time.sleep(1)

# Жмём кнопку Finish
finish_button = driver.find_element(by=By.XPATH, value='//button[@id="finish"]')
finish_button.click()
print('Покупка успешно завершена!')
print('-'*30)
print()
print('Тест успешно завершён!')
