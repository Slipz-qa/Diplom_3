from selenium.webdriver.support.ui import WebDriverWait
import allure

class BasePage:
    BASE_URL = "https://stellarburgers.nomoreparties.site"

    def __init__(self, browser):
        """
        Инициализация базовой страницы.

        :param browser: Экземпляр WebDriver.
        """
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    @allure.step("Открываем URL: {url}")
    def open(self, url):
        self.browser.get(url)

    @allure.step("Открываем базовый URL")
    def open_base_url(self):
        """
        Открывает базовый URL.
        """
        self.browser.get(self.BASE_URL)

    def get_ingredient_counter(self, ingredient_locator):
        """
        Получает значение каунтера ингредиента.

        :param ingredient_locator: Локатор элемента с каунтером ингредиента.
        :return: Значение каунтера как строка.
        """
        counter_element = self.find_element(ingredient_locator)
        return counter_element.text

    def find_element(self, locator):
        """
        Находит элемент по локатору.

        :param locator: Кортеж, содержащий тип локатора и его значение, например (By.XPATH, "//div").
        :return: WebElement.
        """
        return self.browser.find_element(*locator)  # Здесь исправлено с `self.driver` на `self.browser`


