import allure
from pages.LoginPage import LoginPage
from pages.PersonalAccountPage import PersonalAccountPage


@allure.feature("Личный кабинет")
class TestPersonalAccount:

    @allure.title("Логин через личный кабинет")
    def test_go_to_personal_account(self, browser, test_data):
        personal_account_page = PersonalAccountPage(browser)

        # Используем метод логина из PersonalAccountPage
        personal_account_page.login(test_data["email"], test_data["password"])

        assert personal_account_page.is_main_page(), "Не удалось перейти на главную страницу после входа"

    @allure.title("Вход в личный кабинет")
    def test_login_to_personal_account(self, browser, test_data):
        personal_account_page = PersonalAccountPage(browser)

        # Используем метод логина из PersonalAccountPage
        personal_account_page.login(test_data["email"], test_data["password"])

        personal_account_page.go_to_personal_account()
        assert personal_account_page.is_personal_account_page(), "Не удалось перейти в Личный кабинет"

    @allure.title("Переход на Историю заказов")
    def test_go_to_history(self, browser, test_data):
        personal_account_page = PersonalAccountPage(browser)

        # Используем метод логина из PersonalAccountPage
        personal_account_page.login(test_data["email"], test_data["password"])

        personal_account_page.go_to_personal_account()

        personal_account_page.go_to_order_history()

        assert personal_account_page.is_oder_history_page(), "Не удалось перейти в Историю заказов"



    @allure.title("Выход из личного кабинета")
    def test_logout(self, browser, test_data):
        """
        Тест проверяет успешный выход из личного кабинета после авторизации.
        """
        personal_account_page = PersonalAccountPage(browser)
        login_page = LoginPage(browser)

        # Логинимся через личный кабинет
        personal_account_page.login(test_data["email"], test_data["password"])

        login_page.go_to_personal_account()

        # Выходим из аккаунта
        personal_account_page.logout()

        # Проверяем, что мы на странице входа
        assert login_page.is_login_page(), "Не удалось выйти из аккаунта"






