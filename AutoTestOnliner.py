from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys
import re

#Входные параметры
manufacturer = "Samsung"
year = "2019"
os = "Android"
screen_res = "1440x2560 "
screen_tech = "AMOLED"

driver = webdriver.Chrome()
driver.get('https://onliner.by')
driver.maximize_window()

time.sleep(2)

#Вход на сайт
#login = ''
#password = ''
#elem = driver.find_element_by_xpath("//div[contains(text(),'Вход')]")
#elem.click()
#time.sleep(2)
#elem = driver.find_element_by_xpath("//*[@type='text' and @placeholder='Ник или e-mail']")
#elem.send_keys(login)
#elem = driver.find_element_by_xpath("//input[@type='password']")
#elem.send_keys(password)
#elem = driver.find_element_by_xpath("//button[contains(text(),'Войти')]")
#elem.click()

#Вход в каталог
time.sleep(1)
elem = driver.find_element_by_xpath("//span[text()='Каталог' and @class='b-main-navigation__text']")
elem.click()

elem = driver.find_element_by_xpath("//span[text()='Электроника' and @class='catalog-navigation-classifier__item-title-wrapper']")
elem.click()

time.sleep(1)
elem = driver.find_element_by_xpath("//div[contains(text(),'Мобильные телефоны и') and @class='catalog-navigation-list__aside-title']")
elem.click()  

time.sleep(1)
elem = driver.find_element_by_xpath("//span[contains(string(),'Мобильные телефоны')]")
elem.click()

#manufacturer
time.sleep(3)
elem = driver.find_element_by_xpath("//span[contains(string(), 'Производитель')]/following::div[1]")
elements = elem.find_elements_by_xpath("//span[text()='" + manufacturer + "']")
for element in elements:
    if element.is_displayed():
        driver.execute_script("arguments[0].click();",element)
        break

#year
time.sleep(1)
driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
elem = driver.find_element_by_xpath("//span[text()='" + year + "']")
elem.click()

#os
time.sleep(1)
driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
elem = driver.find_element_by_xpath("//span[text()='" + os + "']")
elem.click()

#screen_res
time.sleep(1)
elem = driver.find_element_by_xpath("//span[contains(string(), 'Разрешение экрана')]/following::div[1]")
elem = elem.find_element_by_class_name("schema-filter-control__item")
elem.send_keys(screen_res)

#screen_tech
time.sleep(1)
driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
elem = driver.find_element_by_xpath("//span[text()='" + screen_tech + "']")
elem.click()

#Скролл вверх страницы
time.sleep(1)
driver.execute_script("window.scrollTo(1, -document.body.scrollHeight);")

prices = ['', '']

#Выбор смартфонов
for i in [0, 1]:
    elements = driver.find_elements_by_class_name('schema-product__group')
    elem = elements[i].find_element_by_class_name('schema-product__title')
    elem.click()

    phone_web = driver.find_element_by_xpath("//span[text()='" + manufacturer + "']").text
    year_web = driver.find_element_by_xpath('//td[contains(string(), "Дата выхода на рынок")]/following-sibling::td[1]').text
    os_web = driver.find_element_by_xpath('//td[contains(string(), "Операционная система")]/following-sibling::td[1]').text
    screen_res_web = driver.find_element_by_xpath('//td[contains(string(), "Разрешение экрана")]/following-sibling::td[1]').text
    screen_tech_web = driver.find_element_by_xpath('//td[contains(string(), "Технология экрана")]/following-sibling::td[1]').text

    #Модель телефона
    if manufacturer == phone_web:
        print("OK")
    else:
        print("EROOR")

    #Год 
    year_int = int(year)
    year_web_int = int(year_web.split(" ",1)[0])

    if year_int == year_web_int:
        print("OK")
    else:
        print("EROOR")

    #ОС
    if os == os_web:
        print("OK")
    else:
        print("EROOR")

    #Разрешение экрана
    a = int(screen_res.split("x",1)[0])
    b = int(screen_res.split("x",1)[1])
    c = int(screen_res_web.split("x",1)[0])
    d = int(screen_res_web.split("x",1)[1])

    if a >= c:
        if b <= d:
            print("OK")
        else:
            print("ERROR")

    #Тип экрана
    if screen_tech == screen_tech_web:
        print("OK")
    else:
        print("EROOR")

    time.sleep(1)

    #Просмотр всех предложений
    elem = driver.find_element_by_class_name('button.button_orange.button_big.offers-description__button')
    elem.click()

    driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")

    time.sleep(1)

    elem = driver.find_elements_by_class_name('button-style.button-style_primary.button-style_base.offers-form__button')
    if len(elem) > 0 and elem[0].is_displayed(): 
        elem[0].click()

    #Сортировка по цене
    elem = driver.find_element_by_xpath("//span[text()='По цене']")
    elem.click()
     
    time.sleep(1)

    elements = driver.find_elements_by_xpath('//tr[contains(@class,"state_add-to-cart m-divider")]')
    
    prices[i] = elements[0].find_element_by_class_name('price.price-primary').text

    elem = elements[0].find_element_by_class_name('button.button_orange.button_middle.offers-list__button.offers-list__button_basket')
    elem.click()

    time.sleep(1)
    
    if i == 0:
        driver.execute_script("window.history.go(-3)")

        time.sleep(1)

        scroll = driver.find_element_by_class_name('schema-header__title')
        action=ActionChains(driver)
        action.move_to_element(scroll).perform()

time.sleep(2)

elem = driver.find_element_by_class_name('button.button_orange.button_middle.offers-list__button.offers-list__button_basket.offers-list__button_checked')
elem.click()

a = float(re.findall(r"\d+\.\d+", prices[0].replace(',','.'))[0])
b = float(re.findall(r"\d+\.\d+", prices[1].replace(',','.'))[0])

time.sleep(2)

summa = driver.find_element_by_class_name('cart-form__description.cart-form__description_other.cart-form__description_extended').text.replace(',','.')

c = float(re.findall(r"\d+\.\d+", summa)[0])
 
if (a+b) == c:
    print("Тест пройден")
else:
    print("Тест не пройден")

time.sleep(1)
