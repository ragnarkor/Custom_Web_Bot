#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

# Set UTF-8 encoding for Windows console
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from booking_bot import BookingBot
import yaml
import time
import sys

def extract_config(path):

    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config

def main(
    options_list:list = [],
    keep_alive:bool = False
):

    url = "https://www.smartplay.lcsd.gov.hk/facilities/home"

    options = Options()
    if options_list:
        for option in options_list:
            options.add_argument(option)

    if keep_alive:
        options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.maximize_window()

    config = extract_config("config.yml")
    username = config["username"]
    password = config["password"]
    district = config["district"]
    sport = config["sport"]
    sport_item = config["sport_item"]
    booking_month = config["booking_month"]
    booking_day = config["booking_day"]
    timeslot = config["timeslot"]
    timeslot_list = config["timeslot_list"]
    venue = config["venue"]
    pps_card_num = config["pps_card_num"]
    pps_card_pwd = config["pps_card_pwd"]


    bot = BookingBot(driver)

    # Poll for available period
    while True:
        if bot.search_available_period(booking_month, booking_day, district, sport):
            break
        else:
            print("No available date, waiting 5s and refreshing...")
            time.sleep(5)
            driver.refresh()
            time.sleep(2)  # Wait for page to load

    # driver.get("https://www.smartplay.lcsd.gov.hk/facilities/select/court?venueId=233&fatId=505&venueName=%E5%9C%9F%E7%93%9C%E7%81%A3%E9%AB%94%E8%82%B2%E9%A4%A8&sessionIndex=2&dateIndex=2&playDate=2025-08-22&district=KC&typeCode=BASC&sportCode=BAGM&frmFilterType=&isFree=false")

    bot.select_timeslot(timeslot, venue, sport_item)

    bot.run_with_login_monitor(bot.check_timeslot_availability,timeslot_list, username=username, password=password)
    # Poll for available timeslots
    while True:
        if bot.run_with_login_monitor(bot.check_timeslot_availability,timeslot_list, username=username, password=password):
            break
        else:
            print("No available timeslots, waiting 5s and refreshing...")
            time.sleep(5)
            driver.refresh()
            time.sleep(2)  # Wait for page to load

    bot.run_with_login_monitor(bot.wait_for_booking, username=username, password=password)
    # payment_success = bot.pps_payment(pps_card_num, pps_card_pwd)

    # if payment_success:
    #     print("Payment process completed successfully!")
    #     sys.exit(0) # success
    # else:
    #     print("Payment process failed!")
    #     sys.exit(1) # failure


if __name__ == "__main__":

    options_list = ["--disable-gpu",
                    # "--headless",
                    # "--no-sandbox",
                    # "--disable-dev-shm-usage",
                    "--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"]

    try:
        main(options_list, keep_alive=True)

    except Exception as e:
        try:
            print(f"Error occurred: {e}")
        except UnicodeEncodeError:
            print(f"Error occurred: {repr(e)}")  # Use repr to avoid encoding issues
        
        # Exit with code 2 for unexpected errors (will trigger retry)
        sys.exit(2)