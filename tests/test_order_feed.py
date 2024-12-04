import allure
from pages.LoginPage import LoginPage
from pages.PersonalAccountPage import PersonalAccountPage
from pages.FeedPage import FeedPage
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("Проверка увеличения счетчиков 'Выполнено за всё время' и 'Выполнено за сегодня'")
    def test_check_time_counter(self, browser, test_data):
        login_page = LoginPage(browser)
        personal_account_page = PersonalAccountPage(browser)
        feed_page = FeedPage(browser)

        # Авторизация
        personal_account_page.login(test_data["email"], test_data["password"])

        # Переход в раздел заказов и проверка начальных значений
        feed_page.open_feed()
        total_orders_before = feed_page.get_order_count("all_time")
        today_orders_before = feed_page.get_order_count("today")

        # Создание нового заказа
        feed_page.click_constructor()
        feed_page.drag_and_drop_ingredient("Флюоресцентная булка R2-D3")
        feed_page.drag_and_drop_ingredient("Соус Spicy-X")
        feed_page.drag_and_drop_ingredient("Мясо бессмертных моллюсков Protostomia")
        feed_page.create_order()  # Предполагается, что метод возвращает номер заказа
        feed_page.close_modal_for_order()

        # Проверка счётчиков после создания заказа
        feed_page.open_feed()
        feed_page.refresh_page()
        total_orders_after = feed_page.get_order_count("all_time")
        today_orders_after = feed_page.get_order_count("today")

        # Проверка увеличения счётчиков
        assert total_orders_after > total_orders_before, \
            f"Счётчик 'Выполнено за всё время' не увеличился. Было: {total_orders_before}, стало: {total_orders_after}"
        assert today_orders_after > today_orders_before, \
            f"Счётчик 'Выполнено за сегодня' не увеличился. Было: {today_orders_before}, стало: {today_orders_after}"

    @allure.title("После оформления заказа его номер появляется в разделе В работе")
    def test_order_in_work(self, browser, test_data):
        login_page = LoginPage(browser)
        personal_account_page = PersonalAccountPage(browser)
        feed_page = FeedPage(browser)

        # Авторизация
        personal_account_page.login(test_data["email"], test_data["password"])

        # Переход в раздел заказов
        feed_page.open_feed()

        # Создание нового заказа
        feed_page.click_constructor()
        feed_page.drag_and_drop_ingredient("Флюоресцентная булка R2-D3")
        feed_page.drag_and_drop_ingredient("Соус Spicy-X")
        feed_page.drag_and_drop_ingredient("Мясо бессмертных моллюсков Protostomia")

        # Создание заказа, после чего появляется модальное окно
        feed_page.create_order()
        order_number = feed_page.extract_order_number()
        feed_page.close_modal_for_order()
        personal_account_page.go_to_feed()
        feed_page.refresh_page()
        feed_page.is_order_in_progress(order_number), f"Заказ {order_number} не найден в 'В работе'"

    @allure.title("Заказы пользователя из раздела «История заказов» отображаются на странице «Лента заказов»")
    def test_orders_from_history_displayed_in_feed(self, browser, test_data):
        login_page = LoginPage(browser)
        personal_account_page = PersonalAccountPage(browser)
        feed_page = FeedPage(browser)

        # Авторизация
        personal_account_page.login(test_data["email"], test_data["password"])

        # Переход в раздел заказов
        feed_page.open_feed()

        # Создание нового заказа
        feed_page.click_constructor()
        feed_page.drag_and_drop_ingredient("Флюоресцентная булка R2-D3")
        feed_page.drag_and_drop_ingredient("Соус Spicy-X")
        feed_page.drag_and_drop_ingredient("Мясо бессмертных моллюсков Protostomia")

        # Создание заказа, после чего появляется модальное окно
        feed_page.create_order()
        order_number = feed_page.extract_order_number()
        feed_page.close_modal_for_order()
        personal_account_page.go_to_personal_account()
        personal_account_page.go_to_order_history()
        order_found = feed_page.check_order_in_history(order_number)
        personal_account_page.go_to_feed()
        order_found_in_feed = feed_page.find_order_in_feed(order_number)
        assert order_found_in_feed, f"Заказ {order_number} не найден в ленте заказов."











