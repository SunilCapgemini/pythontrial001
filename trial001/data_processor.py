import os
import re
import nltk
from bs4 import BeautifulSoup

# Read the urls from urls.txt
with open('urls.txt') as f:
    urls = f.readlines()

# Download each url
for url in urls:
    url = url.strip()
    filename = url.split('/')[-1] + '.txt'


    file = os.path.join('ipldata', filename)
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))

    processed_data_folder = 'processed_data'
    if not os.path.exists(processed_data_folder):
        os.makedirs(processed_data_folder)

    if not os.path.exists(file):
        os.system(f'curl {url} -o {file}')
    
    with open(file, encoding='utf-8', errors='replace') as f:
        data = f.read()

    soup = BeautifulSoup(data, 'html.parser')

    def cleap_up(text):
        # clean up
        cleaned_text = re.sub(r'IPL MEDIA ADVISORY', 'IPL MEDIA ADVISORY \n', text)
        cleaned_text = re.sub(r'Code of Conduct', 'Code of Conduct \n', text)
        cleaned_text = re.sub(r'(\n\s*){2,}', '\n', text)
        return cleaned_text

    # Find the div with the specific class
    target_div = soup.find('div', class_='vn-blogDetCnt col-100 floatLft')

    # Clean the text
    from datetime import datetime

    cleaned_text = cleap_up(target_div.get_text())

    # Get current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Save the cleaned text to a file with the current date in the filename
    with open(f'{processed_data_folder}/cleaned_text_{current_date}_{filename}', 'w', encoding='utf-8', errors='replace') as freak:
        freak.write(cleaned_text)

