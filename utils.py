import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to get driver
def get_driver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    options = uc.ChromeOptions()
    prefs = {
    "profile.default_content_setting_values.geolocation": 1  # Change to 2 to block
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument(f"--user-agent={user_agent}")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    return driver

# Function to close driver
def close_driver(driver):
    driver.quit()

# Function to wait
def wait_for_element(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

def wait_for_elements(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(locator))

def wait_for_visibility(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

def wait_for_clickability(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))