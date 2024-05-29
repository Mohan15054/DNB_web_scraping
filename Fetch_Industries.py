from bs4 import BeautifulSoup
import json
import os
import pandas as pd
def remove_empty_space(string):
        return ' '.join(string.split())

def process_html(html_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        data = []
        for link_content in soup.find_all('div', class_='link-content'):
            a_tag = link_content.find('a')
            href = a_tag['href']
            content = a_tag.get_text(strip=True)
            data.append({'Industrial_ref': href, 'Title': content})
        with open('output.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
        return data

    except Exception as e:
         print(e)

def fetch_town_list(html_file,country,title):
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        data_divs = soup.find_all('div', class_='col-md-6 col-xs-6 data')

        # Extract Town name, H_ref, and number-countries
        data_list = []

        for div in data_divs:
            a_tag = div.find('a')
            if a_tag:
                town_name = remove_empty_space(a_tag.get_text(strip=True).rsplit('(', 1)[0].strip())
                h_ref = remove_empty_space(a_tag['href'])
                number_countries = remove_empty_space(a_tag.find('span', class_='number-countries').get_text(strip=True).strip('()'))
                data_list.append({
                    'Town_name': town_name,
                    'H_ref': h_ref,
                    'number_countries': number_countries,
                    'Title': title,
                    'country': country
                })
        return data_list

    except Exception as e:
         print(e)


def fetch_district_list(html_file,country,title,state):
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        data_divs = soup.find_all('div', class_='col-md-6 col-xs-6 data')

        # Extract Town name, H_ref, and number-countries
        data_list = []

        for div in data_divs:
            a_tag = div.find('a')
            if a_tag:
                town_name = remove_empty_space(a_tag.get_text(strip=True).rsplit('(', 1)[0].strip())
                h_ref = remove_empty_space(a_tag['href'])
                number_countries = remove_empty_space(a_tag.find('span', class_='number-countries').get_text(strip=True).strip('()'))
                data_list.append({
                    'Town_name': town_name,
                    'H_ref': h_ref,
                    'number_countries': number_countries,
                    'Title': title,
                    'country': country,
                    'State':state
                })
        return data_list

    except Exception as e:
         print(e)

def fetch_number(html_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        results_summary_div = soup.find('div', class_='results-summary')

        # Extract the text from the div element
        text = results_summary_div.get_text()

        # Extract the number using regular expression
        import re
        match = re.search(r'of\s([\d,]+)', text)
        if match:
            number_str = match.group(1)
            # Remove commas and convert to integer
            number_int = int(number_str.replace(',', ''))
            # print(number_int)
            return number_int
    except Exception as e:
        print(e)
        return 0

def has_header(file_name,df):
    try:
        with open(file_name, 'r') as f:
            first_line = f.readline().strip()
            return first_line.split(',') == list(df.columns)
    except Exception as e:
        print(e)

def process_html_final(html_file,country,title,state,District,h_ref):
    try:
        file_name = 'Fault_Result.csv'
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find the table
        divs = soup.find_all('div', class_='col-md-12 data')
        print(len(divs))
        if len(divs) == 0:
            print("Hello, world!")
            file_exists = os.path.isfile(file_name)
            data_failed = {"FailedData": [h_ref], "Country": [country], "Title": [title], "State": [state], "District": [District]}
            df = pd.DataFrame(data_failed)
            # Check if the file has a header
            if file_exists and has_header(file_name,df):
                # If the file exists and has a header, append the DataFrame without writing the header
                df.to_csv(file_name, mode='a', header=False, index=False)
            else:
                # If the file does not exist or does not have a header, write the DataFrame with the header
                df.to_csv(file_name, mode='a', header=True, index=False)

        # except Exception as e:
        #      print(e)

        company_list = []
        if divs:
            # print(divs[0])
            for div in divs:
                # print(div)
                column_names = {
                    "Company": None,
                    "Country": None,
                    "Sales Revenue": None,
                    "title" : title,
                    "State":state,
                    "District":District
                }
                if div:
                    company = div.find('div', class_='col-md-6')
                    if company:
                        column_names["Company"] = remove_empty_space(company.text.strip())

                    country = div.find('div', class_='col-md-4')
                    if country:
                        column_names["Country"] = remove_empty_space(country.text.replace("Country:", ""))

                    sales_revenue = div.find('div', class_='col-md-2 last')
                    if sales_revenue:
                        column_names["Sales Revenue"] = remove_empty_space(sales_revenue.text.replace("Sales Revenue ($M):", ""))
                else:
                    print("No div found with the specified name.")
                # print("Column",column_names)
                # write_csv(file_name,column_names)

                company_list.append(column_names)
        return company_list
    except Exception as e:
        print(e)