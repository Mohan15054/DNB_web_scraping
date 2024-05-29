from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import post_process
import os
import Fetch_Industries


# Max Page numbe:

page=10
result_file_name = 'main_data_result1.csv'


driver = webdriver.Chrome()

# Open a new tab
driver.execute_script("window.open('https://www.dnb.com/business-directory/company-information.manufacturing.in.html?page=3');")

time.sleep(20)
# Switch to the new tab
driver.switch_to.window(driver.window_handles[1])

# Fetch Insdustries:
try:
    driver.get(f"https://www.dnb.com/business-directory/company-information.manufacturing.in.html?page=1")
    time.sleep(15)
    page_source = driver.page_source
    # Save the page source to an HTML file
    File_name = "Fetch_Insdutries.html"
    with open(File_name, "w", encoding="utf-8") as file:
        file.write(page_source)
    Fetch_Industries(File_name)
    os.remove(File_name)
except Exception as e:
    print(e)

# Fetch Indian Industries:

for i in range(1,page):
    print(i)
    # driver.switch_to.window(driver.window_handles[2])
    try:
        driver.get(f"https://www.dnb.com/business-directory/company-information.manufacturing.in.html?page={i}")
        time.sleep(15)
        page_source = driver.page_source

        # Save the page source to an HTML file
        with open(f"page_source_tes{i}.html", "w", encoding="utf-8") as file:
            file.write(page_source)

        # post_process.process_html(result_file_name,f'page_source_tes{i}.html')   # For Temp
        print(f"Page - {i} feched ")
        # os.remove(f'page_source_tes{i}.html')   # For Temp
    except Exception as e:
        print(e)

print(f"Finished processing {page} completed")
time.sleep(30)

# Close the browser
driver.quit()
