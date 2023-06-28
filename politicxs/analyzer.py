
# import pandas as pd

# from tools.searcher import Searcher
# from tools.wikipedia import Wikipedia
# from tools.twitter import Twitter


# class Analyzer:

#     def __init__(self, politician: pd.Series):
#         self.politician = politician
#         self.full_name = self.politician['full_name']
#         print(f"Analizando {self.full_name}")
#         self.search_result = Searcher(self.full_name, 'DuckDuckGo')


# df = df.head(5)
# # Itero sobre las filas para para analizarlos scrappeando
# for index, row in df.iterrows():

#     politico = Analyzer(row)
#     df.at[index, 'URL_TW'] = politico.search_result.twitter_account
#     df.at[index, 'URL_IG'] = politico.search_result.instagram_account
#     df.at[index, 'URL_FB'] = politico.search_result.facebook_account
#     df.at[index, 'URL_WIKI'] = politico.search_result.wikipedia_page
#     df['URL_WIKI'] =  df['URL_WIKI'].str.replace('en.wikipedia', 'es.wikipedia')

# df.to_csv('final_data3.csv')

