from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.common.exceptions import NoSuchElementException

import booking.constants as const


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:/pyhtonDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def landing_page(self):
        self.get(const.ROOT_URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def change_currency(self, currency=None):
        # data-tooltip-text="Choose your currency"
        currency_element = self.find_element(
            by=By.CSS_SELECTOR,
            value='button[data-tooltip-text="Choose your currency"]'
        )
        currency_element.click()

        selected_currency_element = self.find_element(
            by=By.CSS_SELECTOR,
            value=f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(
            by=By.ID,
            value="ss"
        )
        search_field.clear()
        search_field.send_keys(place_to_go)

        place_to_go_element = self.find_element(
            by=By.CSS_SELECTOR,
            value='li[data-i="0"]'
        )

        place_to_go_element.click()

    def select_check_in_and_check_out(self, check_in_date, check_out_date):

        try:
            next_arrow_element = self.find_element(
                by=By.CSS_SELECTOR,
                value='div[data-bui-ref="calendar-next"]'
            )

            next_arrow_element.click()
            next_arrow_element.click()
            next_arrow_element.click()
        except NoSuchElementException:
            print("NO such element for clicking found")

        check_in_date_element = self.find_element(
            by=By.CSS_SELECTOR,
            value=f'td[data-date="{check_in_date}"]'
        )
        check_in_date_element.click()
        check_out_date_element = self.find_element(
            by=By.CSS_SELECTOR,
            value=f'td[data-date="{check_out_date}"]'
        )

        check_out_date_element.click()

    def check_travel_for_work(self):
        travel_for_work_element = self.find_element(
            by=By.CSS_SELECTOR,
            value='label[for="sb_travel_purpose_checkbox"]'
        )
        travel_for_work_element.click()

    def select_number_of_adults(self, count: int):
        btn_add = self.find_element(
            by=By.CSS_SELECTOR,
            value='button[data-bui-ref="input-stepper-add-button"]'
        )
        btn_remove = self.find_element(
            by=By.CSS_SELECTOR,
            value='button[data-bui-ref="input-stepper-subtract-button"]'
        )
        counter_element = self.find_element(
            by=By.ID,
            value="group_adults"
        )
        current_count = counter_element.get_attribute("value")
        while int(current_count) > count:
            # decrease until equal to count
            btn_remove.click()
            current_count = counter_element.get_attribute("value")
            if int(current_count) == count:
                break

        while int(current_count) < count:
            btn_add.click()
            current_count = counter_element.get_attribute("value")
            if int(current_count) == count:
                break
