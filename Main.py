import os
import Fetch_Industries
import pandas as pd
import get_top_Industries
from selenium import webdriver
import time
from datetime import datetime
import math

driver = webdriver.Chrome()

country = "India"

Excel_file = "Global_Indus_data.xlsx"

# # Open a new tab
driver.execute_script("window.open('https://www.dnb.com/business-directory/company-information.manufacturing.in.html?page=3');")

time.sleep(20)
driver.switch_to.window(driver.window_handles[1])

def get_html_page(File_name, Url):
    try:
        driver.get(Url)
        time.sleep(10)
        page_source = driver.page_source
        with open(File_name, "w", encoding="utf-8") as file:
            file.write(page_source)
    except Exception as e:
        print(e)

def has_header(file_name):
    try:
        with open(file_name, 'r') as f:
            first_line = f.readline().strip()
            return first_line.split(',') == list(df.columns)
    except Exception as e:
        print(e)

file_name = f"Final_file_{datetime.now().strftime('%Y-%m-%d')}.csv"

def save_to_excel(df, excel_file, sheet_name):
    try:
        with pd.ExcelWriter(excel_file, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    except Exception as e:
        print(e)

# Get Industrial_list
try:
    File_name = "agriculture.html"
    get_html_page(File_name, f"https://www.dnb.com/business-directory/company-information.manufacturing.in.html?page=1")
    Industrial_list = Fetch_Industries.process_html(File_name)
    df = pd.DataFrame(Industrial_list)

    tab_name = 'Industrial_list'
    save_to_excel(df, Excel_file, tab_name)
except Exception as e:
    print(e)

# Process each industry and save to Excel
try:
    # Get Top Company per Industry
    count = 0
    gh = {}

    for i in Industrial_list:
        # print(i['Title'])
        # Get Top 10 Companies in corresponding Industry & India sectors h_ref link
        File_name = "Top_indus.html"
        print(f"https://www.dnb.com/{i['Industrial_ref']}")
        get_html_page(File_name, f"https://www.dnb.com/{i['Industrial_ref']}")
        Top_indus = get_top_Industries.get_top_Industries(File_name)
        df = pd.DataFrame(Top_indus[0])
        gh[i['Title']] = df
        # Save each DataFrame to a new sheet in the same Excel file
        save_to_excel(df, 'Top_indus.xlsx', i['Title'][:30])
        India_link = Top_indus[1][0]
        File_name = "Town_list.html"
        get_html_page(File_name, f"https://www.dnb.com/{India_link}")
        Town_list = Fetch_Industries.fetch_town_list(File_name, country=country, title=i['Title'])
        for Towns in Town_list:
            # print("State:", Towns)
            State_link = Towns['H_ref']
            # India_link = Top_indus[1][0]
            File_name = "District_list.html"
            get_html_page(File_name, f"https://www.dnb.com/{State_link}")
            District_list = Fetch_Industries.fetch_district_list(html_file=File_name, country=country, title=i['Title'], state=Towns['Town_name'])
            # print(District_list)
            for i in District_list:
                Number = int((i['number_countries']).replace(',',''))
                # print(number_countries)
                # import re
                # match = re.search(r'of\s([\d,]+)', Number)
                # if match:
                #     number_str = match.group(1)
                #     # Remove commas and convert to integer
                #     Number = int(number_str.replace(',', ''))
                    # print(number_int)
                    # return number_int
                # time.sleep(300)
                District_link =i['H_ref']
                # print(District_link)
                # File_name = "Number.html"
                # get_html_page(File_name, f"https://www.dnb.com/{District_link}")
                # Number = Fetch_Industries.fetch_number('Final_district.html')
                if type(Number) == int:
                    loop_num = math.ceil(Number/50)
                    # print(loop_num)
                # time.sleep(30)
                for page_num in range(1,loop_num+1):
                    print(page_num)
                # time.sleep(300)

                    get_html_page(File_name, f"https://www.dnb.com/{District_link}?page={page_num}")
                    Fetch_final_report = Fetch_Industries.process_html_final(html_file=File_name,country=i['country'],state=i['State'],title=i['Title'],District=i['Town_name'],h_ref=i['H_ref'])
                    # print(Fetch_final_report)
                    df = pd.DataFrame(Fetch_final_report)
                    file_exists = os.path.isfile(file_name)

                    # Check if the file has a header
                    if file_exists and has_header(file_name):
                        # If the file exists and has a header, append the DataFrame without writing the header
                        df.to_csv(file_name, mode='a', header=False, index=False)
                    else:
                        # If the file does not exist or does not have a header, write the DataFrame with the header
                        df.to_csv(file_name, mode='a', header=True, index=False)
                                    # save_to_excel(df, Excel_file, 'Main')
                                    # time.sleep(300)
                            # for Districts in District_list:
                            #     print("District:", Districts)

except Exception as e:
    print(e)

# Close the WebDriver
driver.quit()
