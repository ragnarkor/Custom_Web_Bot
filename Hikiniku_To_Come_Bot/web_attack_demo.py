from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc


options = uc.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36')


driver = uc.Chrome()
driver.get("https://inline.app/booking/-NxpjjSJhxwTw6cV0Lm3:inline-live-3/-Nxpjjmuxwpudr9s2kHN?language=zh-hk")

PartySize = 1
PartySize_XPATH = f"//*[@id='adult-picker']/option[{PartySize+1}]"

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, PartySize_XPATH))
)

PartySizeSelection = driver.find_element(By.XPATH, PartySize_XPATH)
PartySizeSelection.click()


DiningDateSelection = driver.find_element(By.ID, "date-picker")
driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true');", DiningDateSelection)

# Remove the hidden attribute from the calendar picker
HiddenCalendar = driver.find_element(By.ID, "calendar-picker")
driver.execute_script("arguments[0].removeAttribute('hidden');", HiddenCalendar)


CalendarPicker = driver.find_element(By.XPATH, "//div[@data-cy='bt-cal-day' and @data-date='2024-09-18' and @class='sc-jSMfEi jMdVvF']")
# CalendarPicker = driver.find_element(By.XPATH, "//*[@id='calendar-picker']")
driver.execute_script("arguments[0].click();", CalendarPicker)


# Optional: Verify the changes
# print("New aria-expanded value:", DiningDateSelection.get_attribute('aria-expanded'))
# print("Is calendar picker hidden?", HiddenCalendar.get_attribute('hidden'))

TimeSlot_XPATH = "//button[@data-cy='book-now-time-slot-box-16-30']"

TimeSlotSelection = driver.find_element(By.XPATH, TimeSlot_XPATH)
driver.execute_script("arguments[0].click();", TimeSlotSelection)

BookingButton_XPATH = "//div[@class='sc-gsnTZi gFJNgI']"
BookingButton = driver.find_element(By.XPATH, BookingButton_XPATH)
driver.execute_script("arguments[0].click();", BookingButton_XPATH)


while input() == "q":
    driver.quit()
