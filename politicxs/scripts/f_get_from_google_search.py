#########################################
## Busqueda de datos principales en google con selenium
#########################################

from data.initial import POLITICXS

from tools.google import Google
from selenium import webdriver

df = POLITICXS.copy()

driver = webdriver.Firefox()
# Itero sobre las filas para para analizarlos scrappeando
for index, row in POLITICXS.iterrows():
    # if row['WIKIDATA_URL']:
    google_search = Google(row, driver)
    collect = google_search.get_info()
    print(collect)
    for key, value in collect.items():
        df.at[index, f'GOOGLE_{key}'] = value
    

driver.quit()
df = df.drop([col for col in POLITICXS.columns if col != "person_id"], axis=1)
df.to_csv('data/google_values_politicxs_2023.csv', index=False)
