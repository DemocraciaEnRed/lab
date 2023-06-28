import pandas as pd
from data.initial import POLITICXS



#########################################
## Buscamos paginas en api de wikidata
#########################################

# from tools.wikidata import Wikidata

# df = POLITICXS[['person_id', 'full_name']].copy()
# # Itero sobre las filas para para consultar a la api en cada unx
# for index, row in df.iterrows():
#     wikidata_page = Wikidata.search(row['full_name'])
#     print(wikidata_page)
#     df.at[index, 'URL_WIKIDATA'] = wikidata_page

# df = df.drop(['full_name'], axis=1)
# df.to_csv('data/wikidata_links_politicxs_2023.csv')




#########################################
## Buscamos paginas en api de wikipedia
#########################################

# from tools.wikipedia import Wikipedia

# df = POLITICXS[['person_id', 'full_name']].copy()
# # Itero sobre las filas para para consultar a la api en cada unx
# for index, row in df.iterrows():
#     wikipedia_page = Wikipedia.search(row['full_name'])
#     print(wikipedia_page)
#     df.at[index, 'URL_WIKIPEDIA'] = wikipedia_page


# df = df.drop(['full_name'], axis=1)
# df.to_csv('data/wikipedia_links_politicxs_2023.csv')





#########################################
## Ejemplo Selenium navegamos por selenium wikidata para ver si es data correcta
#########################################

# import pandas as pd
# from data.from_apis import WIKIDATA_PAGES

# from tools.wikidata import Wikidata
# from selenium import webdriver

# df = WIKIDATA_PAGES.copy()
# driver = webdriver.Firefox()
# # Itero sobre las filas para para analizarlos scrappeando
# for index, row in df.iterrows():
#     # if row['URL_WIKIDATA']:
#     if not pd.isna(row['URL_WIKIDATA']) :
#         print(row['URL_WIKIDATA'])
#         driver.get(row['URL_WIKIDATA'])
#         driver.implicitly_wait(10)

# driver.quit()




#########################################
## Consuta API wikidata
#########################################

from tools.wikidata import Wikidata
from data.from_apis import WIKIDATA_PAGES

df = pd.merge(POLITICXS, WIKIDATA_PAGES, on='person_id', how='inner')

# Itero sobre las filas para para analizarlos por api
for index, row in df.iterrows():
    if not pd.isna(row['URL_WIKIDATA']) :
        wikidata = Wikidata(row)
        api_response = wikidata.get_info()
        print(api_response)


# df.to_csv('data/wikidata_vars_politicxs_2023.csv')






# #########################################
# ## Poblamos la data final
# #########################################

# from outputs.populate import populate_final_data

# populate_final_data()
