import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Selenium WebDriver
# Bypass SSL dependency by switching to undetected_chromedriver if needed
# Handle secure connections gracefully

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode to avoid UI pop-up
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print("An error occurred initializing the Chrome driver.", str(e))
        driver = None
    return driver

# Function to scrape product details
def scrape_amazon():
    url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
    driver = init_driver()
    if not driver:
        print("Driver initialization failed. Ensure SSL module is accessible or run in a suitable environment.")
        return

    driver.get(url)

    # Wait for page to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']")))
    except Exception as e:
        print("Error waiting for page elements:", str(e))
        driver.quit()
        return

    # Create CSV file for storing results
    with open("amazon_products.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Price", "Rating", "Seller Name"])

        products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
        for product in products:
            try:
                # Extract product name
                product_name = product.find_element(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']").text
            except:
                product_name = "N/A"

            try:
                # Extract product price
                price = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
            except:
                price = "N/A"

            try:
                # Extract product rating
                rating = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']").text
            except:
                rating = "N/A"

            try:
                # Extract seller name (only if available)
                seller_info = product.find_element(By.XPATH, ".//span[contains(text(), 'by')]//following-sibling::span").text
            except:
                seller_info = "N/A"

            # Write data row in CSV
            writer.writerow([product_name, price, rating, seller_info])

    driver.quit()
    print("Scraping completed. Data saved to 'amazon_products.csv'")

if __name__ == "__main__":
    scrape_amazon()
