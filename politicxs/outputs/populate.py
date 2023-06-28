import pandas as pd

from inputs.data import (
    df_input, 
    PUESTOS_AREAS
)


#########################################
## CANDIDATURAS
#########################################

# Agrego id del area por puesto en las candidaturas
CANDIDATURAS = pd.merge(df_input, PUESTOS_AREAS, left_on=['state', 'role_type'], right_on=['state', 'role_type'], how='left')
CANDIDATURAS['area'] = CANDIDATURAS['role_type_area_id'].fillna(0).astype(int)
# Agrego membership_type
CANDIDATURAS['membership_type'] = "campaign_politician"
# Elimino columnas innecesarias
CANDIDATURAS = CANDIDATURAS.drop([
    'role_type_area_id',
], axis=1)

CANDIDATURAS.to_csv('data/final.csv')