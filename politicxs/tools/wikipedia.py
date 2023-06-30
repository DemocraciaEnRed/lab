import wikipedia

import requests
import mwparserfromhell
import json

wikipedia.set_lang("es")

class Wikipedia:

    """
        Wikipedia via API
    """

    API_URL = 'https://es.wikipedia.org/w/api.php'
    API_PARAMS = {
        'format': 'json',
        'action': 'query',
        'prop': 'revisions',
        'language': 'es',
        'rvprop': 'content',
        'rvsection': '0'
    }    


    PROPERTIES = {
        'profesión': 'PROFESION',
        'cargo': 'CARGO1',
        'cargo2': 'CARGO2',
        'cargo3': 'CARGO3',
        'cargo4': 'CARGO4',
        'cargo5': 'CARGO5',
        'fecha de nacimiento': 'FECHA_NACIMIENTO',
        'lugar de nacimiento': 'LUGAR_NACIMIENTO',
        'partido': 'PARTIDO',
        'afiliaciones': 'AFILIACIONES',
        'almamáter': 'ALMAMATER',
        'sitioweb': 'SITIO_WEB',
    }

    
    def __init__(self, row):
        self.id = str(row['WIKIPEDIA_PAGE_ID'])


    def get_info(self):


        print(f"Buscando en API de Wikipedia: {self.id}")
        response = {}
        params = self.API_PARAMS
        params.update({
            "pageids": self.id,
        })        
        data = requests.get(self.API_URL, params=params).json()
        if not data: return response

        # Obtener la información del infobox 
        pages = data['query']['pages']
        revision = pages[self.id]['revisions'][0]['*']
        
        
        # Parsear el contenido del infobox utilizando mwparserfromhell
        wikicode = mwparserfromhell.parse(revision)

        # Convertir el contenido del infobox a un objeto JSON
        infobox_dict = {}
        for template in wikicode.filter_templates():
            template_dict = {}
            for param in template.params:
                param_name = param.name.strip()
                param_value = param.value.strip_code().strip()
                template_dict[param_name] = param_value
            infobox_dict[template.name.strip()] = template_dict

        ficha = [k for k in infobox_dict.keys() if 'ficha de' in k.lower()]
        if ficha:

            data = infobox_dict[ficha[0]]
            for k, v in self.PROPERTIES.items():
                if k in data:
                    response.update({v: data[k].split('|')[0]})

        return response


    @staticmethod
    def search(full_name):
        
        print(f"Buscando en API de Wikipedia: {full_name}")

        results = wikipedia.search(full_name)

        if not results:
            return {}
        
        page_id = results[0]['pageid']
        try:
            return {
                'page_id': page_id,
                'url': wikipedia.page(pageid=page_id).url
            }
        except:
            return {}