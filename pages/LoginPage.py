from selenium.webdriver.support import expected_conditions as EC
from pages.BasePage import BasePage
from locators import *
import allure


class LoginPage (BasePage):
    @allure.step("Переход на страницу восстановления пароля")
    def go_to_forgot_password(self):
        forgot_password_link = self.wait.until(
            EC.element_to_be_clickable(LoginPageLocators.FORGOT_PASSWORD_LINK)
        )
        forgot_password_link.click()

    @allure.step("Ввод email: {email}")
    def enter_email(self, email):
        email_field = self.wait.until(
            EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)
        )
        email_field.send_keys(email)

    @allure.step("Клик на кнопку 'Восстановить'")
    def submit_recovery(self):
        recover_button = self.wait.until(
            EC.element_to_be_clickable(LoginPageLocators.RECOVER_BUTTON)
        )
        recover_button.click()

    @allure.step("Ввод пароля")
    def enter_password(self, password):
        password_field = self.wait.until(
            EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)

    @allure.step("Прокручивает к иконке и кликает на неё")
    def toggle_password_visibility(self):
        show_icon = self.wait.until(
            EC.element_to_be_clickable(LoginPageLocators.SHOW_PASSWORD_ICON)
        )
        self.browser.execute_script("arguments[0].scrollIntoView(true);", show_icon)
        show_icon.click()

    @allure.step("Возвращает значение атрибута 'type' у поля пароля.")
    def get_password_input_type(self):
        password_field = self.wait.until(
            EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)
        )
        return password_field.get_attribute("type")

    @allure.step("Получение класса контейнера поля пароля")
    def get_password_container_class(self):
        container = self.wait.until(
            EC.visibility_of_element_located(LoginPageLocators.PASSWORD_CONTAINER)
        )
        return container.get_attribute("class")

    @allure.step("Переход в личный кабинет")
    def go_to_personal_account(self):
        account_button = self.wait.until(
            EC.element_to_be_clickable(AccountPageLocators.ACCOUNT_BUTTON)
        )
        account_button.click()

    @allure.step("Клик на кнопку 'Войти'")
    def submit_login(self):
        login_button = self.wait.until(
            EC.element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON)
        )
        login_button.click()

    @allure.step("Проверка, что мы находимся на странице логина")
    def is_login_page(self):
        return "login" in self.browser.current_url