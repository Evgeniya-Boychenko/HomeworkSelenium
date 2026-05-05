import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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

def test_successful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    user_name = driver.find_element(By.ID, "username")
    user_name.send_keys("tomsmith")

    password = driver.find_element(By.ID, "password")
    password.send_keys("SuperSecretPassword!")

    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    button.click()

    flash = driver.find_element(By.ID, "flash")
    message = flash.text

    assert "You logged into a secure area!" in message, "Ожидали  'You logged into a secure area!'"

def test_failed_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    bad_user_name = driver.find_element(By.ID, "username")
    bad_user_name.send_keys("tommy")

    bad_password = driver.find_element(By.ID, "password")
    bad_password.send_keys("WrongPassword")

    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    button.click()

    flash = driver.find_element(By.ID, "flash")
    message = flash.text

    assert "invalid" in message, "Ожидали 'Your username is invalid!'"


