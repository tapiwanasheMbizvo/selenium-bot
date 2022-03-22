from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
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

    def submit_search(self):

        btn_submit = self.find_element(
            by=By.CSS_SELECTOR,
            value='button[data-et-click="      customGoal:cCHObTRVDEZRdPQBcGCfTKYCccaT:1 '
                  'goal:www_index_search_button_click  "] '

        )
        btn_submit.click()

    def generate_listing(self):

        elements = self.find_elements(
            by=By.CSS_SELECTOR,
            value='div[data-testid="property-card"]'
        )
        for element in elements:
            # print("WE HAVE ONE")
            title_element = self.find_element(
                by=By.CSS_SELECTOR,
                value='div[data-testid="title"]'
            )

            resort_name = title_element.get_attribute("innerHTML")
            print(f"We have got  {resort_name}")

    def generate_list_one(self):

        columns = ['Resort Name', 'Price', 'Rating']

        list_hotels = []
        list_ratings = []
        list_prices = []
        hotel_boxes = self.find_elements(
            by=By.CSS_SELECTOR,
            value='div[data-testid="property-card"]'
        )

        for hotel in hotel_boxes:
            hotel_name = hotel.find_element(
                by=By.CSS_SELECTOR,
                value='div[data-testid="title"]'
            ).get_attribute("innerHTML").strip()
            hotel_rating = hotel.find_element(
                by=By.CLASS_NAME,
                value='f1cbb919ef'
            ).get_attribute("innerHTML").strip()

            hotel_price = hotel.find_element(
                by=By.CSS_SELECTOR,
                value='div[data-testid="price-and-discounted-price"]'
            ).find_element(
                by=By.TAG_NAME,
                value="span"
            ).get_attribute("innerHTML")

            print(f"We gto {hotel_name} with rating {hotel_rating}")
            print(hotel_price)

            list_hotels.append(hotel_name)
            list_prices.append(hotel_price)
            list_ratings.append(hotel_rating)

        data = {"Hotel Name": list_hotels,
                "Price": list_prices,
                "Rating": list_ratings}

        df = pd.DataFrame(data)

        
        df.to_csv(r"somefile.csv", index=False)
        return df
