import pandas as pd


#########################################
## AREAS Y PUESTOS
#########################################

PUESTOS_AREAS = pd.read_csv("inputs/puestos_areas_2023.csv")



#########################################
## DATA INICIAL
#########################################

df_input = pd.read_csv("inputs/elecciones_2023.csv")



#########################################
## POLITICXS
#########################################

POLITICXS = df_input[[
    'person_id', 'dni',
    'first_name', 'last_name', 'full_name',
    'nickname', 'date_birth', 'place_of_birth', 'gender', 'dead_or_alive',
    'has_descendants', 'previous_pubic_roles','last_degree_of_studies',
    'profession_1', 'profession_2', 'profession_3', 'profession_4',
    'profession_5', 'profession_6', 'Website', 'URL_FB_page',
    'URL_FB_profile', 'URL_IG', 'URL_TW', 'URL_others', 'URL_photo',
    ]]\
    .drop_duplicates(subset=['full_name'])\
    .copy()




#########################################
## PARTIDOS
#########################################

PARTIDOS = df_input['partido'].drop_duplicates().copy()



