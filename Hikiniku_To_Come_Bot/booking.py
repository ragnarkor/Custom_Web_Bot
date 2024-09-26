### Booking logic and process
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class Booking:

    def __init__(self, driver) -> None:

        self.driver = driver

    def _wait_located(self, wait_time=5, xpath=None):

        assert xpath != None, "XPath cannot be None"

        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

        except TimeoutException:
            raise TimeoutException(f"\nTimeout! Cannot find XPATH: {xpath}") from None


    def select_partysize(self, party_size):

        print("\nSearching party size element ......")

        xpath = f"//select[@id='adult-pickers']/option[@value='{party_size}']"
        self._wait_located(xpath=xpath)

        PartySizeSelection = self.driver.find_element(By.XPATH, xpath)
        PartySizeSelection.click()

        print("Party size selected ......")