#########################################
## Consuta API wikidata
#########################################

import pandas as pd
from data.initial import POLITICXS
from data.from_apis import WIKIDATA_PAGES
from tools.wikidata import Wikidata

df = pd.merge(POLITICXS, WIKIDATA_PAGES, on='person_id', how='inner')

# Itero sobre las filas para para analizarlos por api
for index, row in df.iterrows():
    if not pd.isna(row['WIKIDATA_URL']) :
        wikidata = Wikidata(row)
        api_response = wikidata.get_info()
        print(api_response)
        for key, value in api_response.items():
            df.at[index, f'WIKIDATA_{key}'] = value        
        
df = df.drop([col for col in POLITICXS.columns if col != "person_id"], axis=1)
df.to_csv('data/wikidata_values_politicxs_2023.csv')
