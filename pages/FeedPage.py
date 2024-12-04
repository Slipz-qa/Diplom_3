from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from pages.BasePage import BasePage
from locators import *
from selenium.webdriver.support.ui import WebDriverWait
import time
import allure
from selenium.common.exceptions import ElementClickInterceptedException





class FeedPage(BasePage):
    @allure.step("Переход на страницу Ленты заказов")
    def open_feed(self):
        feed_link = self.wait.until(
            EC.element_to_be_clickable(FeedPageLocators.FEED_LINK)
        )
        feed_link.click()

    @allure.step("Проверяем, что находимся на странице Ленты заказов")
    def is_feed_page(self):
        return "feed" in self.browser.current_url

    @allure.step("Кликаем на ингредиент для открытия модального окна")
    def click_ingredient(self):
        ingredient = self.wait.until(
            EC.element_to_be_clickable(FeedPageLocators.INGREDIENT_ITEM)
        )
        ingredient.click()

    @allure.step("Проверяем, что модальное окно открыто и видимо")
    def is_modal_open(self):
        try:
            print("Проверяем наличие модального окна...")
            modal = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "Modal_orderBox__1xWdi"))
            )
            self.browser.execute_script("arguments[0].scrollIntoView(true);", modal)
            return modal.is_displayed()
        except Exception as e:
            print(f"Модальное окно не найдено: {e}")
            return False

    @allure.step("Закрываем модальное окно кликом по крестику")
    def close_modal(self):
        try:
            print("Проверяем наличие модального окна...")

            # Ждём появления контейнера модального окна
            self.wait.until(
                EC.presence_of_element_located(FeedPageLocators.CLOSE_MODAL_Wo),
                message="Модальное окно не открылось в отведённое время."
            )
            print("Контейнер модального окна найден.")

            # Ждём и находим кнопку закрытия
            close_button = self.wait.until(
                EC.element_to_be_clickable(FeedPageLocators.CLOSE_BUTTON_X),
                message="Кнопка закрытия не появилась в отведённое время."
            )
            print("Кнопка закрытия найдена.")

            # Скроллим к кнопке и кликаем на неё
            self.browser.execute_script("arguments[0].scrollIntoView(true);", close_button)
            #time.sleep(0.5)  # Короткая пауза для стабильности

            print("Кнопка видима и активна. Выполняем клик.")
            close_button.click()

            # Ждём, пока активный класс исчезнет, что указывает на закрытие окна
            self.wait.until_not(
                EC.presence_of_element_located(FeedPageLocators.ClOSE_BUTTON_FIND),
                message="Модальное окно не закрылось в отведённое время."
            )
            print("Модальное окно успешно закрыто.")

        except Exception as e:
            print(f"Ошибка при закрытии модального окна: {str(e)}")
            raise AssertionError(f"Не удалось закрыть модальное окно: {str(e)}")

    @allure.step("Проверяет, что модальное окно закрыто")
    def is_modal_closed(self):
        try:
            # Проверяем, что класс для открытого окна исчез
            self.wait.until_not(
                EC.presence_of_element_located(FeedPageLocators.ClOSE_BUTTON_FIND)
            )
            print("Модальное окно успешно закрыто.")
            return True
        except Exception as e:
            print(f"Модальное окно не закрылось: {str(e)}")
            return False

    @allure.step("Кликает на 'Конструктор")
    def click_constructor(self):
        constructor_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/"]'))
        )
        constructor_link.click()

    @allure.step("Проверяет, что мы находимся на главной страниц")
    def is_constructor_page(self):
        return self.BASE_URL in self.browser.current_url

    @allure.step("Ожидает, пока элемент станет видимым, и скроллит до него")
    def wait_and_scroll_to_element(self, locator, timeout=10):
        element = WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    @allure.step("Ищет заказ в ленте заказов")
    def find_order_in_feed(self, order_number):
        try:
            orders = self.wait.until(
                EC.presence_of_all_elements_located(OrderHistoryLocators.ORDER_ITEM)
            )
            for order in orders:
                if order_number in order.text:
                    print(f"[LOG] Заказ {order_number} найден в ленте.")
                    return True
            print(f"[LOG] Заказ {order_number} не найден в ленте.")
            return False
        except TimeoutException:
            print("[LOG] Заказы не были найдены вовремя.")
            return False

    @allure.step("Открываем модальное окно с деталями заказа")
    def open_order_modal(self, order_element):
        """
        Открывает модальное окно с деталями заказа.

        :param order_element: Веб-элемент заказа.
        """
        order_element.click()

    @allure.step("Перетаскивает ингредиент в зону сборки")
    def drag_and_drop_ingredient(self, ingredient_name):
        ingredient_locator = (By.XPATH, f"//p[contains(text(), '{ingredient_name}')]")
        ingredient = self.wait_and_scroll_to_element(ingredient_locator)
        drop_zone = self.wait_and_scroll_to_element(FeedPageLocators.DROP_ZONE)

        ActionChains(self.browser).drag_and_drop(ingredient, drop_zone).perform()

    @allure.step("ажимает на кнопку оформления заказа")
    def create_order(self):
        create_order_button = self.wait_and_scroll_to_element(FeedPageLocators.CREATE_ORDER_BUTTON)
        create_order_button.click()

        WebDriverWait(self.browser, 15).until(lambda driver: True)

    @allure.step("Извлекает номер заказа из модального окна")
    def get_order_number(self):
        modal_title = self.wait_and_scroll_to_element(FeedPageLocators.MODAL_TITLE)
        return modal_title.text

    @allure.step("Ожидает, пока элемент исчезнет")
    def wait_for_element_to_disappear(self, locator, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            EC.invisibility_of_element(locator)
        )

    @allure.step("Закрывает модальное окно кликом по крестику, проверяя все состояния")
    def close_modal_for_order(self):
        try:
            print("Проверяем наличие открытого модального окна...")

            # Ждем появления открытого модального окна
            self.wait.until(
                EC.presence_of_element_located(FeedPageLocators.CLOSE_MODAL_W4),
                message="Открытое модальное окно не обнаружено."
            )
            print("Модальное окно найдено.")

            # Находим кнопку закрытия
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".Modal_modal__close__TnseK")),
                message="Кнопка закрытия не появилась или не кликабельна."
            )
            print("Кнопка закрытия найдена.")

            # Скроллим к кнопке, чтобы она попала в зону видимости
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", close_button)
            print("Прокрутка к кнопке выполнена.")

            # Выполняем клик по кнопке закрытия
            try:
                close_button.click()
                print("Клик по кнопке закрытия выполнен.")
            except ElementClickInterceptedException:
                print("Клик по кнопке перехвачен, выполняем JavaScript-клик.")
                self.browser.execute_script("arguments[0].click();", close_button)

            # Ожидаем исчезновения модального окна
            self.wait.until_not(
                EC.presence_of_element_located(FeedPageLocators.CLOSE_MODAL_W4),
                message="Модальное окно не закрылось."
            )
            print("Модальное окно успешно закрыто.")

        except Exception as e:
            print(f"Ошибка при закрытии модального окна: {str(e)}")
            raise AssertionError(f"Не удалось закрыть модальное окно: {str(e)}")

    @allure.step("Извлекает номер заказа из открытого модального окна")
    def extract_order_number(self):
        print("Проверяем наличие открытого модального окна...")
        time.sleep(5) #Это единственный sleep,я пыталась заменить, но остальные не так работают

        # Ждём, пока появится модальное окно с идентификатором заказа
        modal_element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[contains(text(), "идентификатор заказа")]/preceding-sibling::h2')
            ),
            message="Элемент с номером заказа не найден."
        )
        print("Модальное окно найдено и открыто.")

        # Увеличиваем время ожидания для получения реального номера заказа
        max_attempts = 30  # Количество попыток
        for attempt in range(max_attempts):
            order_number = modal_element.text.strip()

            if order_number.isdigit():  # Проверяем, что это настоящий номер заказа
                print(f"Найден номер заказа: {order_number}")
                return order_number

            print(f"Попытка {attempt + 1}/{max_attempts}: Номер пока не сформирован, ждём 2 секунды...")
            WebDriverWait(self.browser, 2).until(lambda driver: True)  # Ждём перед следующей проверкой

        raise AssertionError("Настоящий номер заказа не был получен в отведённое время.")

    @allure.step("Переходит в личный кабинет и проверяет наличие заказа в истории")
    def check_order_in_history(self, order_number):
        # Убедимся, что искомый номер всегда формируется корректно
        search_order_number = f"#0{order_number.lstrip('#0')}"  # Очищаем лишние префиксы перед добавлением
        print(f"[LOG] Переходим в историю заказов для поиска заказа: {search_order_number}...")

        # Открываем раздел "История заказов"
        history_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="История заказов"]')),
            message="Кнопка 'История заказов' не найдена или не кликабельна."
        )
        history_button.click()

        # Находим список заказов
        order_list = self.browser.find_element(By.CLASS_NAME, "OrderHistory_profileList__374GU")

        # Цикл для прокрутки и поиска заказа
        attempts = 0
        max_attempts = 3  # Ограничиваем количество попыток
        while attempts < max_attempts:
            try:
                print(f"[LOG] Попытка {attempts + 1} поиска заказа {search_order_number}...")

                # Проверяем, появился ли заказ с нужным номером
                element = self.browser.find_element(By.XPATH, f'//p[text()="{search_order_number}"]')
                print(f"[LOG] Заказ с номером {search_order_number} найден в истории!")
                return True  # Если нашли заказ, выходим из функции
            except:
                # Если не нашли, продолжаем скроллить
                print(f"[LOG] Заказ с номером {search_order_number} не найден, прокручиваем дальше...")
                self.browser.execute_script("arguments[0].scrollTop += 300;", order_list)

                # Ждем немного, чтобы дать странице обновиться
                WebDriverWait(self.browser, 2).until(lambda driver: True)
                attempts += 1

        # Если цикл завершился, а заказ не найден
        raise AssertionError(
            f"[LOG] Заказ с номером {search_order_number} не найден в истории после {max_attempts} попыток.")

    @allure.step("Проверяет, что заказ отображается в разделе 'В работе'")
    def is_order_in_progress(self, order_number):
        orders = self.browser.find_elements(
            By.CSS_SELECTOR, "li.text.text_type_digits-default.mb-2"
        )
        return any(order.text == order_number for order in orders)

    @allure.step("Обновляет текущую страницу")
    def refresh_page(self):

        self.browser.refresh()

    @allure.step("Получает количество заказов из счётчиков")
    def get_order_count(self, counter_type):
        if counter_type == "all_time":
            element = self.wait_and_scroll_to_element(FeedPageLocators.ALL_TIME_ORDER_COUNT)
            return int(element.text)

        elif counter_type == "today":
            element = self.wait_and_scroll_to_element(FeedPageLocators.TODAY_ORDER_COUNT)
            return int(element.text)

    def get_counter(self):
        """
        Возвращает текущее значение каунтера ингредиента.

        :return: Значение каунтера как целое число.
        """
        try:
            # Получаем значение каунтера и пытаемся преобразовать его в целое число
            return int(self.get_ingredient_counter(FeedPageLocators.INGREDIENT_COUNTER))
        except ValueError:
            # Если текст каунтера нельзя преобразовать в число, возвращаем 0
            return 0
        except Exception as e:
            # В случае других ошибок (например, если элемент не найден), можно логировать ошибку или вернуть 0
            print(f"Error occurred while getting the counter: {e}")
            return 0

    @allure.step("Находит элемент заказа")
    def find_order_element(self):
        """
        Находит первый элемент заказа на странице.

        :return: Веб-элемент заказа.
        """
        return self.browser.find_element(*FeedPageLocators.ORDER_ITEM)

    @allure.step("Проверяем, что модальное окно с деталями заказа открылось")
    def is_order_modal_open(self):
        """
        Проверяет, что модальное окно с деталями заказа открыто.

        :return: True, если модальное окно отображается.
        """
        return self.browser.find_element(*FeedPageLocators.ORDER_MODAL).is_displayed()




