import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


# Creo un dataframe
df = pd.DataFrame({
    'key': [
        'massa',
        'wado',
        'scioli',
        'grabois',
        'bullrich',
        'larreta',
        'manes',
    ],
    'name': [
        "Sergio Massa",
        "Eduardo de Pedro",
        'Daniel Scioli',
        'Juan Grabois',
        'Patricia Bullrich ',
        'Horacio Rodríguez Larreta',
        'Facundo Manes',
    ],
    'wikipedia_page': [
        "https://es.wikipedia.org/wiki/Sergio_Massa",
        "https://es.wikipedia.org/wiki/Eduardo_de_Pedro",
        "https://es.wikipedia.org/wiki/Daniel_Scioli",
        "https://es.wikipedia.org/wiki/Juan_Grabois",
        "https://es.wikipedia.org/wiki/Patricia_Bullrich",
        "https://es.wikipedia.org/wiki/Horacio_Rodr%C3%ADguez_Larreta",
        "https://es.wikipedia.org/wiki/Facundo_Manes",
    ],
    'twitter_page': [
        "https://twitter.com/SergioMassa",
        "https://twitter.com/wadodecorrido",
        "https://twitter.com/danielscioli",
        "https://twitter.com/JuanGrabois",
        "https://twitter.com/PatoBullrich",
        "https://twitter.com/horaciorlarreta",
        "https://twitter.com/ManesF",
    ],
    'puestos': [None]*7,
    'ocupacion': [None]*7,
    'educado_en': [None]*7,
    'educacion': [None]*7,
    'nacimiento': [None]*7,
    'residencia': [None]*7,
    'religion': [None]*7,
    'hijos': [None]*7,
    'partido': [None]*7,
    'seguidores': [None]*7,
})


# Creo la clase para analizar cosas desde wikipedia
class AnalyzerWikipedia:
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

# Creo la clase para analizar cosas desde twitter
class AnalyzerTwitter:
    """
        Con selenium dado que es una web que carga la data dinamicamente
            Selenium navega y captura elementos
    """    

    seguidores = ""

    def __init__(self, url):
        
        if url:
            print(f"Scrappeanding {url}")
            self.driver = webdriver.Firefox()
            # Abrir la página de Twitter
            self.driver.get(url)

            # Esperar a que la página cargue completamente
            self.driver.implicitly_wait(10)

            self.process_account()
            self.driver.quit()


    def process_account(self):
        self.seguidores = self.driver.find_element(By.XPATH, '//a[contains(@href, "/followers")]').text


# Creo el analizador de politicos que le agrega los analyzers anteriores
class AnalyzerPolitician:

    def __init__(self, politician: dict):
        print(f"Analizando {politician['name']}")
        self.nombre = politician['name']
        self.wikipedia = AnalyzerWikipedia(politician['wikipedia_page'])
        self.twitter = AnalyzerTwitter(politician['twitter_page'])
        

# Itero sobre las filas para para analizarlos scrappeando
for index, row in df.iterrows():
    politico = AnalyzerPolitician(row)
    # Wikipedia
    row['ocupacion'] = politico.wikipedia.ocupacion
    row['educado_en'] = politico.wikipedia.educado_en
    row['nacimiento'] = politico.wikipedia.nacimiento
    row['residencia'] = politico.wikipedia.residencia
    row['religion'] = politico.wikipedia.religion
    row['hijos'] = politico.wikipedia.hijos
    row['educacion'] = politico.wikipedia.educacion
    row['partido'] = politico.wikipedia.partido
    row['puestos'] = ', '.join(politico.wikipedia.puestos)
    
    # Twitter
    row['seguidores'] = politico.twitter.seguidores
    
print("Exportando a excel")
df.to_csv('final_data.csv')
