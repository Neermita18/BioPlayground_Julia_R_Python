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


def fetch_genbank_data(accession_id):
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(f'https://www.ncbi.nlm.nih.gov/nuccore/{accession_id}')
    time.sleep(10)  # Allow the page to load fully

    # Find all span elements with the class "feature"
    span_elements = driver.find_elements(By.CLASS_NAME, "feature")

    # Extract and process text from each span element
    for span in span_elements:
        text_content = span.text

        # Define patterns to extract specific fields
        patterns = {
            'mRNA': re.compile(r'mRNA\s+join\(([\d.,]+)\)\s+(.+)', re.DOTALL),
            'source': re.compile(r'source\s+(\d+\.\.\d+)\s+(.+)', re.DOTALL),
            'gene': re.compile(r'gene\s+(\d+\.\.\d+)\s+(/gene="[^"]+"\s+/gene_synonym="[^"]+")'),
         
            'CDS': re.compile(r'CDS\s+join\(([\d.,]+)\)\s+(.+)', re.DOTALL)
        }

        # Dictionary to store the extracted information
        extracted_info = {}

        # Extract the relevant information using the defined patterns
        for key, pattern in patterns.items():
            match = pattern.search(text_content)
            if match:
                if key == 'source':
                    extracted_info[key] = {
                        'range': match.group(1),
                        'details': match.group(2).replace('/', '').strip()
                    }
                elif key == 'gene':
                    extracted_info[key] = {
                        'range': match.group(1),
                        'details': match.group(2).replace('/', '').strip()
                    }
                elif key == 'mRNA':
                    extracted_info[key] = {
                        'range': match.group(1),
                        'details': match.group(2).replace('/', '').strip()
                    }
                elif key == 'CDS':
                    extracted_info[key] = {
                        'range': match.group(1),
                        'details': match.group(2).replace('/', '').strip()
                    }

        # Print the extracted information
        if extracted_info:  # Only print if there is any extracted info
            print("Extracted Information:")
            for key, value in extracted_info.items():
                if key == 'mRNA':
                    print(f"{key.upper()}: {value['range']}")
                    # Extracting product from mRNA details
                    product_match = re.search(r'product="([^"]+)"', value['details'])
                    if product_match:
                        print("Product:", product_match.group(1))
                else:
                    print(f"{key.upper()}: {value['range']}")
                    print(value['details'])
            print("-" * 40)

    # Extract gene information from the 'pre' tag
    gene_info = driver.find_element(By.TAG_NAME, 'pre')
    gene_text = gene_info.text

    # Define patterns for gene information
    gene_patterns = {
        'locus': re.compile(r'LOCUS\s+(.+)'),
        'definition': re.compile(r'DEFINITION\s+(.+)'),
        'accession': re.compile(r'ACCESSION\s+(.+)'),
        'version': re.compile(r'VERSION\s+(.+)'),
        'source': re.compile(r'SOURCE\s+(.+)'),
        'organism': re.compile(r'organism="([^"]+)"')
    }

    # Extract and print gene information
    for key, pattern in gene_patterns.items():
        match = pattern.search(gene_text)
        if match:
            print(f"{key.upper()}: {match.group(1).strip()}")
    print("-" * 40)

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
    return b.text

accession_id = "AY329622.1"
genbank_data = fetch_genbank_data(accession_id)
print("Source and definition:", genbank_data)

