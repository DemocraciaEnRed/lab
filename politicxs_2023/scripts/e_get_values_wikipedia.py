#########################################
## Consuta API wikipedia
#########################################

import pandas as pd
from data.initial import POLITICXS
from data.from_apis import WIKIPEDIA_PAGES
from tools.wikipedia import Wikipedia

df = pd.merge(POLITICXS, WIKIPEDIA_PAGES, on='person_id', how='inner')
df['WIKIPEDIA_PAGE_ID'] = df['WIKIPEDIA_PAGE_ID'].fillna(0).astype(int)

# Itero sobre las filas para para analizarlos por api
for index, row in df.iterrows():
    if not pd.isna(row['WIKIPEDIA_URL']) :
        wikipedia = Wikipedia(row)
        api_response = wikipedia.get_info()
        print(api_response)
        for key, value in api_response.items():
            df.at[index, f'WIKIPEDIA_{key}'] = value
        
df = df.drop([col for col in POLITICXS.columns if col != "person_id"], axis=1)
df.to_csv('data/wikipedia_values_politicxs_2023.csv', index=False)

