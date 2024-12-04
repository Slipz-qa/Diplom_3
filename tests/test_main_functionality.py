import allure
from pages.LoginPage import LoginPage
from pages.PersonalAccountPage import PersonalAccountPage
from pages.FeedPage import FeedPage



@allure.feature("Переходы: Конструктор и Лента заказов")
class TestConstructorAndFeed:

    @allure.title("Переход в Конструктор")
    def test_go_to_constructor(self, browser,test_data):
        login_page = LoginPage(browser)
        personal_account_page = PersonalAccountPage(browser)
        feed_page = FeedPage(browser)
        personal_account_page.login(test_data["email"], test_data["password"])
        feed_page.click_constructor()
        assert feed_page.is_constructor_page(), "Не удалось перейти в Конструктор"


    @allure.title("Переход в Ленту заказов")
    def test_go_to_feed(self, browser,test_data):
        login_page = LoginPage(browser)
        personal_account_page = PersonalAccountPage(browser)
        feed_page = FeedPage(browser)
        personal_account_page.login(test_data["email"], test_data["password"])
        feed_page.open_feed()
        assert feed_page.is_feed_page(), "Не удалось перейти на Ленту заказов"


    @allure.title("Клик по ингредиенту и проверка модального окна")
    def test_click_ingredient_and_check_modal(self, browser,test_data):
        login_page = LoginPage(browser)
        personal_account_page = PersonalAccountPage(browser)
        feed_page = FeedPage(browser)
        personal_account_page.login(test_data["email"], test_data["password"])
        feed_page.open_feed()
        feed_page.click_ingredient()
        assert feed_page.is_modal_open(), "Модальное окно не открылось"

    @allure.title("Закрытие модального окна")
    def test_close_modal_window(self, browser,test_data):
        login_page = LoginPage(browser)
        personal_account_page = PersonalAccountPage(browser)
        feed_page = FeedPage(browser)
        personal_account_page.login(test_data["email"], test_data["password"])
        feed_page.open_feed()
        feed_page.click_ingredient()
        feed_page.close_modal()
        assert feed_page.is_modal_closed(), "Модальное окно не закрылось"

    @allure.title("Создание заказа")
    def test_create_order(self, browser,test_data):
        login_page = LoginPage(browser)
        personal_account_page = PersonalAccountPage(browser)
        feed_page = FeedPage(browser)
        personal_account_page.login(test_data["email"], test_data["password"])
        feed_page.open_feed()
        feed_page.click_constructor()
        feed_page.drag_and_drop_ingredient("Флюоресцентная булка R2-D3")
        feed_page.drag_and_drop_ingredient("Соус Spicy-X")
        feed_page.drag_and_drop_ingredient("Мясо бессмертных моллюсков Protostomia")
        feed_page.create_order()
        order_number = feed_page.extract_order_number()
        assert order_number, "Номер заказа не отображается"
        print(f"Номер заказа: {order_number}")

    @allure.title("Увеличение каунтера")
    def test_check_counters(self, browser, test_data):
        login_page = LoginPage(browser)
        personal_account_page = PersonalAccountPage(browser)
        feed_page = FeedPage(browser)

        personal_account_page.login(test_data["email"], test_data["password"])

        feed_page.click_constructor()

        initial_counter = feed_page.get_counter()

        feed_page.drag_and_drop_ingredient("Флюоресцентная булка R2-D3")
        feed_page.drag_and_drop_ingredient("Соус Spicy-X")
        feed_page.drag_and_drop_ingredient("Мясо бессмертных моллюсков Protostomia")

        final_counter = feed_page.get_counter()

        assert final_counter == initial_counter + 2, \
            f"Ожидалось, что каунтер увеличится на 2, но было {final_counter - initial_counter}."







