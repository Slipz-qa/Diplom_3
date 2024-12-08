
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException

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

    def wait_for_element_to_be_clickable(self, locator):
        """
        Ожидает, что элемент будет кликабельным, и возвращает его.
        """
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click_element(self, locator):
        """
        Ожидает, пока элемент станет кликабельным, и кликает по нему.
        """
        element = self.wait_for_element_to_be_clickable(locator)
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()

    def enter_text(self, locator, text):
        """
        Ожидает видимости элемента и вводит текст в соответствующее поле.
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.send_keys(text)

    def scroll_to_element_and_click(self, locator):
        """
        Прокручивает к элементу и кликает по нему.
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()

    def get_element_attribute(self, locator, attribute):
        """
        Получает значение атрибута у элемента.
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.get_attribute(attribute)

    def wait_for_url_contains(self, url_part, timeout=10):
        """
        Ожидает, пока текущий URL не будет содержать указанную подстроку.
        """
        self.wait.until(EC.url_contains(url_part))

    def is_element_present(self, locator, timeout=10):
        """
        Проверяет, что элемент присутствует на странице.
        """
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_url_contains(self, url_part, timeout=10):
        """
        Проверяет, что URL содержит указанную подстроку.
        """
        self.wait.until(EC.url_contains(url_part))
        return url_part in self.browser.current_url

    def scroll_to_element(self, element):
        """
        Прокручивает страницу до элемента.
        """
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)

    def wait_for_element_to_be_visible(self, locator, timeout=10):
        """
        Ожидает, пока элемент не станет видимым.
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def send_keys_to_element(self, locator, keys, timeout=10):
        """
        Ожидает видимости элемента и вводит текст в поле.
        """
        element = self.wait_for_element_to_be_visible(locator, timeout)
        element.send_keys(keys)

    def get_element_text(self, locator, timeout=10):
        """
        Ожидает видимости элемента и извлекает его текст.
        """
        element = self.wait_for_element_to_be_visible(locator, timeout)
        return element.text

    def wait_for_element_to_disappear(self, locator, timeout=10):
        """
        Ожидает, пока элемент исчезнет с DOM.

        :param locator: Локатор элемента.
        :param timeout: Максимальное время ожидания в секундах.
        """
        try:
            self.wait.until_not(EC.presence_of_element_located(locator),
                                message=f"Элемент {locator} не исчез в отведённое время.")
        except TimeoutException:
            raise AssertionError(f"Элемент {locator} не исчез за {timeout} секунд.")

    def wait_for_elements_to_be_present(self, locator, timeout=10):
        """
        Ожидает, пока элементы будут присутствовать на странице.

        :param locator: Локатор элементов.
        :param timeout: Таймаут ожидания.
        :return: Список найденных элементов.
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def wait_for_custom_condition(self, condition, timeout=10):
        """
        Ожидает пользовательского условия.

        :param condition: Лямбда-функция или условие для выполнения.
        :param timeout: Таймаут ожидания.
        """
        WebDriverWait(self.browser, timeout).until(condition)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def get_element_class(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.get_attribute("class")

    def scroll_into_view(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)







