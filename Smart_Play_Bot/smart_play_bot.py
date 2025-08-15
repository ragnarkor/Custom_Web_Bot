#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

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
    bot.get_login_page()
    bot.login(username, password)
    bot.search_available_period(booking_month, booking_day, district, sport)

    # driver.get("https://www.smartplay.lcsd.gov.hk/facilities/search-result?district=KC&startDate=2025-08-22&typeCode=BASC&venueCode=&sportCode=BAGM&typeName=%E7%B1%83%E7%90%83&frmFilterType=&venueSportCode=&isFree=false")

    bot.select_timeslot(timeslot, venue, sport_item)
    
    # Poll for available timeslots
    while True:
        if bot.check_timeslot_availability(timeslot_list):
            print("Available timeslots found, proceeding to booking")
            break
        else:
            print("No available timeslots, waiting 1 minute and refreshing...")
            time.sleep(60)
            driver.refresh()
            time.sleep(2)  # Wait for page to load
    
    bot.wait_for_booking()


    print("Starting payment process...")
    bot.pps_payment(pps_card_num, pps_card_pwd)
    print("Payment process completed successfully!")


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