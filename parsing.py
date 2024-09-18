import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import os
import csv

# FUNCTIONS
def get_url()->None:
  "Loading URLS of each CAR and saving as file"
  print('___ LOAD URLS ___')

  sub_url = []
  for page in tqdm(range(1, int(input('How many pages do you want? '))+1)):
    url = f'https://www.mashina.kg/search/all/?page={page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    objects = soup.find("div", class_="search-results-table")
    lincs = objects.find_all('div', class_="list-item list-label")
    for ur in lincs:
      sub_url.append(ur.find('a')['href'])

  print(f'\n ___ Received {len(sub_url)} URLS ___')

  urls = []
  for i in sub_url:
    urls.append("https://www.mashina.kg" + i)

  pd.DataFrame(urls, columns=['URLS']).to_csv('urls.csv', index=False)
  print('\nFILE "urls.csv" SAVED')


def get_data(ur:str)->dict:
  
  response = requests.get(ur)
  soup = BeautifulSoup(response.text, "html.parser")
  objects = soup.find('div', class_='tab-pane fade in active')
  atr_dict = {}
  
  try:
    atributs = objects.find_all('div', class_ = 'field-row clr')
    for atr in atributs:
      key = atr.find('div', class_='field-label').text.strip().replace('\n', '')
      val = atr.find('div', class_='field-value').text.strip().replace('\n', '')
      atr_dict[key] = val
      
  except Exception:
    pass
    
  try:
    views = soup.find('span', class_ = 'listing-icons views').text
    atr_dict['views'] = views
  except Exception:
    pass

  try: 
    hearts = soup.find('span', class_ = 'listing-icons heart').text
    atr_dict['hearts'] = hearts
  except Exception:
    pass

  try: 
    tel_number = soup.find('div', class_ = 'number').text
    atr_dict['tel_number'] = tel_number
  except Exception:
    pass

  try:
    USD_price = soup.find('div', class_ = 'price-dollar').text.replace('$ ', '').replace(' ', '')
    KGS_price = soup.find('div', class_ = 'price-som').text.replace(' сом', '').replace(' ', '')
    brend = soup.find('div', class_ = 'head-left').find('h1').text
    publicated = soup.find('div', class_ = 'subblock upped-at').text.strip()
    atr_dict['USD_price'] = USD_price
    atr_dict['KGS_price'] = KGS_price
    atr_dict['brend'] = brend
    atr_dict['publicated'] = publicated
  except Exception:
    pass
  try:
    look_like_key = soup.find_all('div', class_ = 'name')
    look_like_val = soup.find_all('div', class_ = 'value')
    for i, j in zip(look_like_key, look_like_val):
      atr_dict[i.text] = j.text
  except Exception:
    look_like = None

  return atr_dict



#PROCESS
print('#########___START PARSING SCRIPT ___#########')
current_time = time.localtime()
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
print()
print(f"___ Current date and time ___  << {formatted_time} >>")
print('\n#######################################################\n')

print('###### Do you want to get the URLS? ######')
while True:
  answer = input('Write Y or N: ')
  if (answer == 'Y') or (answer == 'N'):
    break
  else:
    print(' !!! INVALID INPUT !!! Please re-enter !!!')


if answer=='Y':
  get_url()
elif answer=='N':
  if 'urls.csv' in os.listdir():
    pass
  else:
    print("!!! <urls.csv> file not found! Let's run the script for getting URLS!")
    get_url()



print('######  PARSING ######')
if "error_urls.csv" in os.listdir():
  answer = input('Do you want to PARS invalid URRLS? Y/N ')
  if answer.strip() == 'Y':
    urls = pd.read_csv('error_urls.csv').URLS.to_list()
  else:  
    urls = pd.read_csv('urls.csv').URLS.to_list()
else:
  urls = pd.read_csv('urls.csv').URLS.to_list()

cars = []
error_urls = []
for url in tqdm(urls):
  try:
    cars.append(get_data(url))
  except Exception:
    url_index = urls.index(url)
    print('!!!___ERRROR___!!!')
    print(f'With url index: {url_index}')
    print(f'With url: {url}')
    error_urls.append(url)
    
    


df = pd.DataFrame(cars)
print('___ DATA INFO ___\n')
print(df.info())
print(f'\n\nNumber of unique phone numbers: {df.tel_number.unique().shape[0]} / {df.shape[0]}\n')
df.to_csv(f'mashina_kg_{formatted_time}.csv', index=False)
print(f'___ File << mashina_kg_{formatted_time}.csv >> saved ___')

if len(error_urls) > 0:
  print('THERE ARE INVALID URLS')
  pd.DataFrame(error_urls, columns=['URLS']).to_csv('error_urls.csv', index=False)
  print('\nFILE "error_urls.csv" SAVED')


print('##### END #####')





