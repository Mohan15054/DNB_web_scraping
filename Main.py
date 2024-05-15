from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open a new tab
driver.execute_script("window.open('https://www.dnb.com/business-directory/company-information.manufacturing.in.html?page=3');")

time.sleep(30)
# Switch to the new tab
driver.switch_to.window(driver.window_handles[1])

# Navigate to a URL

for i in range(1,5):
    print(i)

    driver.get(f"https://www.dnb.com/business-directory/company-information.manufacturing.in.html?page={i}")

    page_source = driver.page_source

    # Save the page source to an HTML file
    with open(f"page_source_tes{i}.html", "w", encoding="utf-8") as file:
        file.write(page_source)

    # Wait for a few seconds (optional)
time.sleep(300)

# Close the browser
driver.quit()
