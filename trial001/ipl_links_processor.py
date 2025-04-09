import requests
from bs4 import BeautifulSoup

url = "https://www.iplt20.com/news/Latest"
response = requests.get(url)
data = response.text

with open('iplnews.txt', 'w') as f:
    f.write(data)

soup = BeautifulSoup(data, 'html.parser')


# Find the div with the specific class
target_div = soup.find('div', id='div-match-report')

links = []
for link in target_div.find_all('a'):
    href = link.get('href')
    if href and href.startswith('https://www.iplt20.com/'):
        links.append(href)

with open('urls.txt', 'w') as f:
    for link in links:
        f.write(link + '\n')
