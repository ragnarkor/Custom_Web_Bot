from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from datetime import datetime


from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

class BookingBot:
    
    def __init__(self, driver):
        self.driver = driver

    def _wait_located(self,
                      wait_time = 5,
                      locater = None,
                      _type = "xpath") -> None:

        assert locater != None, "XPath cannot be None"

        if _type == "xpath":
            by = By.XPATH
        elif _type == "class":
            by = By.CLASS_NAME
        else:
            raise ValueError("\nInvalid locator type. Use 'xpath' or 'class_name'.")

        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, locater))
            )

        except TimeoutException:
            raise TimeoutException(f"\nTimeout! Cannot find '{_type}': {locater}") from None
        
    def get_login_page(self):

        login_button_xpath = "/html/body/div[1]/header/div/div/div[2]/div[1]/ul/li[2]/a/span"

        self.driver.maximize_window()
        
        print("Loading to login page")
        self._wait_located(locater=login_button_xpath, _type="xpath")
        LoginButtonElement = self.driver.find_element(By.XPATH, login_button_xpath)
        self.driver.execute_script("arguments[0].click();", LoginButtonElement)

    def login(
        self,
        username = None,
        password = None            
    ):

        username_xpath = "//input[@class='el-input__inner' and @name='pc-login-username']"
        password_xpath = "//input[@type='password' and @name='pc-login-password']"
        login_button_xpath = "/html/body/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div[3]/div"

        ### Switch driver to new page
        self.driver.switch_to.window(self.driver.window_handles[-1])

        time.sleep(1)

        if username and password:
            UsernameField = self.driver.find_element(By.XPATH, username_xpath)
            UsernameField.send_keys(username)

            PasswordField = self.driver.find_element(By.XPATH, password_xpath)
            PasswordField.send_keys(password)

            time.sleep(0.5)

            LoginButtonElement = self.driver.find_element(By.XPATH, login_button_xpath)
            self.driver.execute_script("arguments[0].click();", LoginButtonElement)

            print("Logged in")

    def search_available_period(self, day):

        facility_button_xpath = "/html/body/div/div[1]/div[1]/div/div[1]/div/div[1]/ul/li[2]/div"

        sport_input_field_xpath = "/html/body/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[1]/div/div[1]"
        input_field_xpath = "/html/body/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[1]/div[2]/div[2]/div/div/div[1]/input"
        sport_type_xpath = "//p[@data-v-21e43f8c and @data-v-42c8b4a0 and contains(text(),'乒乓球')]"

        district_input_field_xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[3]/div[2]"
        district_xpath = "//div[@class='programme-district-box' and .//div[text()='九龍']]"

        date_input_field_xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[3]/div[2]"
        _today = datetime.today().day
        if _today == day:
            date_xpath = f"//td[@class='available today free-date' and .//span[normalize-space(text())={day}]]"
        else:
            date_xpath = f"//td[@class='available free-date' and .//span[normalize-space(text())={day}]]"

        search_button_xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[4]/div"

        ### Facility Home Page
        time.sleep(1)
        self._wait_located(locater=facility_button_xpath, _type="xpath")
        FacilityButtonElement = self.driver.find_element(By.XPATH, facility_button_xpath)
        self.driver.execute_script("arguments[0].click();", FacilityButtonElement)

        ### Select Sport Type
        time.sleep(1)
        self._wait_located(locater=sport_input_field_xpath, _type="xpath")
        SportInputFieldElement = self.driver.find_element(By.XPATH, sport_input_field_xpath)
        SportInputFieldElement.click()

        self._wait_located(locater=input_field_xpath, _type="xpath")
        InputFieldElement = self.driver.find_element(By.XPATH, input_field_xpath)
        InputFieldElement.send_keys('乒乓球')

        self._wait_located(locater=sport_type_xpath, _type="xpath")
        SportTypeElement = self.driver.find_element(By.XPATH, sport_type_xpath)
        SportTypeElement.click()
        print("Select Sport Type")

        ### Select District
        time.sleep(1)
        self._wait_located(locater=district_input_field_xpath, _type="xpath")
        DistrictInputFieldElement = self.driver.find_element(By.XPATH, district_input_field_xpath)
        DistrictInputFieldElement.click()

        self._wait_located(locater=district_xpath, _type="xpath")
        DistrictElement = self.driver.find_element(By.XPATH, district_xpath)
        #DistrictElement.click()
        self.driver.execute_script("arguments[0].click();", DistrictElement)
        print("Select District")

        ### Select Date
        time.sleep(1)
        self._wait_located(locater=date_input_field_xpath, _type="xpath")
        DateInputFieldElement = self.driver.find_element(By.XPATH, date_input_field_xpath)
        self.driver.execute_script("arguments[0].click();", DateInputFieldElement)

        self._wait_located(locater=date_xpath, _type="xpath")
        DateElement = self.driver.find_element(By.XPATH, date_xpath)
        self.driver.execute_script("arguments[0].click();", DateElement)
        print("Select Date")

        ### Select Search Button
        SearchButtonElement = self.driver.find_element(By.XPATH, search_button_xpath)
        self.driver.execute_script("arguments[0].click();", SearchButtonElement)
        print("Click Search Button")


        ### All Tested
    def _classify_time(self, timeslot_str):

        hour = int(re.search("\d+", timeslot_str).group())

        if "上午" in timeslot_str:
            return "Morning"
        
        elif "下午" in timeslot_str:
            if (1 <= hour < 6) or (hour == 12):
                return "Afternoon"
            elif 6 <= hour < 12:
                return "Night"

    def select_timeslot(self, timeslot_str, venuen_name):
        morning_button_xpath = "/html/body/div[1]/div[2]/div[4]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[1]"
        afternoon_button_xpath = "/html/body/div[1]/div[2]/div[4]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[2]"
        night_button_xpath = "/html/body/div[1]/div[2]/div[4]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[3]"

        continue_button_xpath = "//div[@data-v-8c95f640 and @class='xp-button xp-primary-d']//div[@tabindex='0' and @role='button']"
        cancel_button_xpath = "//div[@class='dialog-box' and @role='dialog']/div[@class='btn-box']/div[@class='cancel-button' and @role='button']"
        continue2_button_xpath = "/html/body/div/div[2]/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div"

        time_type = self._classify_time(timeslot_str)

        if time_type == "Morning":
            time_type_xpath = morning_button_xpath
            print(f"Click {time_type}")
        elif time_type == "Afternoon":
            time_type_xpath = afternoon_button_xpath
            print(f"Click {time_type}")
        elif time_type == "Night":
            time_type_xpath = night_button_xpath
            print(f"Click {time_type}")

        timeslot_xpath = f"//h3[text()='{venuen_name}']/ancestor::div[contains(@class, 'chooseTime')]//div[contains(text(), '乒乓球檯 (空調)(市區)')]/following-sibling::div//div[contains(text(), '{timeslot_str}')]"
        
        # Click Morning / Afternoon / Night
        time.sleep(2)
        self._wait_located(locater=time_type_xpath, _type="xpath")
        TimeTypeElement = self.driver.find_element(By.XPATH, time_type_xpath)
        TimeTypeElement.click()

        # Click timeslot
        time.sleep(1)
        self._wait_located(locater=timeslot_xpath, _type="xpath")
        TimeslotElement = self.driver.find_element(By.XPATH, timeslot_xpath)
        print("@(#)*@(#*)@")
        self.driver.execute_script("arguments[0].click();", TimeslotElement)


        time.sleep(1)
        self._wait_located(locater=continue_button_xpath, _type="xpath")
        ContinueButtonElement = self.driver.find_element(By.XPATH, continue_button_xpath)
        self.driver.execute_script("arguments[0].click();", ContinueButtonElement)


        time.sleep(1)
        self._wait_located(locater=cancel_button_xpath, _type="xpath")
        CancelButtonElement = self.driver.find_element(By.XPATH, cancel_button_xpath)
        self.driver.execute_script("arguments[0].click();", CancelButtonElement)


        time.sleep(1)
        self._wait_located(locater=continue2_button_xpath, _type="xpath")
        Continue2ButtonElement = self.driver.find_element(By.XPATH, continue2_button_xpath)
        self.driver.execute_script("arguments[0].click();", Continue2ButtonElement)


        # Click checkbox
        checkbox1_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div[1]/div/div[1]/img"
        time.sleep(1)
        self._wait_located(locater=checkbox1_xpath, _type="xpath")
        Checkbox1Element = self.driver.find_element(By.XPATH, checkbox1_xpath)
        Checkbox1Element.click()
        
        # Click checkbox
        checkbox2_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/img"
        self._wait_located(locater=checkbox2_xpath, _type="xpath")
        Checkbox2Element = self.driver.find_element(By.XPATH, checkbox2_xpath)
        Checkbox2Element.click()

        # Continue button
        time.sleep(1)
        confirm_button_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div"
        self._wait_located(locater=confirm_button_xpath, _type="xpath")
        ConfirmButtonElement = self.driver.find_element(By.XPATH, confirm_button_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmButtonElement)

        # Confirm payment
        confirm_payment_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[3]/div[2]/div"
        time.sleep(1)
        self._wait_located(locater=confirm_payment_xpath, _type="xpath")
        ConfirmPaymentButtonElement = self.driver.find_element(By.XPATH, confirm_payment_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmPaymentButtonElement)

    ### Not test
    def payment(self):
        # Mastercard payment
        mastercard_payment_xpath = "/html/body/div/div[2]/div[2]/div/div/div/div[2]/div[7]/div[2]/img"
        time.sleep(5)
        self._wait_located(locater="/html/body/app-root/app-payment-detail-form/div/div/div/div/div[1]/div[2]/app-footer/div/div[2]/img", _type="xpath") # Mastercard Logo
        MastercardPaymentButtonElement = self.driver.find_element(By.XPATH, mastercard_payment_xpath)
        MastercardPaymentButtonElement.click()

        confirm_payment_xpath = "/html/body/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div"
        time.sleep(1)
        self._wait_located(locater=confirm_payment_xpath, _type="xpath")
        ConfirmPaymentButtonElement = self.driver.find_element(By.XPATH, confirm_payment_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmPaymentButtonElement)

        cardholder_xpath = "/html/body/input[1]"
        time.sleep(5)
        self._wait_located(locater=cardholder_xpath, _type="xpath")
        self.driver.find_element(By.XPATH, cardholder_xpath).send_keys("MrTesting")