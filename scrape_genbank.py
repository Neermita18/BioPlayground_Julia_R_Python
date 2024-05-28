import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup, Tag
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

def fetch_genbank_data(accession_id):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(f'https://www.ncbi.nlm.nih.gov/nuccore/{accession_id}')
    time.sleep(5) 

    # Find all span elements with the class "feature"
    span_elements = driver.find_elements(By.CLASS_NAME, "feature")

    # Define patterns to extract specific fields
    patterns = {
        'mRNA': re.compile(r'mRNA\s+join\(([\d.,\s]+)\)\s+.+/product="([^"]+)"', re.DOTALL),
        'source': re.compile(r'source\s+(\d+\.\.\d+)\s+(.+)', re.DOTALL),
        'gene': re.compile(r'gene\s+(\d+\.\.\d+)\s+(/gene="[^"])'),
        'CDS': re.compile(r'CDS\s+join\(([\d.,]+)\)\s+(.+)', re.DOTALL)
    }

    # Dictionary to store the extracted information
    extracted_info = {
        'source': None,
        'gene': None,
        'mRNA': None,
        'CDS': None
    }

    # Extract and process text from each span element
    for span in span_elements:
        text_content = span.text
        for key, pattern in patterns.items():
            match = pattern.search(text_content)
            if match:
                if key == 'source':
                    extracted_info[key] = {
                        'range': match.group(1),
                        'details': match.group(2).replace('/', '').replace('\n', '').strip()
                    }
                elif key == 'gene':
                    extracted_info[key] = {
                        'range': match.group(1),
                    }
                elif key == 'mRNA':
                    extracted_info[key] = {
                        'range': match.group(1).replace('\n', '').replace(' ', ''),
                        'product': match.group(2)
                    }
                elif key == 'CDS':
                    extracted_info[key] = {
                        'range': match.group(1).replace('\n', ''),
                        'details': match.group(2).replace('/', '').replace('\n', '').strip()
                    }

    # Extract gene information from the 'pre' tag
    gene_info = driver.find_element(By.TAG_NAME, 'pre')
    gene_text = gene_info.text

    # Define patterns for gene information
    gene_patterns = {
        'locus': re.compile(r'LOCUS\s+(.+)'),
        'definition': re.compile(r'DEFINITION\s+(.+)'),
        'accession': re.compile(r'ACCESSION\s+(.+)'),
        'source': re.compile(r'SOURCE\s+(.+)'),
        'organism': re.compile(r'organism="([^"]+)"')
    }

    # Extract gene information
    gene_data = {}
    for key, pattern in gene_patterns.items():
        match = pattern.search(gene_text)
        if match:
            gene_data[key] = match.group(1).strip()

    driver.quit()
    
    # URL template for GenBank entry
    url = f'https://www.ncbi.nlm.nih.gov/nuccore/{accession_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title of the page
    features = soup.find('div', class_="content")
    for f in features:
        a = soup.find('div', class_="rprtheader")
        b = a.find('h1')

    return gene_data, extracted_info, b.text

if __name__ == "__main__":
    accession_id = "AF359939.1"
    gene_data, extracted_info, title = fetch_genbank_data(accession_id)
    print("Source and definition:", title)
    print(title)
    print(type(gene_data))
    print(extracted_info)


