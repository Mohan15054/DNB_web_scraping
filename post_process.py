from bs4 import BeautifulSoup
import csv

def remove_empty_space(string):
        return ' '.join(string.split())


def write_csv(filename,data): 
    try:
        # filename='main_data_result.csv'
        with open(filename, 'a', newline='') as csvfile:
                fieldnames = list(data.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # If the file is empty, write the header
                if csvfile.tell() == 0:
                    writer.writeheader()
                # Write the data
                writer.writerow({key: remove_empty_space(value) for key, value in data.items()})
    except Exception as e:
         print("Error writing data  to file :",e)

def process_html(file_name,html_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the table
        divs = soup.find_all('div', class_='col-md-12 data')

        print(len(divs))
    except Exception as e:
         print(e)


    if divs:
        # print(divs[0])
        for div in divs:
            # print(div)
            column_names = {
                "Company": None,
                "Country": None,
                "Sales Revenue": None
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
            # print(column_names)
            write_csv(file_name,column_names)
