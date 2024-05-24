import requests

from bs4 import BeautifulSoup, Tag

def fetch_genbank_data(accession_id):
    
    
    
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
    

    features = soup.find('div', class_="seqrprt seqviewer")
    # print((features))
    for f in features:
        a= soup.find('div', class_= "rprtheader")
        # print(a)
        b= a.find('h1')
        # print(b.text)
    return b.text

    # for feature in features:
    #     # print(type(feature))
    #     feature_name = feature.find('div', class_="seqrprt seqviewer")
    #     # print(feature_name)
        
    # #    y= soup.find('div', class_="seq gbff")
    # #     print(y) 
    
    #     c=soup.find('div', class_="sequence")
    #     print(c)
            
           
    #     # if feature_name in data:
        #     sequence = feature.find('pre', class_='sequence').text
        #     data[feature_name].append(sequence)
    
    # return data

# Example usage:
accession_id = "NC_000007.14"  # Replace with actual accession ID
genbank_data = fetch_genbank_data(accession_id)
print("Source and definition: ", genbank_data)

# print("mRNA Sequences:")
# for mrna in genbank_data['mRNA']:
#     print(mrna)

# print("\nGene Sequences:")
# for gene in genbank_data['gene']:
#     print(gene)

# print("\nCDS Sequences:")
# for cds in genbank_data['CDS']:
#     print(cds)