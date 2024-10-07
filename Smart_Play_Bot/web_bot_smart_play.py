import argparse
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time


class SmartPlayBot:

    def __init__(self, URL: str, usename: str, password: str, usingDocker: bool) -> None:

        self.URL = URL
        self.options = None
        self.driver = None
        self.usingDocker = usingDocker

        self.HomePage = None
        self.LoginPage = None
        self.username = usename
        self.password = password

        print("\nSmart Play Booking Bot Start ......")

    def set_options(self,
                    keep_alive: bool = False,
                    options_list: list[str] = None):
        """
        Setup driver config

        Args:
            keep_alive: Keep the browser open after run the code
            options_list: A list of arguments for driver config
        """

        self.options = Options()
        if self.usingDocker:
            self.options.add_argument('--ignore-ssl-errors=yes')
            self.options.add_argument('--ignore-certificate-errors')

        if keep_alive:
            self.options.add_experimental_option("detach", True)

        if options_list:
            for option in options_list:
                self.options.add_argument(option)

    def load_driver(self, max_window=True):
        """
        Load chrome driver & Access to URL

        Args:
            max_window: Determine if maximize window
        """
        if self.usingDocker:
            self.driver = webdriver.Remote(
                command_executor='http://172.17.0.3:4444',
                options=self.options
            )
        else:
            self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.URL)

        print(f"\nAccessing to {self.URL}")

        if max_window:
            self.driver.maximize_window()

    def close_driver(self):
        """
        Close the driver
        """
        self.driver.quit()
        print("\nDriver Closed ......")

    def get_login_page(self, wait_time: int = 5, login_button_xpath: str = None):

        try:
            print("\nSearching Login Button ......")

            self.HomePage = self.driver.current_window_handle
            print(f"HomePage: {self.HomePage}")

            LoginButtonElement = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, login_button_xpath))
            )
            self.driver.execute_script(
                "arguments[0].click();", LoginButtonElement)

            print("Redirecting to Login page ......")

        except TimeoutException:
            print(f"\nTimeout. Cannot find the XPATH: {login_button_xpath}")

    def login(self,
              wait_time: int = 5,
              username_xpath: str = None,
              password_xpath: str = None,
              login_button_xpath: str = None,
              IamSmart_button_xpath: str = None):

        print("\nLoad new tab webpage source")

        # Switch driver to new page
        WebDriverWait(self.driver, wait_time).until(
            EC.number_of_windows_to_be(2)
        )

        for window_handle in self.driver.window_handles:
            if window_handle != self.HomePage:
                self.driver.switch_to.window(window_handle)
                break

        self.LoginPage = self.driver.current_window_handle
        print(f"LoginPage: {self.LoginPage}")

        # Use IamSmart Login -- Not support IamSmart Login Now
        if username_xpath is None and password_xpath is None:

            print("\nLoading for iAM Smart Login")

            try:
                # Find & Click IamSmart Login Button
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located(
                        (By.XPATH, IamSmart_button_xpath))
                )

                IamSmartButton = self.driver.find_element(
                    By.XPATH, IamSmart_button_xpath)
                self.driver.execute_script(
                    "arguments[0].click();", IamSmartButton)

            except NoSuchElementException:
                print(f"Cannot find iAM Smart login button xpath: {\
                      IamSmart_button_xpath}")

        # Use username and password Login
        if IamSmart_button_xpath is None:

            UsernameField = self.driver.find_element(By.XPATH, username_xpath)
            UsernameField.send_keys(self.username)

            PasswordField = self.driver.find_element(By.XPATH, password_xpath)
            PasswordField.send_keys(self.password)

            LoginButton = self.driver.find_element(
                By.XPATH, login_button_xpath)
            self.driver.execute_script("arguments[0].click();", LoginButton)

    def search_available_period(self, wait_time: int = 5):

        # Wait for 團體付款 icon
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//img[@data-v-174fb000]"))
        )

        # Load Sport, date, district selection page
        FacultyXPATH = "//span[@data-v-49217096 and text()='設施']"
        WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, FacultyXPATH))
        )
        FacultyButton = self.driver.find_element(By.XPATH, FacultyXPATH)
        self.driver.execute_script("arguments[0].click();", FacultyButton)

        # Select Sport
        InputBarXPATH = "//div[@data-v-429aaa46 and @data-v-012d0593 and @class='text']"
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, InputBarXPATH))
        ).click()

        TextAreaXPATH = "//input[@data-v-21e43f8c and @data-v-42c8b4a0]"
        TextArea = self.driver.find_element(By.XPATH, TextAreaXPATH)
        TextArea.send_keys('乒乓球')

        PingPongXPATH = "//div[@class='search-associate-tab-item']/p[text()='乒乓球']"
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, PingPongXPATH))
        ).click()

        # Select District
        DistrictBarXPATH = "//div[@data-v-5528557e and @class='sp-select-value']"
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, DistrictBarXPATH))
        ).click()

        # Wati for Select dropdown
        DropDownXPATH = "//div[@data-v-5528557e and @class='sp-select-option' and not(contains(@style, 'display: none;'))]"
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, DropDownXPATH))
        )

        DistrictXPATH = "//div[@class='programme-district-box' and .//div[text()='九龍']]"
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, DistrictXPATH))
        ).click()

        # Select Date
        DateInputXPATH = "//input[@type='text' and @class='el-input__inner']"
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, DateInputXPATH))
        ).click()

        DateXPATH = "//td[@class='available free-date' and .//span[normalize-space(text())='13']]"
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, DateXPATH))
        ).click()

        # Search
        SearchButtonXPATH = "//div[@data-v-ff4d1da4 and @role='button' and text()='搜尋']"
        SearchButton = self.driver.find_element(By.XPATH, SearchButtonXPATH)
        self.driver.execute_script("arguments[0].click();", SearchButton)

    def book(self, wait_time: int = 5):

        # Select Time Slot by District
        TimeSlotXPATH = "//h3[@class='venuen-name' and contains(text(), '何文田體育館')]/ancestor::div[@class='el-row chooseTime commonFlex']//div[@data-v-196fdd38 and contains(text(), '乒乓球檯 (空調)(市區)')]/ancestor::div[@class='el-row']//div[@class='time flex' and text()='上午8時']"
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, TimeSlotXPATH))
        )
        TimeSlotButton = self.driver.find_element(By.XPATH, TimeSlotXPATH)
        self.driver.execute_script("arguments[0].click();", TimeSlotButton)
        # self.driver.execute_script("arguments[0].innerText = arguments[1];", TimeSlotButton, "test")

        # Click confirm
        ConfirmTimeXPATH = "//div[@data-v-ff4d1da4 and @role='button' and contains(text(), '繼續')]"
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, ConfirmTimeXPATH))
        )
        ConfirmTimeButton = self.driver.find_element(
            By.XPATH, ConfirmTimeXPATH)

        # Scroll down & click confirm
        prev_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", ConfirmTimeButton)

            time.sleep(1)

            # Calculate new height and compare with the previous height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")

            if new_height == prev_height:
                self.driver.execute_script(
                    "arguments[0].click();", ConfirmTimeButton)
                break  # Exit the loop if no new content is loaded
            prev_height = new_height

        ClosePopupXPATH = "//div[@class='cancel-button' and contains(text(),  '否')]"
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, ClosePopupXPATH))
        )
        ClosePopButton = self.driver.find_element(By.XPATH, ClosePopupXPATH)
        self.driver.execute_script("arguments[0].click();", ClosePopButton)

        ConfirmToPayXPATH = "//div[@data-v-ff4d1da4 and @role='button' and contains(text(), '繼續')]"
        ConfirmTimeButton = self.driver.find_element(
            By.XPATH, ConfirmToPayXPATH)
        self.driver.execute_script(
            "arguments[0].innerText = arguments[1];", ConfirmToPayXPATH, "test")

        # Scroll down & click confirm
        prev_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", ConfirmTimeButton)

            time.sleep(1)

            # Calculate new height and compare with the previous height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")

            if new_height == prev_height:
                self.driver.execute_script(
                    "arguments[0].click();", ConfirmTimeButton)
                break  # Exit the loop if no new content is loaded
            prev_height = new_height

        # Click checkbox
        checkbox_1_XPATH = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='app']/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div[1]/div/div[1]"))
        ).click()

        checkbox_2_XPATH = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='app']/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@data-v-ff4d1da4 and @role='button' and contains(text(), '確認並同意 ')]"))
        ).click()

    def payment(self):

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@data-v-ff4d1da4 and @role='button' and contains(text(), '確認付款')]"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div[2]/div[1]/div/div/div/div[2]/div[7]/div[2]/img"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div[2]/div[1]/div/div/div/div[4]/div[2]/div"))
        ).click()

        print(self.driver.current_url)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/app-root/app-payment-detail-form/div/div/div/div/div[1]/div[2]/form/div[1]/app-payment-method-card-layout/div[2]/app-payment-method-card/div/div/div/div[1]/div/label/span"))
        ).click()

        print(self.driver.current_url)

        CardOwnerXPATH = "/html/body/input[1]"
        CardOwner = self.driver.find_element(By.XPATH, CardOwnerXPATH)
        CardOwner.send_keys('Chan Tai Man')

        CardNumberXPATH = "/html/body/input[2]"
        CardNumber = self.driver.find_element(By.XPATH, CardNumberXPATH)
        CardNumber.send_keys('5423602760838913')

        CardNumberXPATH = "//*[@id='securityCode']"
        CardNumber = self.driver.find_element(By.XPATH, CardNumberXPATH)
        CardNumber.send_keys('903')


