#########################################
## Ejemplo Selenium navegamos por selenium wikidata para ver si es data correcta
#########################################

import pandas as pd
from data.from_apis import WIKIDATA_PAGES, WIKIPEDIA_PAGES

from tools.wikidata import Wikidata
from selenium import webdriver

df = WIKIPEDIA_PAGES.copy()
driver = webdriver.Firefox()
# Itero sobre las filas para para analizarlos scrappeando
for index, row in df.iterrows():
    # if row['WIKIDATA_URL']:
    if not pd.isna(row['WIKIPEDIA_URL']) :
        print(row['WIKIPEDIA_URL'])
        driver.get(row['WIKIPEDIA_URL'])
        driver.implicitly_wait(10)




df = WIKIDATA_PAGES.copy()
# Itero sobre las filas para para analizarlos scrappeando
for index, row in df.iterrows():
    # if row['WIKIDATA_URL']:
    if not pd.isna(row['WIKIDATA_URL']) :
        print(row['WIKIDATA_URL'])
        driver.get(row['WIKIDATA_URL'])
        driver.implicitly_wait(10)


driver.quit()