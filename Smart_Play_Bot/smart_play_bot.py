from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from booking_bot import BookingBot
import yaml

def extract_config(path):

    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config

def main(
    options_list:list = [],
    keep_alive:bool = False
):

    url = "https://www.smartplay.lcsd.gov.hk/website/tc/index.html"

    options = Options()
    if options_list:
        for option in options_list:
            options.add_argument(option)

    if keep_alive:
        options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    config = extract_config(r"C:\web_bot\Web_Bot\Smart_Play_Bot\config.yml")
    username = config["username"]
    password = config["password"]
    district = config["district"]
    sport = config["sport"]
    sport_item = config["sport_item"]
    booking_month = config["booking_month"]
    booking_day = config["booking_day"]
    timeslot = config["timeslot"]
    venue = config["venue"]
    cardholder = config["cardholder"]
    card_num = config["card_num"]
    expiry_month = config["expiry_month"]
    expiry_year = config["expiry_year"]
    security_code = config["security_code"]


    bot = BookingBot(driver)
    bot.get_login_page()
    bot.login(username, password)
    bot.search_available_period(booking_month, booking_day, district, sport)

    driver.get("https://www.smartplay.lcsd.gov.hk/facilities/search-result?district=KC&startDate=2025-08-18&typeCode=BASC&venueCode=&sportCode=BAGM&typeName=%E7%B1%83%E7%90%83&frmFilterType=&venueSportCode=&isFree=false")

    bot.select_timeslot(timeslot, venue, sport_item)
    bot.check_timeslot_availability(timeslot, venue, sport_item)
    bot.wait_for_booking()


    bot.payment(cardholder, card_num, expiry_month, expiry_year, security_code)


if __name__ == "__main__":

    options_list = ["--disable-gpu",
                    # "--headless",
                    # "--no-sandbox",
                    # "--disable-dev-shm-usage",
                    "--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"]

    try:
        main(options_list, keep_alive=True)

    except Exception as e:
        print(e)