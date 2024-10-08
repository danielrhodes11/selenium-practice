from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time


def click_element_with_retry(driver, by, value, retries=3):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return element
        except StaleElementReferenceException:
            if attempt < retries - 1:
                time.sleep(1)  # wait before retrying
            else:
                raise


# Set up the WebDriver service
service = Service(
    executable_path='/Users/danielrhodes/Desktop/Selenium/chromedriver')
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://orteil.dashnet.org/cookieclicker/")

    # Wait for the language selection element to be clickable
    language = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='langSelect-EN']"))
    )
    language.click()

    # Wait for the cookie element to be clickable and get the cookie element
    cookie = click_element_with_retry(driver, By.ID, "bigCookie")
    cookies_id = "cookies"
    product_price_prefix = "productPrice"
    product_prefix = "product"

    while True:
        try:
            cookie = click_element_with_retry(driver, By.ID, "bigCookie")
            cookies_count_text = driver.find_element(
                By.ID, cookies_id).text.split(" ")[0]
            cookies_count = int(cookies_count_text.replace(",", ""))

            for i in range(4):
                product_price_text = driver.find_element(
                    By.ID, product_price_prefix + str(i)).text
                # Debugging line
                print(
                    f"Product price text for product {i}: '{product_price_text}'")

                # Check if product_price_text is empty
                if not product_price_text:
                    print(f"Product price for product {i} is empty.")
                    continue

                try:
                    product_price = int(product_price_text.replace(",", ""))
                except ValueError as e:
                    print(
                        f"Failed to convert product price '{product_price_text}' to int: {e}")
                    continue

                if cookies_count >= product_price:
                    product = driver.find_element(
                        By.ID, product_prefix + str(i))
                    product.click()

            print(f"Cookies: {cookies_count}")
            time.sleep(1)  # Adjust the sleep time if necessary
        except StaleElementReferenceException:
            # Handle stale element if the cookie element becomes stale again
            cookie = click_element_with_retry(driver, By.ID, "bigCookie")

finally:
    driver.quit()
