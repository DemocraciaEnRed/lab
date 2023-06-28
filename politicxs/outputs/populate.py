import pandas as pd

from data.initial import (
    df_input, 
    PUESTOS_AREAS
)

from data.from_apis import (
    WIKIPEDIA_PAGES,
    WIKIDATA_PAGES
)


#########################################
## CANDIDATURAS
#########################################
def populate_final_data():
        

    # Agrego id del area por puesto en las candidaturas
    CANDIDATURAS = pd.merge(df_input, PUESTOS_AREAS, left_on=['state', 'role_type'], right_on=['state', 'role_type'], how='left')
    CANDIDATURAS['area'] = CANDIDATURAS['role_type_area_id'].fillna(0).astype(int)
    # Agrego membership_type
    CANDIDATURAS['membership_type'] = "campaign_politician"
    # Agrego páginas de wikipedia
    CANDIDATURAS = pd.merge(CANDIDATURAS, WIKIPEDIA_PAGES, on='person_id', how='inner')
    # Agrego páginas de wikidata
    CANDIDATURAS = pd.merge(CANDIDATURAS, WIKIDATA_PAGES, on='person_id', how='inner')



    # Elimino columnas innecesarias
    CANDIDATURAS = CANDIDATURAS.drop([
        'role_type_area_id',
    ], axis=1)

    CANDIDATURAS.to_csv('outputs/elecciones_2023.csv')