#########################################
## Poblamos la data final
#########################################

import pandas as pd

from data.initial import (
    df_input, 
    PUESTOS_AREAS
)

from data.from_apis import *


# Agrego id del area por puesto en las candidaturas
CANDIDATURAS = pd.merge(df_input, PUESTOS_AREAS, left_on=['state', 'role_type'], right_on=['state', 'role_type'], how='left')
CANDIDATURAS['area'] = CANDIDATURAS['role_type_area_id'].fillna(0).astype(int)
# Agrego membership_type
CANDIDATURAS['membership_type'] = "campaign_politician"
# Agrego data de wikipedia
CANDIDATURAS = pd.merge(CANDIDATURAS, WIKIPEDIA_VALUES, on='person_id', how='inner')
# Agrego data de wikidata
CANDIDATURAS = pd.merge(CANDIDATURAS, WIKIDATA_VALUES, on='person_id', how='inner')
# Agrego data de google
CANDIDATURAS = pd.merge(CANDIDATURAS, GOOGLE_VALUES, on='person_id', how='inner')

# CANDIDATURAS['date_birth'].fillna(CANDIDATURAS['WIKIDATA_FECHA_NACIMIENTO'], inplace=True)
# CANDIDATURAS['place_of_birth'].fillna(CANDIDATURAS['WIKIDATA_LUGAR_NACIMIENTO'], inplace=True)
# CANDIDATURAS['gender'].fillna(CANDIDATURAS['WIKIDATA_GENERO'], inplace=True)

# Elimino columnas innecesarias
# CANDIDATURAS = CANDIDATURAS[df_input.columns]

CANDIDATURAS.to_csv('outputs/elecciones_2023.csv', index=False)