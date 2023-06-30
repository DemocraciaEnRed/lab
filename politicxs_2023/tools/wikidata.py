
import requests
from bs4 import BeautifulSoup

# Creo la clase para analizar cosas desde wikipedia
class Wikidata:
    """
        Wikidata via API y los elementos referenciados via scrapping
    """

    API_URL = 'https://www.wikidata.org/w/api.php'
    API_PARAMS = {
        'language': 'es',
        'format': 'json'
    }    


    PROPERTIES = {
        "P735": 'NOMBRE',
        "P734": 'APELLIDO',
        "P1449": 'APODO',
        "P19": 'LUGAR_NACIMIENTO',
        "P569": 'FECHA_NACIMIENTO',
        "P21": 'GENERO',
        "P2002": 'USER_TWITTER',
        "P2013": 'USER_FACEBOOK',
        "P2003": 'USER_INSTAGRAM',
        "P1971": 'NUMERO_HIJXS',
        "P69": 'EDUCADO_EN',
        'P18': 'IMAGEN',
        "P39": 'PUESTOS_ANTERIORES', # Hay que buscar la forma de captar mas de 1
        "P106": 'OCUPACIONES' # Hay que buscar la forma de captar mas de 1
    }

    def __init__(self, row):
        self.id = row['WIKIDATA_URL'].split("/")[-1]


    def get_referenced_info(self, referenced_id): 
        response = requests.get('https://www.wikidata.org/wiki/'+referenced_id)
        page = BeautifulSoup(response.text, 'html.parser')
        title = page.find(class_='wikibase-title-label').get_text().strip()
        return title

    def get_info(self): 
        print(f"Buscando en API de Wikidata: {self.id}")
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
        for k, v in self.PROPERTIES.items():
            if k in claims:
                data_type = claims[k][0]["mainsnak"]["datavalue"]['type']
                data_value = claims[k][0]["mainsnak"]["datavalue"]["value"]
                if data_type == "wikibase-entityid":
                    try:    
                        referenced_data = self.get_referenced_info(data_value['id'])
                        response.update({v: referenced_data})
                    except:
                        print(f"Error al obtener información referenciada {v}")
                elif data_type == "string":
                    response.update({v: data_value})
                elif data_type == "time":
                    response.update({v: data_value['time']})

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