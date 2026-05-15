import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    # Selenium Manager will auto-download the appropriate driver
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux


    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@allure.feature("Authentication")
@allure.title("Успешный вход в систему с валидными значениями")
@allure.description("""
    Тест проверяет авторизацию с корректными учетными данными
    1. Переход на страницу /login
    2. Ввод логина 'tomsmith' и пароля 'SuperSecretPassword!'
    3. Нажатие кнопки Submit
    4. Проверка появления сообщения об успешном входе
""")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://the-internet.herokuapp.com/login", name="Ссылка на сайт")
def test_successful_login(driver):

    with allure.step("Открыть страницу логина"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Ввести логин 'tomsmith'"):
        user_name = driver.find_element(By.ID, "username")
        user_name.send_keys("tomsmith")

    with allure.step("Ввести пароль 'SuperSecretPassword!'"):
        password = driver.find_element(By.ID, "password")
        password.send_keys("SuperSecretPassword!")

    with allure.step("Нажать кнопку входа"):
        button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button.click()

    with allure.step("Проверить сообщение об успешнов входе"):
        flash = driver.find_element(By.ID, "flash")
        message = flash.text

    assert "You logged into a secure area!" in message, "Ожидали  'You logged into a secure area!'"

@allure.feature("Authentication")
@allure.title("Попытка входа в систему с некорректными значениями")
@allure.description("""
    Тест проверяет авторизацию с некорректными учетными данными
    1. Переход на страницу /login
    2. Ввод логина 'tommy' и пароля 'WrongPassword'
    3. Нажатие кнопки Submit
    4. Проверка появления сообщения об ошибке
""")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://the-internet.herokuapp.com/login", name="Ссылка на сайт")
def test_failed_login(driver):
    with allure.step("Открыть страницу логина"):
        driver.get("https://the-internet.herokuapp.com/login")
        import time
        time.sleep(2)

    with allure.step("Ввести логин 'tommy'"):
        bad_user_name = driver.find_element(By.ID, "username")
        bad_user_name.send_keys("tommy")

    with allure.step("Ввести пароль 'WrongPassword'"):
        bad_password = driver.find_element(By.ID, "password")
        bad_password.send_keys("WrongPassword")

    with allure.step("нажать кнопку входа"):
        button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button.click()

    with allure.step("Проверить сообщение об ошибке"):
        flash = driver.find_element(By.ID, "flash")
        message = flash.text

        assert "invalid" in message, "Ожидали 'Your username is invalid!'"


