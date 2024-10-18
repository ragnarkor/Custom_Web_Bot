from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains
import time
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

        username_xpath = "/html/body/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div[1]/input"
        password_xpath = "/html/body/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div[2]/input"
        login_button_xpath = "/html/body/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div[3]/div"

        ### Switch driver to new page
        self.driver.switch_to.window(self.driver.window_handles[-1])

        if username and password:
            UsernameField = self.driver.find_element(By.XPATH, username_xpath)
            UsernameField.send_keys(username)

            PasswordField = self.driver.find_element(By.XPATH, password_xpath)
            PasswordField.send_keys(password)

            LoginButtonElement = self.driver.find_element(By.XPATH, login_button_xpath)
            self.driver.execute_script("arguments[0].click();", LoginButtonElement)

            print("Logged in")

    def search_available_period(self):

        facility_button_xpath = "/html/body/div/div[1]/div[1]/div/div[1]/div/div[1]/ul/li[2]/div"
        sport_input_field_xpath = "/html/body/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[1]/div/div[1]/span"
        input_field_xpath = "/html/body/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div[1]/div[2]/div[2]/div/div/div[1]/input"

        time.sleep(1)
        self._wait_located(locater=facility_button_xpath, _type="xpath")
        FacilityButtonElement = self.driver.find_element(By.XPATH, facility_button_xpath)
        self.driver.execute_script("arguments[0].click();", FacilityButtonElement)

        self._wait_located(locater=sport_input_field_xpath, _type="xpath")
        SportInputFieldElement = self.driver.find_element(By.XPATH, sport_input_field_xpath)
        SportInputFieldElement.click()

        self._wait_located(locater=input_field_xpath, _type="xpath")
        InputFieldElement = self.driver.find_element(By.XPATH, input_field_xpath)
        InputFieldElement.send_keys('乒乓球') ### Not test yet