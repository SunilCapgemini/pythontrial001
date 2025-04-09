import os
import re
import nltk
from bs4 import BeautifulSoup
file = 'ipldata/iplt20.txt'

if not os.path.exists(os.path.dirname(file)):
    os.makedirs(os.path.dirname(file))

if not os.path.exists(file):
    os.system(f'curl https://www.iplt20.com/news/4150/tata-ipl-2025-match-22-pbks-vs-csk-match-report -o {file}')

with open(file) as f:
    data = f.read()


soup = BeautifulSoup(data, 'html.parser')

# Function to remove multiple consecutive newlines
def remove_multiple_newlines(text):
    # Replace two or more consecutive newlines with a single newline
    cleaned_text = re.sub(r'(\n\s*){2,}', '\n', text)
    return cleaned_text.strip()


# Find the div with the specific class
target_div = soup.find('div', class_='vn-blogDetCnt col-100 floatLft')


# Clean the text
from datetime import datetime

cleaned_text = remove_multiple_newlines(target_div.get_text())

# Get current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Save the cleaned text to a file with the current date in the filename
with open(f'cleaned_text_{current_date}.txt', 'w') as file:
    file.write(cleaned_text)

