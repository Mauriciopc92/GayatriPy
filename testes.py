import requests
from bs4 import BeautifulSoup

# Send a request to the website and retrieve the HTML content
url = 'https://www.fundamentus.com.br/detalhes.php?papel=PETR4'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the specific HTML elements containing the information you want to scrape
table = soup.find('table', {'class': 'w728'})

# Extract information from the table
rows = table.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    if len(cells) == 2:  # Assuming each row has two cells: label and value
        label = cells[0].text.strip()
        value = cells[1].text.strip()
        print(f'{label}: {value}')
