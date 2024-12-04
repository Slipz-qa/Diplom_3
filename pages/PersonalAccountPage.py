from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from pages.BasePage import BasePage
from locators import *
from selenium.webdriver.support.ui import WebDriverWait
import allure
from pages.LoginPage import LoginPage


class PersonalAccountPage(BasePage):
    @allure.step("Проверяем, находимся ли мы на главной странице")
    def is_main_page(self):
        return self.BASE_URL in self.browser.current_url

    @allure.step("Переход на Ленту заказов")
    def go_to_feed(self):
        # Ожидаем, пока элемент станет видимым и кликабельным
        feed_link = WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/feed"]'))
        )
        # Прокручиваем к элементу (если нужно)
        self.browser.execute_script("arguments[0].scrollIntoView(true);", feed_link)

        WebDriverWait(self.browser, 2).until(lambda driver: True)
        # Кликаем на элемент
        feed_link.click()

    @allure.step("Проверяем, что мы находимся на странице ленты заказов")
    def is_feed_page(self):
        return "feed" in self.browser.current_url

    @allure.step("Проверяем, что мы находимся на странице восстановления пароля")
    def is_recovery_page(self):
        return "forgot" in self.browser.current_url

    @allure.step("Проверяем, что мы находимся на странице смены пароля")
    def is_reset_page(self):
        WebDriverWait(self.browser, 10).until(
            EC.url_contains("reset-password")
        )
        current_url = self.browser.current_url
        allure.attach(body=f"Текущий URL: {current_url}", name="Current URL",
                      attachment_type=allure.attachment_type.TEXT)
        return "reset-password" in current_url


    @allure.step("Переход в Личный кабинет")
    def go_to_personal_account(self):
        account_link = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(AccountPageLocators.ACCOUNT_BUTTON)
        )
        account_link.click()
        # Ожидаем, пока не перейдёт на страницу личного кабинета
        WebDriverWait(self.browser, 10).until(
            EC.url_contains("/account/profile")
        )

    @allure.step("Проверяем, что мы на странице Личного кабинета")
    def is_personal_account_page(self):
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="/account/profile"]'))
        )
        return "account/profile" in self.browser.current_url

    @allure.step("Выход из аккаунта")
    def logout(self):
        # Ожидаем появления и доступности кнопки выхода
        logout_button = WebDriverWait(self.browser, 15).until(
            EC.element_to_be_clickable(AccountPageLocators.LOGOUT_BUTTON)
        )

        # Прокручиваем к кнопке, чтобы убедиться, что она в зоне видимости
        self.browser.execute_script("arguments[0].scrollIntoView(true);", logout_button)

        # Ждем, пока кнопка станет видимой
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of(logout_button)
        )

        # Кликаем на кнопку выхода
        logout_button.click()

        # Убедимся, что мы вернулись на страницу логина
        WebDriverWait(self.browser, 10).until(
            EC.url_contains("login")
        )

    @allure.step("Ввод пароля")
    def enter_password(self, password):
        password_field = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(AccountPageLocators.PASSWORD_FIELD)
        )
        password_field.send_keys(password)

    @allure.step("Переходит в историю заказов и извлекает номер заказа")
    def go_to_order_history(self):
        # Ожидание кликабельности ссылки "История заказов"
        history_link = self.wait.until(
            EC.element_to_be_clickable(AccountPageLocators.ORDER_HISTORY_LINK)
        )
        # Скроллим к элементу и кликаем по нему
        self.browser.execute_script("arguments[0].scrollIntoView(true);", history_link)
        history_link.click()

        # Ожидаем появления элемента заказа и логируем номер заказа
        order_item = self.wait.until(
            EC.presence_of_element_located(OrderHistoryLocators.ORDER_ITEM)
        )
        order_number = order_item.find_element(*OrderHistoryLocators.ORDER_NUMBER).text
        print(f"[LOG] Найден номер заказа: {order_number}")
        return order_number

    @allure.step("Получение номера заказа из истории")
    def get_order_number(self):
        try:
            order = self.wait.until(
                EC.presence_of_element_located(OrderHistoryLocators.ORDER_TEXTBOX)
            )
            order_number = order.find_element(OrderHistoryLocators.ORDER_NUMBER).text
            print(f"[LOG] Найден номер заказа: {order_number}")
            return order_number
        except TimeoutException:
            print("[LOG] Не удалось найти номер заказа.")
            return None

    def login(self, email, password):
        """Метод для выполнения логина в личный кабинет"""
        login_page = LoginPage(self.browser)  # Используем уже доступный self.browser
        login_page.open_base_url()
        login_page.go_to_personal_account()
        login_page.enter_email(email)
        self.enter_password(password)  # Используем метод текущего класса
        login_page.submit_login()

    @allure.step("Проверяем, что мы находимся на странице ленты заказов")
    def is_oder_history_page(self):
        return "history" in self.browser.current_url