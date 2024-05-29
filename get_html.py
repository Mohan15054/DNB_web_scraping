from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

# Open a new tab
driver.execute_script("window.open('https://www.dnb.com/business-directory/company-information.manufacturing.in.html?page=3');")

time.sleep(20)

def get_html_page(File_name,Url):
    try:
        driver.get(Url)
        time.sleep(10)
        page_source = driver.page_source
        with open(File_name, "w", encoding="utf-8") as file:
            file.write(page_source)
    except Exception as e:
        print(e)
