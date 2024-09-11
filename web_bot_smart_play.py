from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException


class SmartPlayBot:

    def __init__(self, URL:str) -> None:
        
        self.URL = URL
        self.options = None
        self.driver = None

        print("\nSmart Play Booking Bot Start ......")

    def set_options(self,
                    keep_alive:bool = False,
                    options_list:list[str] = None):
        """
        Setup driver config

        Args:
            keep_alive: Keep the browser open after run the code
            options_list: A list of arguments for driver config
        """
        
        self.options = Options()
        
        if keep_alive:
            self.options.add_experimental_option("detach", True)
        
        if options_list:
            for option in options_list:
                self.options.add_argument(option)
    
    def load_driver(self, max_window = True):
        """
        Load chrome driver & Access to URL

        Args:
            max_window: Determine if maximize window
        """
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.URL)

        print(f"\nAccessing to {self.URL}")

        if max_window:
            self.driver.maximize_window()

    def get_login_page(self, wait_time:int = 5, login_button_xpath:str = None):

        try:
            print("\nSearching Login Button ......")

            LoginButtonElement = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, login_button_xpath))
            )
            self.driver.execute_script("arguments[0].click();", LoginButtonElement)

            print("Redirecting to Login page ......")
        
        except TimeoutException:
            print(f"\nTimeout. Cannot find the XPATH: {login_button_xpath}")


if __name__ == "__main__":
    URL = "https://www.smartplay.lcsd.gov.hk/website/tc/index.html"

    bot = SmartPlayBot(URL=URL)

    bot.set_options(keep_alive=True)

    bot.load_driver(max_window=False)

    # <span class="btn__inner"><span class="ico ico--login"></span>登入</span>

    LoginButtonXPATH = "//span[@class='btn__inner']"

    bot.get_login_page(login_button_xpath=LoginButtonXPATH)