from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SmartPlayBot:

    def __init__(self, URL:str) -> None:
        
        self.URL = URL
        self.options = None
        self.driver = None

        self.HomePage = None
        self.LoginPage = None

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

            self.HomePage = self.driver.current_window_handle
            print(f"HomePage: {self.HomePage}")

            LoginButtonElement = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, login_button_xpath))
            )
            self.driver.execute_script("arguments[0].click();", LoginButtonElement)

            print("Redirecting to Login page ......")
        
        except TimeoutException:
            print(f"\nTimeout. Cannot find the XPATH: {login_button_xpath}")

    def login(self,
              wait_time:int = 5,
              username_xpath:str = None,
              password_xpath:str = None,
              login_button_xpath:str = None,
              IamSmart_button_xpath:str = None):

        print("\nLoad new tab webpage source")

        ### Switch driver to new page
        WebDriverWait(self.driver, wait_time).until(
            EC.number_of_windows_to_be(2)
        )

        for window_handle in self.driver.window_handles:
            if window_handle != self.HomePage:
                self.driver.switch_to.window(window_handle)
                break

        self.LoginPage = self.driver.current_window_handle
        print(f"LoginPage: {self.LoginPage}")
        
        ### Use IamSmart Login
        if username_xpath is None and password_xpath is None:

            print("\nLoading for iAM Smart Login")

            try:
                ### Find & Click IamSmart Login Button
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.XPATH, IamSmart_button_xpath))
                )

                IamSmartButton = self.driver.find_element(By.XPATH, IamSmart_button_xpath)
                self.driver.execute_script("arguments[0].click();", IamSmartButton)

            except NoSuchElementException:
                print(f"Cannot find iAM Smart login button xpath: {IamSmart_button_xpath}")


        ### Use username and password Login
        if IamSmart_button_xpath is None:

            UsernameField = self.driver.find_element(By.XPATH, username_xpath)
            UsernameField.send_keys("GG1234")

            PasswordField = self.driver.find_element(By.XPATH, password_xpath)
            PasswordField.send_keys("GG1234")


            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, login_button_xpath))
            )

            LoginButton = self.driver.find_element(By.XPATH, login_button_xpath)
            self.driver.execute_script("arguments[0].click();", LoginButton)

    def booking(self, wait_time:int = 200):

        self.driver.switch_to.window(self.driver.window_handles[-1])

        print(self.driver.window_handles)

        # FacultyXPATH = "//span[@class='weight-bold']"

        # WebDriverWait(self.driver, wait_time).until(
        #     EC.element_to_be_clickable((By.XPATH, FacultyXPATH))
        # )

        # FacultyButton = self.driver.find_element(By.XPATH, FacultyXPATH)
        # self.driver.execute_script("arguments[0].click();", FacultyButton)


if __name__ == "__main__":
    URL = "https://www.smartplay.lcsd.gov.hk/website/tc/index.html"

    ### Setup Driver
    bot = SmartPlayBot(URL=URL)

    bot.set_options(keep_alive=True)

    bot.load_driver(max_window=True)


    ### Load login page
    LoginButtonXPATH = "//span[@class='btn__inner']"

    bot.get_login_page(login_button_xpath=LoginButtonXPATH)


    ### Login processing
    IamSmart_button_xpath = "//div[@class='smart']"
    bot.login(IamSmart_button_xpath=IamSmart_button_xpath)

    # username_xpath = "//input[@name='pc-login-username']"
    # password_xpath = "//input[@name='pc-login-password']"
    # login_button_xpath = "//div[contains(text(), '登錄') or contains(text(), 'Login')]"

    # bot.login(username_xpath=username_xpath,
    #           password_xpath=password_xpath,
    #           login_button_xpath=login_button_xpath)



    ### Booking processing
    bot.booking()