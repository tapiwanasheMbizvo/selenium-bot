from booking.booking import Booking

with Booking() as bot:
    bot.landing_page()
    # bot.change_currency(currency='ZAR')
    bot.select_place_to_go("zanzibar")
    bot.select_check_in_and_check_out(check_in_date='2022-06-06', check_out_date='2022-06-11')
    bot.check_travel_for_work()
    bot.select_number_of_adults(count=7)
