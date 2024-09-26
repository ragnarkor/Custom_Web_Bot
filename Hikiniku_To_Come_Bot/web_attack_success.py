import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, date, timedelta
from selenium.webdriver.common.alert import Alert


from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException

import time

class Booking_Bot:

    def __init__(self, URL:str, PartySize:int, TimeSlot:list[str]) -> None:
        self.URL = URL

        self.PartySize = PartySize
        assert 0 < self.PartySize < 5, "Party Size exceed the range 1 - 4"

        self.TimeSlot = TimeSlot
        self._IsValidTimeSlot(self.TimeSlot)

        self.options = None

        print("\nBooking Bot start ......")

    def _IsValidTimeSlot(self, TimeSlot:str) -> bool:

        assert isinstance(TimeSlot, list), "Please input a list"

        time_format = "%H-%M"

        for time in TimeSlot:
            time_fstr = datetime.strptime(time, time_format)
            StartTime = datetime.strptime("11-00", time_format)
            EndTime = datetime.strptime("21-15", time_format)

            if not StartTime <= time_fstr <= EndTime:
                raise Exception(f"Time Slot: {time_fstr.strftime('%H-%M')} exceed the range 11:00 - 21:15")


    def setup_options(self, SettingOptions:list[str] = []) -> None:
        """Setting Chrome browser options

        Args:
            SettingOptions (list[str], optional): A list of arguments to setup Chrome browser. Defaults to [].
        """

        self.options = uc.ChromeOptions()

        if SettingOptions:
            for setting in SettingOptions:
                self.options.add_argument(setting)


    def Load_driver(self, KeepAlive:bool = False) -> None:
        """Build Chrome driver based on the setup_options() & Access the URL

        Args:
            KeepAlive (bool, optional): Determine if the browser keep or not after run the script. Defaults to False.
        """

        print("\nLoad Chrome driver ......")

        self.driver = uc.Chrome(options=self.options, enable_cdp_events=KeepAlive)
        self.driver.get(self.URL)


    def select_partysize(self, WaitTime:int = 5, XPATH:str = None) -> None:
        """Select the number of person

        Args:
            WaitTime (int, optional): The wait time to find the existence of the XPATH element. Defaults to 5.
            XPATH (str, optional): The XPATH of element. Defaults to None.
        """

        if XPATH is None:
            XPATH = f"//*[@id='adult-picker']/option[{self.PartySize+1}]"

        try:
            print("\nSearching party size element ......")

            WebDriverWait(self.driver, WaitTime).until(
                EC.presence_of_element_located((By.XPATH, XPATH))
            )

            PartySizeSelection = self.driver.find_element(By.XPATH, XPATH)
            PartySizeSelection.click()

            print("Party size selected ......")

        except TimeoutException:
            raise TimeoutException(f"\nTimeout! Cannot find XPATH: {XPATH}") from None


    def select_date(self, WaitTime:int = 5, DateID:str = None, CalendarID:str = None, DateXPATH:str = None) -> None:
        """Expand & Unhide calendar, Select date

        Args:
            WaitTime (int, optional): The wait time to find the existence of the XPATH element. Defaults to 5.
            DateID (str, optional): The date ID to search element. Defaults to None.
            CalendarID (str, optional): The Calendar ID to search element. Defaults to None.
            DateXPATH (str, optional): The date XPATH to search element. Defaults to None.
        """

        if DateID is None:
            DateID = "date-picker"

        if CalendarID is None:
            CalendarID = "calendar-picker"

        if DateXPATH is None:
            DateAfter7Days = date.today() + timedelta(days=7)
            print(DateAfter7Days)
            # DateAfter7Days = datetime(2024, 9, 23) + timedelta(days=7)
            DateXPATH = f"//div[@data-cy='bt-cal-day' and @data-date='{DateAfter7Days.strftime('%Y-%m-%d')}']"

        try:
            # print("\nSearching calendar element ......")

            ### Expand the calendar & Unhide
            DateSelectionBox = self.driver.find_element(By.ID, DateID)
            self.driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true');", DateSelectionBox)

            HiddenCalendar = self.driver.find_element(By.ID, CalendarID)
            self.driver.execute_script("arguments[0].removeAttribute('hidden');", HiddenCalendar)

            print("\nExpand & Display calendar ......")

            ### Select date from calendar
            CalendarDatePicker = self.driver.find_element(By.XPATH, DateXPATH)
            self.driver.execute_script("arguments[0].click()", CalendarDatePicker)

            print("Date selected ......")

        except NoSuchElementException:
            raise NoSuchElementException(f"Cannot find the date ID: `{DateID}` or calendar ID: `{CalendarID}` or date xpath: `{DateXPATH}`") from None


    def select_time_slot(self, WaitTime:int = 5, TimeSlotXPATH_template:str = None, BookingButtonXPATH:str = None):

        ### Set xpath config
        if TimeSlotXPATH_template is None:
            TimeSlotXPATH_template = "//button[@data-cy='book-now-time-slot-box-###']"
        else:
            assert "###" in TimeSlotXPATH_template, "Please replace the time slot as `###`"

        if BookingButtonXPATH is None:
            BookingButtonXPATH = "//div[@class='sc-gsnTZi gFJNgI']"

        print("\nTry preference time slot ......")

        ### Loop all time slot preference
        for time_slot in self.TimeSlot:
            TimeSlotXPATH = TimeSlotXPATH_template.replace("###", time_slot)

            try:
                ### Select time slot
                TimeSlotSelection = self.driver.find_element(By.XPATH, TimeSlotXPATH)
                self.driver.execute_script("arguments[0].click();", TimeSlotSelection)

                print(f"\nSelected time slot ({time_slot}) ......")
                
                WebDriverWait(self.driver, WaitTime).until(
                    EC.presence_of_element_located((By.XPATH, BookingButtonXPATH))
                )

                BookingButton = self.driver.find_element(By.XPATH, BookingButtonXPATH)
                self.driver.execute_script("arguments[0].click();", BookingButton)

                print("Clicked booking button ......")


                # alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())

                # # Accept the alert (click OK)
                # alert.accept()


                ### Scroll down pop up windows & click confirm
                # ConfirmTimeXPATH = "//button[@data-cy='confirm-house-rule' and @class='sc-hHLeRK fyDsji']"

                # WebDriverWait(self.driver, WaitTime).until(
                #     EC.visibility_of_element_located((By.XPATH, ConfirmTimeXPATH))
                # )
                # ConfirmTimeButton = self.driver.find_element(By.XPATH, ConfirmTimeXPATH)


                WebDriverWait(self.driver, WaitTime).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "ReactModal__Content"))
                )
 

                # Locate the modal element
                modal_element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[2]")

                scroll_origin = ScrollOrigin.from_element(modal_element)
                ActionChains(self.driver)\
                    .scroll_from_origin(scroll_origin, 0, 2000)\
                    .perform()
                
                time.sleep(1)

                WebDriverWait(self.driver, WaitTime).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button/span"))
                )
                ConfirmButton = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button/span")
                self.driver.execute_script("arguments[0].click();", ConfirmButton)


            # except NoSuchElementException:
            #     print(f"Time Slot: {time_slot} is full or Cannot not find time slot xpath: {TimeSlotXPATH}")

            # except UnexpectedAlertPresentException:
            #     ### Handle alert
            #     self.driver.switch_to.alert.accept()
            #     print("Accepted")

            # except TimeoutException:
            #     print(f"Cannot find the button xpath: {BookingButtonXPATH}")
            except:
                pass



if __name__ == "__main__":

    URL = "https://inline.app/booking/-NxpjjSJhxwTw6cV0Lm3:inline-live-3/-Nxpjjmuxwpudr9s2kHN"
    PartySize = 1
    TimeSlot = ["21-15"]
    # TimeSlot = ["17-00"]

    bot = Booking_Bot(URL=URL, PartySize=PartySize, TimeSlot=TimeSlot)

    SettingOptions = ["--disable-gpu",
                      "--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"]

    ### Define Browser Setting Options
    bot.setup_options(SettingOptions=SettingOptions)

    ### Load Chrome Driver & Access to the URL
    bot.Load_driver(KeepAlive=True)

    ### Select the number of person
    bot.select_partysize()

    ### Select the date
    bot.select_date()


    bot.select_time_slot()


