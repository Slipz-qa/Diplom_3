import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class WebDriverFactory:
    @staticmethod
    def get_webdriver(browser_name):
        if browser_name == 'firefox':
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service)
        elif browser_name == 'chrome':
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service)
        else:
            raise ValueError(f"Browser '{browser_name}' is not supported")

@pytest.fixture(params=["chrome", "firefox"])
def browser(request):
    browser_name = request.config.getoption("--browser")
    driver = WebDriverFactory.get_webdriver(browser_name)
    driver.maximize_window()
    yield driver
    driver.quit()



# Тестовые данные: логин и пароль
TEST_DATA = {
    "email": "ArtemBarrel@yandex.ru",
    "password": "123456"
}
@pytest.fixture
def test_data():
    """Фикстура для предоставления тестовых данных."""
    return TEST_DATA

def pytest_addoption(parser):
    """Добавляем параметр --browser для выбора браузера."""
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to use for tests"
    )