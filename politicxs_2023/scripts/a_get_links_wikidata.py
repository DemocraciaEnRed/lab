#########################################
## Buscamos paginas en api de wikidata
#########################################

from data.initial import POLITICXS
from tools.wikidata import Wikidata

df = POLITICXS.copy()
# Itero sobre las filas para para consultar a la api en cada unx
for index, row in df.iterrows():
    wikidata_page = Wikidata.search(row['full_name'])
    print(wikidata_page)
    df.at[index, 'WIKIDATA_URL'] = wikidata_page

df = df.drop([col for col in POLITICXS.columns if col != "person_id"], axis=1)
df.to_csv('data/wikidata_links_politicxs_2023.csv', index=False)