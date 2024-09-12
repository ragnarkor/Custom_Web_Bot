from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# options = webdriver.EdgeOptions()
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# service = Service("edgedriver_linux64/msedgedriver")

# driver = webdriver.Edge(service=service,
#                         options=options)

service = Service("chromedriver-linux64/chromedriver")

driver = webdriver.Chrome(service=service,
                          options=options)

driver.get("https://orteil.dashnet.org/cookieclicker/")


WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "langSelect-EN"))
)

LanguageSelectionButton = driver.find_element(By.ID, "langSelect-EN")
LanguageSelectionButton.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "bigCookie"))
)

count = 0

while count <= 100:
    BigCookieButton = driver.find_element(By.ID, "bigCookie")
    BigCookieButton.click()
    count += 1

# driver.maximize_window()



### Undetection Chromedriver
import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36')

driver = uc.Chrome()
driver.get("https://inline.app/booking/-NxpjjSJhxwTw6cV0Lm3:inline-live-3/-Nxpjjmuxwpudr9s2kHN?language=zh-hk")
