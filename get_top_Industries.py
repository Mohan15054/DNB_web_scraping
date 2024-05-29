from bs4 import BeautifulSoup
import json


# html_file="agriculture.html"

def remove_empty_space(string):
        return ' '.join(string.split())


def get_top_Industries(Filename):
    
    companies = []
    with open(Filename, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    for company_div in soup.find_all('div', class_='col-md-4 item'):
        company_name = company_div.find('div', class_='company-name').text.strip()
        revenue = company_div.find('span', class_='revenue').text.strip()
        country = company_div.find('span', class_='country').text.strip()
        companies.append({'company_name': company_name, 'revenue': revenue, 'country': country})
    
    # for link_content in soup.find_all('div', class_='link-content'):
    #     a_tag = company_div.find('a')
    #     href = a_tag['href']
    #     content = a_tag.get_text(strip=True)
    for company_div in soup.find_all('div', class_='col-md-6 col-xs-6 data'):
        a_tag = company_div.find('a')
        if a_tag:
            h_ref = remove_empty_space(a_tag.get('href'))  # Get the href attribute
            country_name = remove_empty_space(a_tag.text.strip())  # Get the country name
            # number_countries = company_div.find('span', class_='number-countries').text.strip()  # Get the number of countries
            # print(f"Country: {country_name}, Href: {h_ref}, Number of Countries: {number_countries}")
            if "India" in country_name:
                India_href = [h_ref]


    # json_data = json.dumps(companies, indent=4)
    return [companies, India_href]

# get_top_Industries('aerospace.html')