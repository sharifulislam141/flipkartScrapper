from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random

driver = webdriver.Chrome()

base_url = 'https://www.flipkart.com/search?q=t+shirts&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page='
page_number = 1
max_page = 25

titles = []
product_links = []
discount_prices = []
main_prices = []
image_links = []

while page_number <= max_page:
    url = base_url + str(page_number)
    time.sleep(random.randint(1,3))
    driver.get(url)
    print(f"Processing Page {page_number}")

    product_groups = driver.find_elements(By.CLASS_NAME, 'cPHDOP.col-12-12')

    for product_group in product_groups:
        products = product_group.find_elements(By.XPATH, '//a[contains(@class,"WKTcLC")]')
        for product in products:
            title = product.get_attribute('title')
            if title:
                titles.append(title)
            else:
                titles.append("No data")
            
            product_link_href = product.get_attribute('href')
            product_link = 'https://www.flipkart.com' + product_link_href
            if product_link:
                product_links.append(product_link)
            else:
                product_links.append("No data")

        discount_price_elements = product_group.find_elements(By.CLASS_NAME, 'Nx9bqj')
        for discount_price_element in discount_price_elements:
            discount_price = discount_price_element.text
            if discount_price:
                discount_prices.append(discount_price)
            else:
                discount_prices.append("No data")

        main_price_elements = product_group.find_elements(By.CLASS_NAME, 'yRaY8j')
        for main_price_element in main_price_elements:
            main_price = main_price_element.text
            if main_price:
                main_prices.append(main_price)
            else:
                main_prices.append("No data")

        image_link_elements = product_group.find_elements(By.CLASS_NAME, '_53J4C-')
        for image_link_element in image_link_elements:
            image_link = image_link_element.get_attribute('src')
            if image_link:
                image_links.append(image_link)
            else:
                image_links.append("No data")
    
    page_number += 1

driver.quit()

# Ensure all lists are the same length
max_length = max(len(titles), len(product_links), len(discount_prices), len(main_prices), len(image_links))
titles.extend(["No data"] * (max_length - len(titles)))
product_links.extend(["No data"] * (max_length - len(product_links)))
discount_prices.extend(["No data"] * (max_length - len(discount_prices)))
main_prices.extend(["No data"] * (max_length - len(main_prices)))
image_links.extend(["No data"] * (max_length - len(image_links)))

data = {
    'Title': titles,
    'Product Link': product_links,
    'Discount Price': discount_prices,
    'Main Price': main_prices,
    'Image Link': image_links
}

df = pd.DataFrame(data)
df.to_csv('flipkart.csv', index=False,encoding='utf-8-sig')
print("Scraping Complete")
