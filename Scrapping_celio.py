import requests
import pandas as pd
from bs4 import BeautifulSoup

# Variables init
hrefs_list = []
records = []
# Source website
r = requests.get('https://store.celio.com/')
soup = BeautifulSoup(r.text, 'html.parser')
# Compared url to retrieve french shops
store_url = "https://store.celio.com/fr/"

# Get all links in celio shop general page
for link in soup.find_all('a'):
# If link match the french url add it to the list
    if store_url in link.get('href'):
        hrefs_list.append(link.get('href'))

# Function to get the data we want, we use try except in case data are missing like phone number for example
def celio_scrap(i):
    try:
        shop_name = results[i].find('h3').contents[3].contents[0]
    except:
        shop_name = "NA"
    try:
        whole_address = results[i].find('p', attrs={'class': 'adress-content'})
    except:
        whole_address = "NA"
    try:            
        address_line1 = whole_address.find_all('span')[0].contents[0].strip()
    except:
        address_line1 = "NA"        
    try:            
        postal = whole_address.find_all('span')[1].contents[0]
    except:
        postal = "NA"
    try:            
        city = whole_address.find_all('span')[2].contents[0]
    except:
        city = "NA"
    try: 
        phone = results[i].find('p', attrs={'class': 'telephone'}).contents[0][6:]
    except:
        phone = "NA"
    try:
        # If the shop is closed <span class:"closed"> can be found so we start searching for this one
        if results[i].find('span', attrs={'class': 'closed'}) is None:
            # If the span can't be found, shop is open so we retrieve the content we want
            hour = results[i].find('p', attrs={'class': 'horaires'}).contents[0][23:]
        else:
            # If it's found we manually set the value to closed
            hour = "Fermé"
    except:
        hour = "NA"
    # Append all the data to a list
    records.append((shop_name, address_line1, postal, city, phone, hour))

try:
# Looping through the urls list to get the data of each shop using the function
    for urls in hrefs_list:
        r = requests.get(urls)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('div', attrs={'class': 'Information'})
# Verifying the size of the result list because some city have several shops
        if len(results) > 1:
# If there are several shop, we loop to get all of them
            # Optionnal announce when several shops are found
            # print("Il y a plusieurs magasins sur le lien : {}".format(urls))
            i = 0
            for result in results:
                celio_scrap(i)
                i += 1
        else:
            celio_scrap(0)
except Exception as e:
    print(urls)
    print('Error: '+ str(e))
    
print('Traitement terminé avec un total de {} magasins trouvés'.format(len(records)))

# Add everything we got in a dataframe
dataframe_celio = pd.DataFrame(records, columns=['Nom Magasin', 'Adresse', 'Code Postal', 'Ville', 'Téléphone', 'Horaires'])
dataframe_celio.to_csv('TD_celio.csv', index = False, encoding = 'utf-8')
dataframe_celio