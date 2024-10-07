### Booking logic and process
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains

import time
from datetime import date, timedelta

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
        self._wait_located(xpath=xpath, _type="xpath")

        PartySizeSelection = self.driver.find_element(By.XPATH, xpath)
        PartySizeSelection.click()

        print("Party size selected ......")


    def select_date(
            self,
            date_id:str = None,
            calendar_id:str = None,
            date_xpath:str = None
    ) -> None:
        
        if date_id is None:
            date_id = "date-picker"

        if calendar_id is None:
            calendar_id = "calendar-picker"

        if date_xpath is None:
            DateAfter7Days = date.today() + timedelta(days=7)

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
                # self.driver.quit()
            else:
                CalendarDatePicker = self.driver.find_element(By.XPATH, date_xpath)
                self.driver.execute_script("arguments[0].click()", CalendarDatePicker)
                print("Date selected ......")

        except:
            print(Exception)


    def select_time_slot(
        self,
        timeslot_list:list,
        timeslot_xpath_template:str = None,
        booking_button_xpath:str = None,
    ) -> None:
        
        if timeslot_xpath_template is None:
            timeslot_xpath_template = "//button[@data-cy='book-now-time-slot-box-###']"

        if booking_button_xpath is None:
            booking_button_xpath = "//div[@class='sc-gsnTZi gFJNgI']"

        print("\nTry to book selected the timeslot ......")

        for time_slot in timeslot_list:
            TimeslotXpath = timeslot_xpath_template.replace("###", time_slot)

            try:
                print(f"Try {time_slot} now")

                ### Click Timeslot
                self._wait_located(TimeslotXpath, _type="xpath")
                TimeslotSelection = self.driver.find_element(By.XPATH, TimeslotXpath)
                self.driver.execute_script("arguments[0].click();", TimeslotSelection)

                print(f"Selected time slot ({time_slot}) ......")

                ### Click book button
                self._wait_located(booking_button_xpath, _type="xpath")
                BookingButton = self.driver.find_element(By.XPATH, booking_button_xpath)
                self.driver.execute_script("arguments[0].click();", BookingButton)

                print("Clicked booking button ......")

            except:
                print(Exception)


    def payment(self,
                modal_class_name:str = None,
                modal_xpath:str = None,
                confirm_button_xpath:str = None):
        
        if confirm_button_xpath is None:
            confirm_button_xpath = "/html/body/div[4]/div/div/div/div[3]/button/span"

        print("\nClick agreement ......")

        ### Click argreement
        self._wait_located("ReactModal__Content", _type="class")

        ### Handle modal
        modal_element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[2]")

        print("\nScroll Down ......")

        scroll_origin = ScrollOrigin.from_element(modal_element)
        ActionChains(self.driver)\
            .scroll_from_origin(scroll_origin, 0, 2000)\
            .perform()
        
        time.sleep(1)

        self._wait_located(confirm_button_xpath, _type="xpath")
        ConfirmButton = self.driver.find_element(By.XPATH, confirm_button_xpath)
        self.driver.execute_script("arguments[0].click();", ConfirmButton)

        ### Input payment info
        ...