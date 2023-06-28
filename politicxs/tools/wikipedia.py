import wikipedia

import requests
from bs4 import BeautifulSoup

wikipedia.set_lang("es")

# Creo la clase para analizar cosas desde wikipedia
class Wikipedia:
    """
        Con BeautifulSoup dado que es una web que carga la data completa
        BeautifulSoup obtiene el código completo de html
    """

    ocupacion = ""
    educacion = ""
    educado_en = ""
    nacimiento = ""
    residencia = ""
    religion = ""
    hijos = ""
    partido = ""
    

    def __init__(self, url):
        self.puestos = []
        if url:
            print(f"Scrappeanding {url}")
            response = requests.get(url)
            self.page = response.text
            self.process_biography()

    def process_biography(self):
        soup = BeautifulSoup(self.page, 'html.parser')
        # Infobox de biografia
        infobox = soup.find(class_='infobox')
        # Correspondiente a la biografía
        bio_section = infobox.find('tbody')
        # Buscar las filas de la tabla de la sección de la biografía
        rows = bio_section.find_all('tr')        
        
        # Recorrer cada fila y extraer los puestos
        for row in rows:

            # Si el texto contiene una etiqueta de encabezado, es un puesto
            if row.find('th', style="text-align:center;background-color:#E6E6FA;;") or row.find('th', style="text-align:center;background-color:#8DB1C3;color:#FFF;"):
                texto = row.find('th').get_text().strip()
                if texto:
                    self.puestos.append(texto)
            else: 
                # Obtener el texto de la fila
                if 'Educado en' in row.get_text():
                    self.educado_en = row.find('td').get_text().strip()
                if 'Educación' in row.get_text():
                    self.educacion = row.find('td').get_text().strip()
                if 'Ocupación' in row.get_text():
                    self.ocupacion = row.find('td').get_text().strip()    
                if 'Nacimiento' in row.get_text():
                    self.nacimiento = row.find('td').get_text().strip()      
                if 'Residencia' in row.get_text():
                    self.residencia = row.find('td').get_text().strip()      
                if 'Religión' in row.get_text():
                    self.religion = row.find('td').get_text().strip()      
                if 'Hijos' in row.get_text():
                    self.hijos = row.find('td').get_text().strip()               
                if 'Partido político' in row.get_text():
                    self.partido = row.find('td').get_text().strip()



    @staticmethod
    def search(full_name):
        
        print(f"Buscando en API de Wikipedia: {full_name}")

        results = wikipedia.search(full_name)

        if not results:
            return ''
        
        page_id = results[0]['pageid']
        try:
            return wikipedia.page(pageid=page_id).url
        except:
            return ''