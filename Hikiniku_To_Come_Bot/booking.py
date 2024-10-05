### Booking logic and process
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from datetime import date, timedelta

class Booking:

    def __init__(self, driver) -> None:

        self.driver = driver


    def _wait_located(self, wait_time=5, xpath=None) -> None:

        assert xpath != None, "XPath cannot be None"

        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

        except TimeoutException:
            raise TimeoutException(f"\nTimeout! Cannot find XPATH: {xpath}") from None


    def select_partysize(self, party_size:int) -> None:

        print("\nSearching party size element ......")

        xpath = f"//select[@id='adult-picker']/option[@value='{party_size}']"
        self._wait_located(xpath=xpath)

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
                self.driver.quit()
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
    ) -> None:
        
        if timeslot_xpath_template is None:
            timeslot_xpath_template = "//button[@data-cy='book-now-time-slot-box-###']"

        print("\nTry to book selected the timeslot ......")

        for time_slot in timeslot_list:
            TimeslotXpath = timeslot_xpath_template.replace("###", time_slot)

            try:
                print(f"Try {time_slot} now")
                ...

            except:
                ...