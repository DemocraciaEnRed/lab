
import requests

# Creo la clase para analizar cosas desde wikipedia
class Wikidata:
    """
        WIKIDATA VIA API
    """

    API_URL = 'https://www.wikidata.org/w/api.php'
    API_PARAMS = {
        'language': 'es',
        'format': 'json'
    }    

    def __init__(self, row):
        self.id = row['URL_WIKIDATA'].split("/")[-1]
        print(self.id)

    def get_info(self): 
        response = {}
        params = self.API_PARAMS
        params.update({
            "action": "wbgetentities",
            "ids": self.id,
            "props": "claims"
        })        
        data = requests.get(self.API_URL, params=params).json()
        if not data: return response
        
        claims = data["entities"][self.id]["claims"]
        if "P2002" in claims:
            response.update({'WIKIDATA_USER_TWITTER': claims["P2002"][0]["mainsnak"]["datavalue"]["value"]})
        if "P19" in claims:
            response.update({'WIKIDATA_PLACE_OF_BIRTH': claims["P19"][0]["mainsnak"]["datavalue"]["value"]})            

        return response


    @classmethod
    def search(cls, full_name):
        
    
        print(f"Buscando en API de Wikidata: {full_name}")
        params = cls.API_PARAMS
        params.update({
            'action': 'wbsearchentities',
            'search': full_name
        })
        data = requests.get(cls.API_URL, params=params)
        if not data.json()['search']:
            return ''
        
        results = []
        for d in data.json()['search']:
            if 'description' in d.keys():
                if 'arg' in d['description'].lower():
                    results.append(d['url'])
                    break
        if not results:
            return ''
        return 'https:'+results[0]