if __name__ == "__main__":
    try:
        URL = "https://www.smartplay.lcsd.gov.hk/website/tc/index.html"
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--username", help="Username for login")
        parser.add_argument("-pw", "--password", help="Password for login")
        args = parser.parse_args()

        dockerTesting = input("Are you testing in Docker? (Y/N): ")
        # Setup Driver
        bot = SmartPlayBot(
            URL=URL,
            usename=args.username,
            password=args.password,
            usingDocker=True if dockerTesting.lower() == "y" else False
        )

        SettingOptions = ["--disable-gpu",
                          "--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"]

        bot.set_options(keep_alive=True, options_list=SettingOptions)
        bot.load_driver(max_window=True)

        # Load login page
        LoginButtonXPATH = "//span[@class='btn__inner' and text()='登入']"

        bot.get_login_page(login_button_xpath=LoginButtonXPATH)

        # Login processing

        username_xpath = "//input[@name='pc-login-username']"
        password_xpath = "//input[@name='pc-login-password']"
        login_button_xpath = "//div[contains(text(), '登錄') or contains(text(), 'Login')]"

        bot.login(username_xpath=username_xpath,
                  password_xpath=password_xpath,
                  login_button_xpath=login_button_xpath)

        # Search booking time slot
        bot.search_available_period()

        # Book
        bot.book()

        bot.payment()
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
    finally:
        bot.close_driver()
        sys.exit(0)


#################################################
# All Work (Edited at: 2024/09/25 00:11)
# Input credit card function is not tested yet
# Username & Password omitted!!!!
#################################################
