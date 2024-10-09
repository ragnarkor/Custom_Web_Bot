### Booking logic and process
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains

import sys
import time
from datetime import datetime, date, timedelta

class Booking:

    def __init__(self, driver) -> None:

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


    def select_partysize(self, party_size:int) -> None:

        print("\nSearching party size element ......")

        xpath = f"//select[@id='adult-picker']/option[@value='{party_size}']"
        self._wait_located(locater=xpath, _type="xpath")

        PartySizeSelection = self.driver.find_element(By.XPATH, xpath)
        PartySizeSelection.click()

        print("Party size selected ......")


    def select_date(self) -> None:
        
        date_id = "date-picker"
        calendar_id = "calendar-picker"
        DateAfter7Days = date.today() + timedelta(days=2)

        print(f"\nSelected Date: {DateAfter7Days}\n")
        
        date_xpath = f"//div[@data-cy='bt-cal-day' and @data-date='{DateAfter7Days.strftime('%Y-%m-%d')}']"

        try:
            ### Expand the calendar & Unhide
            DateSelectionBox = self.driver.find_element(By.ID, date_id)
            self.driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true');", DateSelectionBox)

            HiddenCalendar = self.driver.find_element(By.ID, calendar_id)
            self.driver.execute_script("arguments[0].removeAttribute('hidden');", HiddenCalendar)

            print("Expand & Display calendar ......")

            ### Select date from calendar
            is_disabled = self.driver.find_element(By.XPATH,date_xpath).get_attribute("disabled") # Check if that date is full
            
            if is_disabled:
                print("The date you selected is full !!!!!!!")
                sys.exit(1)
            else:
                CalendarDatePicker = self.driver.find_element(By.XPATH, date_xpath)
                self.driver.execute_script("arguments[0].click()", CalendarDatePicker)
                print("Date selected ......")

        except Exception as e:
            print(e)


    def select_time_slot(self, timeslot_list:list) -> None:
        
        timeslot_xpath_template = "//button[@data-cy='book-now-time-slot-box-###']"
        booking_button_xpath = "//div[@class='sc-gsnTZi gFJNgI']"

        print("\nTry to book selected the timeslot ......")

        for time_slot in timeslot_list:
            TimeslotXpath = timeslot_xpath_template.replace("###", time_slot)

            try:
                print(f"Try {time_slot} now")

                ### Click Timeslot
                self._wait_located(locater=TimeslotXpath, _type="xpath")
                TimeslotSelection = self.driver.find_element(By.XPATH, TimeslotXpath)
                self.driver.execute_script("arguments[0].click();", TimeslotSelection)

                print(f"Selected time slot ({time_slot}) ......")

                ### Click book button
                self._wait_located(locater=booking_button_xpath, _type="xpath")
                BookingButton = self.driver.find_element(By.XPATH, booking_button_xpath)
                self.driver.execute_script("arguments[0].click();", BookingButton)

                print("Clicked booking button ......")

                has_alert = self.driver.execute_script("return (typeof window.alert === 'function');")
                print("Alert detection using JavaScript: ", has_alert)
                if has_alert:
                    WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                    self.driver.switch_to.alert.accept()

            except Exception as e:
                print(e)


    def payment(self, booker_info_dict:dict = {}, gender:str = "M"):

        modal_name = "ReactModal__Content"
        #modal_xpath = "/html/body/div[4]/div/div/div"
        confirm_button_xpath = "/html/body/div[4]/div/div/div/div[3]/button/span"

        surname_field_xpath = "//input[@id='familyName' and @data-cy='familyName']"
        firstname_field_xpath = "//input[@id='givenName' and @data-cy='givenName']"

        gender = booker_info_dict["gender"]
        if gender == "M":
            gender_xpath = "//input[@id='gender-male']"
        elif gender == "F":
            gender_xpath = "//input[@id='gender-female']"
        else:
            gender_xpath = "//input[@id='gender-none']"

        phone_num_xpath = "//input[@id='phone' and @data-cy='phone']"
        email_xpath = "//input[@id='email' and @data-cy='email']"
        purpose_xpath = "/html/body/div[1]/div/div/form/section[1]/div[5]/div[1]/div[5]/span"

        credit_card_xpath = "/html/body/div/form/span[2]/div/div/div[2]/span/input"
        expired_date_xpath = "/html/body/div/form/span[2]/div/span/input"
        cvc_code_xpath = "/html/body/div/form/span[2]/div/span/input"
        owner_name_xpath = "/html/body/div[1]/div/div/form/section[2]/div[2]/div[4]/input"

        deposit_agreement_xpath = "/html/body/div[1]/div/div/form/div[2]/div[1]/label"
        confirm_booking_button_xpath = "/html/body/div[1]/div/div/form/div[2]/button[1]/div/span"

        print("\nClick agreement ......")

        ### Click argreement
        self._wait_located(locater="ReactModal__Content", _type="class")

        ### Handle modal
        modal_element = self.driver.find_element(By.CLASS_NAME, modal_name)

        print("\nScroll Down ......")

        scroll_origin = ScrollOrigin.from_element(modal_element)
        ActionChains(self.driver)\
            .scroll_from_origin(scroll_origin, 0, 2000)\
            .perform()
        
        time.sleep(1)

        self._wait_located(locater=confirm_button_xpath, _type="xpath")
        ConfirmButton = self.driver.find_element(By.XPATH, confirm_button_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmButton)

        ### Input payment info
        time.sleep(2)

        self.driver.find_element(By.XPATH, surname_field_xpath).send_keys(booker_info_dict["surname"])
        self.driver.find_element(By.XPATH, firstname_field_xpath).send_keys(booker_info_dict["first_name"])
        self.driver.find_element(By.XPATH, gender_xpath).click()

        self.driver.find_element(By.XPATH, phone_num_xpath).send_keys(booker_info_dict["phone"])
        self.driver.find_element(By.XPATH, email_xpath).send_keys(booker_info_dict["email"])
        self.driver.find_element(By.XPATH, purpose_xpath).click()

        self.driver.find_element(By.XPATH, credit_card_xpath).send_keys(booker_info_dict["credit_card_num"])
        self.driver.find_element(By.XPATH, expired_date_xpath).send_keys(booker_info_dict["expired_date"])
        self.driver.find_element(By.XPATH, cvc_code_xpath).send_keys(booker_info_dict["cvv"])

        owner_name = booker_info_dict["surname"] + " " + booker_info_dict["first_name"]
        self.driver.find_element(By.XPATH, owner_name_xpath).send_keys(owner_name)

        # self.driver.find_element(By.XPATH, deposit_agreement_xpath).click()
        # self.driver.find_element(By.XPATH, confirm_booking_button_xpath).click()