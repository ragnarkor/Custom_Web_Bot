from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from booking_bot import BookingBot

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

    bot = BookingBot(driver)
    bot.get_login_page()
    bot.login("123", "1231231231")
    bot.search_available_period()


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