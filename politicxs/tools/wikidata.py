
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


    def get_referenced_info(self, id): pass 

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
        
        print(claims["P1448"][0]["mainsnak"]["datavalue"]["value"])
        if "P735" in claims:
            response.update({'FIRST_NAME': claims["P735"][0]["mainsnak"]["datavalue"]["value"]})
        if "P734" in claims:
            response.update({'LAST_NAME': claims["P734"][0]["mainsnak"]["datavalue"]["value"]})                        
        if "P1449" in claims:
            response.update({'NICKNAME': claims["P1449"][0]["mainsnak"]["datavalue"]["value"]})          

        if "P19" in claims:
            response.update({'PLACE_OF_BIRTH': claims["P19"][0]["mainsnak"]["datavalue"]["value"]})            
        if "P569" in claims:
            response.update({'DATE_OF_BIRTH': claims["P569"][0]["mainsnak"]["datavalue"]["value"]})                        
        if "P21" in claims:
            response.update({'GENDER': claims["P21"][0]["mainsnak"]["datavalue"]["value"]})

        if "P2002" in claims:
            response.update({'USER_TWITTER': claims["P2002"][0]["mainsnak"]["datavalue"]["value"]})
        if "P2013" in claims:
            response.update({'USER_FACEBOOK': claims["P2013"][0]["mainsnak"]["datavalue"]["value"]})   
        if "P2003" in claims:
            response.update({'USER_INSTAGRAM': claims["P2003"][0]["mainsnak"]["datavalue"]["value"]})                        

        # Si la persona tiene hijos: P40 (child)
        # Cuántos hijos tiene: P1971 (number of children)
        # Estudios alcanzados: P69 (educated at)
        # Si tuvo cargos públicos previos: P39 (position held)
        # Listado de profesiones: P106 (occupation)
        # Foto: P18 (image)

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