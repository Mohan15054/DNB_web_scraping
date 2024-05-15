from bs4 import BeautifulSoup
import csv

# Read HTML file
with open('page_source.html', 'r',encoding='utf-8') as html_file:
    html_content = html_file.read()

# Parse HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table
table = soup.find('table')
print(table)
# Open CSV file for writing
with open('table_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Loop through rows
    for row in table.find_all('tr'):
        # Extract data from each cell in the row
        data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        # Write data to CSV file
        writer.writerow(data)

print("CSV file generated successfully.")
