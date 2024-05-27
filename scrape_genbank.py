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
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    print(driver)
    driver.get(f'https://www.ncbi.nlm.nih.gov/nuccore/{accession_id}')
    time.sleep(10)
        
    
    span_elements = driver.find_elements(By.CLASS_NAME, "feature")

# Extract and process text from each span element
    for span in span_elements:
        text_content = span.text

        # Define patterns to extract specific fields
        patterns = {
            'organism': re.compile(r'/organism="([^"]+)"'),
            'mol_type': re.compile(r'/mol_type="([^"]+)"'),
            'chromosome': re.compile(r'/chromosome="([^"]+)"'),
            'map': re.compile(r'/map="([^"]+)"'),
            'clone': re.compile(r'/clone="([^"]+)"')
        }

        # Dictionary to store the extracted information
        extracted_info = {}

        # Extract the relevant information using the defined patterns
        for key, pattern in patterns.items():
            match = pattern.search(text_content)
            if match:
                extracted_info[key] = match.group(1)

        # Print the extracted information
        if extracted_info:  # Only print if there is any extracted info
            print("Extracted Information:")
            for key, value in extracted_info.items():
                print(f"{key}: {value}")
            print("-" * 40)
        
            
     
        
    gene_info = driver.find_element(By.TAG_NAME, 'pre')

# Get the text from the element
    gene_text = gene_info.text
    locus_pattern = re.compile(r'LOCUS\s+(.+)')
    definition_pattern = re.compile(r'DEFINITION\s+(.+)')
    accession_pattern = re.compile(r'ACCESSION\s+(.+)')
    version_pattern = re.compile(r'VERSION\s+(.+)')
    source_pattern = re.compile(r'SOURCE\s+(.+)')
    organism_pattern = re.compile(r'/organism="([^"]+)"')

    locus_match = locus_pattern.search(gene_text)
    definition_match = definition_pattern.search(gene_text)
    accession_match = accession_pattern.search(gene_text)
    version_match = version_pattern.search(gene_text)

    source_match = source_pattern.search(gene_text)
    organism_match = organism_pattern.search(gene_text)

 
    if locus_match:
            print(f"LOCUS: {locus_match.group(1)}")
    if definition_match:
            print(f"DEFINITION: {definition_match.group(1)}")
    if accession_match:
            print(f"ACCESSION: {accession_match.group(1)}")
    if version_match:
            print(f"VERSION: {version_match.group(1)}")
    if source_match:
            print(f"SOURCE: {source_match.group(1)}")
    if organism_match:
            print(f"ORGANISM: {organism_match.group(1)}")
    print("-" * 40)


   
    

    driver.quit()
    
    
    # URL template for GenBank entry
    url = f'https://www.ncbi.nlm.nih.gov/nuccore/{accession_id}'
    
   
    response = requests.get(url)
    # print(response)
    # print(response.text)
    # print(response.content)
    
 
    soup = BeautifulSoup(response.content, 'html.parser')
   

    # Find the sections of interest (mRNA, gene, CDS)
    data = {
        'mRNA': [],
        'gene': [],
        'CDS': []
    }
    

    features = soup.find('div', class_="content")
    # print((features))
    for f in features:
        a= soup.find('div', class_= "rprtheader")
        # print(a)
        b= a.find('h1')
        # print(b.text)
    return b.text

   


accession_id = "AY329622.1" 
genbank_data = fetch_genbank_data(accession_id)
print("Source and definition: ", genbank_data)

