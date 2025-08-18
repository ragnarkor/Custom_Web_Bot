from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import time
import re
from datetime import datetime

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
        """ Load Smartplay Homepage and Redirect to Login Page """

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
        """ Input user account info and Login """

        username_xpath = "//input[@class='el-input__inner' and @name='pc-login-username']"
        password_xpath = "//input[@type='password' and @name='pc-login-password']"
        login_button_xpath = "//div[@data-v-8c95f640='' and @role='button']"

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

    def login_in_process(self, username=None, password=None):
        """ Input user account info and Login """

        username_xpath = "//input[@class='el-input__inner' and @name='pc-login-username']"
        password_xpath = "//input[@type='password' and @name='pc-login-password']"
        login_button_xpath = "//div[@data-v-8c95f640='' and @role='button' and contains(text(), '登入')]"

        if username and password:
            UsernameField = self.driver.find_element(By.XPATH, username_xpath)
            UsernameField.clear()
            UsernameField.send_keys(username)

            PasswordField = self.driver.find_element(By.XPATH, password_xpath)
            PasswordField.clear()
            PasswordField.send_keys(password)

            time.sleep(0.5)

            LoginButtonElement = self.driver.find_element(By.XPATH, login_button_xpath)
            self.driver.execute_script("arguments[0].click();", LoginButtonElement)

            print("Logged in")

    def search_available_period(self, month:int, day:int, district:str, sport:str):
        """ Redirect to timeslot selection page by given month, day """

        month, day = int(month), int(day)

        sport_input_field_xpath = "/html/body/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[1]/div/div[1]"
        input_field_xpath = "/html/body/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[1]/div[2]/div[2]/div/div/div[1]/input"
        sport_type_xpath = f"//p[@data-v-21e43f8c and @data-v-42c8b4a0 and contains(text(),'{sport}')]"

        district_input_field_xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[3]/div[2]"
        district_xpath = f"//div[@class='programme-district-box' and .//div[text()='{district}']]"

        date_input_field_xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[3]/div[2]"

        _today = datetime.today()
        input_date = datetime(_today.year, month, day)

        if input_date.month > _today.month:
            date_xpath = f"//td[@class='next-month free-date' and .//span[normalize-space(text())={day}]]"
        elif input_date.day == _today.day:
            date_xpath = f"//td[@class='available today free-date' and .//span[normalize-space(text())={day}]]"
        else:
            date_xpath = f"//td[@class='available free-date' and .//span[normalize-space(text())={day}]]"

        search_button_xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[4]/div"

        ### Select Sport Type
        time.sleep(1)
        self._wait_located(locater=sport_input_field_xpath, _type="xpath")
        SportInputFieldElement = self.driver.find_element(By.XPATH, sport_input_field_xpath)
        SportInputFieldElement.click()

        self._wait_located(locater=input_field_xpath, _type="xpath")
        InputFieldElement = self.driver.find_element(By.XPATH, input_field_xpath)
        InputFieldElement.send_keys(sport)

        self._wait_located(locater=sport_type_xpath, _type="xpath")
        SportTypeElement = self.driver.find_element(By.XPATH, sport_type_xpath)
        SportTypeElement.click()


        ### Select District
        time.sleep(1)
        self._wait_located(locater=district_input_field_xpath, _type="xpath")
        DistrictInputFieldElement = self.driver.find_element(By.XPATH, district_input_field_xpath)
        DistrictInputFieldElement.click()

        self._wait_located(locater=district_xpath, _type="xpath")
        DistrictElement = self.driver.find_element(By.XPATH, district_xpath)
        self.driver.execute_script("arguments[0].click();", DistrictElement)

        ### Select Date
        try:
            time.sleep(1)
            self._wait_located(locater=date_input_field_xpath, _type="xpath")
            DateInputFieldElement = self.driver.find_element(By.XPATH, date_input_field_xpath)
            self.driver.execute_script("arguments[0].click();", DateInputFieldElement)

            self._wait_located(locater=date_xpath, _type="xpath")
            DateElement = self.driver.find_element(By.XPATH, date_xpath)
            self.driver.execute_script("arguments[0].click();", DateElement)

        except Exception as e:
            return False


        ### Select Search Button
        SearchButtonElement = self.driver.find_element(By.XPATH, search_button_xpath)
        self.driver.execute_script("arguments[0].click();", SearchButtonElement)
        
        print("Click Search Button")
        return True

    def _classify_time(self, timeslot_str:str):
        """ Categorize timeslot_str into [Morning, Afternoon, Night] for redirection"""

        hour = int(re.search("\d+", timeslot_str).group())

        if "上午" in timeslot_str:
            return "Morning"
        
        elif "下午" in timeslot_str:
            if (1 <= hour < 6) or (hour == 12):
                return "Afternoon"
            elif 6 <= hour < 12:
                return "Night"

    def select_timeslot(self, timeslot_str:str, venuen_name:str, sport_item:str):
        """ Select the time and venuen """

        morning_button_xpath = "/html/body/div[1]/div[2]/div[4]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[1]"
        afternoon_button_xpath = "/html/body/div[1]/div[2]/div[4]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[2]"
        night_button_xpath = "/html/body/div[1]/div[2]/div[4]/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[3]"

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


        timeslot_xpath = f"//h3[text()='{venuen_name}']/ancestor::div[contains(@class, 'chooseTime')]//div[contains(text(), '{sport_item}')]/following-sibling::div//div[contains(text(), '{timeslot_str}')]"
        
        # Click Morning / Afternoon / Night
        time.sleep(2)
        self._wait_located(locater=time_type_xpath, _type="xpath")
        TimeTypeElement = self.driver.find_element(By.XPATH, time_type_xpath)
        TimeTypeElement.click()

        # Click timeslot
        time.sleep(1)
        self._wait_located(locater=timeslot_xpath, _type="xpath")
        TimeslotElement = self.driver.find_element(By.XPATH, timeslot_xpath)
        self.driver.execute_script("arguments[0].click();", TimeslotElement)
        print(f"Click {timeslot_str}")

    def _clear_selected_sessions(self):
        """ Clear selected session states """
        time.sleep(1)
        
        # Find elements with session-tag-box-select class
        session_elements_xpath = "//div[contains(@class, 'session-tag-box-select')]"
        
        try:
            self._wait_located(locater=session_elements_xpath, _type="xpath")
        except:
            print("No selected element")
            return
        
        # Get all matching elements
        session_elements = self.driver.find_elements(By.XPATH, session_elements_xpath)
        
        if session_elements:
            # Click each element
            for i, element in enumerate(session_elements):
                self.driver.execute_script("arguments[0].click();", element)
                time.sleep(0.5)
        else:
            print("Clear all selected elements")
            return

    def check_timeslot_availability(self, timeslot_list:list):
        """ Check the timeslot availability """

        continue_button_xpath = "//div[@data-v-8c95f640 and @class='xp-button xp-primary-d']//div[@tabindex='0' and @role='button']"

        self._clear_selected_sessions()

        i = 0
        while i < len(timeslot_list):
            current_timeslot_group = timeslot_list[i]
            
            # Check availability of all timeslots in current group
            all_available = True
            time_elements = []
            
            for timeslot in current_timeslot_group:
                # Find time element with class="time" starting with current timeslot
                time_xpath = f"//div[@class='time' and starts-with(text(), '{timeslot}')]"
                
                time_element = self.driver.find_element(By.XPATH, time_xpath)
                time_elements.append(time_element)
                
                # Check if sibling element has session-tag-box-disabled class
                sibling_xpath = f"{time_xpath}/following-sibling::*[1]"
                sibling_element = self.driver.find_element(By.XPATH, sibling_xpath)
                
                if "session-tag-box-disabled" in sibling_element.get_attribute("class"):
                    all_available = False
                    break
            
            # If all timeslots available, click their sibling elements and exit
            if all_available and time_elements:
                
                for j, time_element in enumerate(time_elements):
                    # Find sibling element (target button)
                    sibling_xpath = f"//div[@class='time' and starts-with(text(), '{current_timeslot_group[j]}')]/following-sibling::*[1]"
                    sibling_element = self.driver.find_element(By.XPATH, sibling_xpath)
                    self.driver.execute_script("arguments[0].click();", sibling_element)
                    time.sleep(0.5)

                # Click continue button
                time.sleep(1)
                self._wait_located(locater=continue_button_xpath, _type="xpath")
                ContinueButtonElement = self.driver.find_element(By.XPATH, continue_button_xpath)
                self.driver.execute_script("arguments[0].click();", ContinueButtonElement)
                print(f"Available group: {current_timeslot_group}")

                time.sleep(1)
                break
            else:
                i += 1
        
        if i >= len(timeslot_list):
            return False
        
        return True

    def wait_for_booking(self):
        """ Wait for booking """
        cancel_button_xpath = "//div[@class='dialog-box' and @role='dialog']/div[@class='btn-box']/div[@class='cancel-button' and @role='button']"
        continue2_button_xpath = "/html/body/div/div[2]/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div"

        checkbox1_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div[1]/div/div[1]/img"
        checkbox2_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/img"
        confirm_button_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div"
        confirm_payment_xpath = "/html/body/div/div[2]/div[3]/div/div/div/div[3]/div[2]/div"


        time.sleep(1)
        self._wait_located(locater=cancel_button_xpath, _type="xpath")
        CancelButtonElement = self.driver.find_element(By.XPATH, cancel_button_xpath)
        self.driver.execute_script("arguments[0].click();", CancelButtonElement)

        time.sleep(1)
        self._wait_located(locater=continue2_button_xpath, _type="xpath")
        Continue2ButtonElement = self.driver.find_element(By.XPATH, continue2_button_xpath)
        self.driver.execute_script("arguments[0].click();", Continue2ButtonElement)

        # Click checkbox
        time.sleep(1)
        self._wait_located(locater=checkbox1_xpath, _type="xpath")
        Checkbox1Element = self.driver.find_element(By.XPATH, checkbox1_xpath)
        Checkbox1Element.click()
        
        # Click checkbox
        self._wait_located(locater=checkbox2_xpath, _type="xpath")
        Checkbox2Element = self.driver.find_element(By.XPATH, checkbox2_xpath)
        Checkbox2Element.click()

        # Continue button
        time.sleep(1)
        self._wait_located(locater=confirm_button_xpath, _type="xpath")
        ConfirmButtonElement = self.driver.find_element(By.XPATH, confirm_button_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmButtonElement)

        # Confirm payment
        time.sleep(1)
        self._wait_located(locater=confirm_payment_xpath, _type="xpath")
        ConfirmPaymentButtonElement = self.driver.find_element(By.XPATH, confirm_payment_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmPaymentButtonElement)
        print("Confirmed")

    def pps_payment(self, pps_card_num:str, pps_card_pwd:str):
        """ Select payment method and payment processing 
        
        Returns:
            bool: True if payment completed successfully, False otherwise
        """
        # Override UA to desktop for payment page only
        try:
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "platform": "Windows"
                },
            )
        except Exception:
            print("UA override skipped")
            
        # mastercard_payment_xpath = "/html/body/div/div[2]/div[2]/div/div/div/div[2]/div[7]/div[2]/img"
        pps_payment_xpath = "/html/body/div/div[2]/div[2]/div/div/div/div[2]/div[19]/div[2]/img"
        confirm_payment_xpath = "/html/body/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div"

        payment_button_xpath = "/html/body/div[3]/form[1]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table/tbody/tr[10]/td[2]/a[1]/img"

        # PPS payment
        time.sleep(1)
        self._wait_located(locater=pps_payment_xpath, _type="xpath")
        PPSPaymentButtonElement = self.driver.find_element(By.XPATH, pps_payment_xpath)
        PPSPaymentButtonElement.click()
        print("Select PPS")

        time.sleep(1)
        self._wait_located(locater=confirm_payment_xpath, _type="xpath")
        ConfirmPaymentButtonElement = self.driver.find_element(By.XPATH, confirm_payment_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmPaymentButtonElement)

        # Switch to the new payment tab
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(1)

        print("input pps info")

        card_number_xpath = "/html/body/div[3]/form[1]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/input"
        self._wait_located(locater=card_number_xpath, _type="xpath")
        self.driver.find_element(By.XPATH, card_number_xpath).send_keys(pps_card_num)
        print("Input card number")  

        card_pwd_xpath = "/html/body/div[3]/form[1]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td[2]/input"
        self._wait_located(locater=card_pwd_xpath, _type="xpath")
        self.driver.find_element(By.XPATH, card_pwd_xpath).send_keys(pps_card_pwd)
        print("Input card pwd")  

        check_box_xpath = "/html/body/div[3]/form[1]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table/tbody/tr[6]/td/input"
        self._wait_located(locater=check_box_xpath, _type="xpath")
        CheckBoxElement = self.driver.find_element(By.XPATH, check_box_xpath)
        CheckBoxElement.click()
        print("Click check box")

        # Payment button
        time.sleep(1)
        self._wait_located(locater=payment_button_xpath, _type="xpath")
        PaymentButtonElement = self.driver.find_element(By.XPATH, payment_button_xpath)
        self.driver.execute_script("arguments[0].click();", PaymentButtonElement)

        print("Click Payment Button")
        return True

    def monitor_dialog(self):
        """Monitor if the error dialog or login dialog is present, and handle accordingly."""
        error_dialog_xpath = "//div[@role='dialog' and @id='dialog' and .//div[@class='button' and contains(text(), '關閉')]]"
        close_btn_xpath = ".//div[@class='button' and contains(text(), '關閉')]"
        login_dialog_xpath = "//div[@role='dialog' and @class='el-dialog' and .//*[contains(text(), '登入')]]"
        
        try:
            ErrorDialogElement = self.driver.find_element(By.XPATH, error_dialog_xpath)
            if ErrorDialogElement.is_displayed():
                CloseBtnElement = ErrorDialogElement.find_element(By.XPATH, close_btn_xpath)
                self.driver.execute_script("arguments[0].click();", CloseBtnElement)
                print("Closed error dialog")
                return True
        except Exception:
            pass

        # Then, check for the login dialog
        try:
            LoginDialogElement = self.driver.find_element(By.XPATH, login_dialog_xpath)
            if LoginDialogElement.is_displayed():
                return True
        except Exception:
            pass

        return False

    def run_with_login_monitor(self, func, *args, username=None, password=None, **kwargs):
        """Continuously monitor login dialog and retry the function until it succeeds. If the function raises an exception, it will be propagated to the outer layer."""
        while True:
            if self.monitor_dialog():
                self.login_in_process(username, password)
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception:
                time.sleep(1)
                continue

    def wait_until_queue_empty(self):

        label_xpath = "//p[contains(text(), '輪候隊伍前方人數')]"
        value_xpath = label_xpath + "/following-sibling::p[1]"
        exit_button_xpath = "/html/body/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div"

        try:
            LabelElement = self.driver.find_element(By.XPATH, label_xpath)
            ValueElement = LabelElement.find_element(By.XPATH, value_xpath)
            if LabelElement and ValueElement:
                self._wait_located(locater=exit_button_xpath, _type="xpath")
                ExitButtonElement = self.driver.find_element(By.XPATH, exit_button_xpath)
                self.driver.execute_script("arguments[0].click();", ExitButtonElement)
        except Exception as e:
            pass

    