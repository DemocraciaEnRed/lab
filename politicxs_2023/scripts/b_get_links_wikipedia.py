
#########################################
## Buscamos paginas en api de wikipedia
#########################################

from data.initial import POLITICXS
from tools.wikipedia import Wikipedia

df = POLITICXS.copy()
# Itero sobre las filas para para consultar a la api en cada unx
for index, row in df.iterrows():
    wikipedia_page = Wikipedia.search(row['full_name'])
    print(wikipedia_page)
    if len(wikipedia_page.keys()) != 0:
        df.at[index, 'WIKIPEDIA_URL'] = wikipedia_page['url']
        df.at[index, 'WIKIPEDIA_PAGE_ID'] = wikipedia_page['page_id']


df = df.drop([col for col in POLITICXS.columns if col != "person_id"], axis=1)
df.to_csv('data/wikipedia_links_politicxs_2023.csv', index=False)
