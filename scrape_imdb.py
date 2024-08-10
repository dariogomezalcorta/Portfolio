'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configurar el servicio del driver
service = Service(ChromeDriverManager().install())

# Inicializar el driver de Chrome
driver = webdriver.Chrome(service=service)

# Navegar a la página de IMDb
driver.get('https://www.imdb.com/chart/top/')

# Obtener los elementos de las películas
peliculas = driver.find_elements(By.XPATH, '//li[@class = "ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent"]')

# Iterar sobre cada película y extraer el título y la metadata
for pelicula in peliculas:
    try:
        titulo = pelicula.find_element(By.XPATH, './/h3[@class = "ipc-title__text"]').text
        print(f"Título: {titulo}")
    except:
        print("No se pudo encontrar el título.")
    
    try:
        metadata_elements = pelicula.find_elements(By.XPATH, './/span[contains(@class, "cli-title-metadata-item")]')
        metadata = [element.text for element in metadata_elements]
        print(f"Metadata: {', '.join(metadata)}")
    except:
        print("No se pudo encontrar la metadata.")
    
    print("--------------------------------------------------")

# Cerrar el navegador
driver.quit()
'''

import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Especifica la ruta al ejecutable de ChromeDriver
service = Service(r'C:/Users/dario/OneDrive/Escritorio/chromedriver-win64/chromedriver.exe')

# Inicializa el driver de Chrome
driver = webdriver.Chrome(service=service)

driver.get('https://www.imdb.com/chart/top/')

peliculas = driver.find_elements(By.XPATH, '//li[@class="ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent"]')

# Abre un archivo CSV para escribir
with open('peliculas_imdb.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Titulo', 'Año', 'Duracion', 'Clasificación'])

    for pelicula in peliculas:
        # Extrae el título de la película
        titulo = pelicula.find_element(By.XPATH, './/h3[@class="ipc-title__text"]').text
        
        # Extrae los elementos de metadata (año, duración, clasificación)
        metadata_elements = pelicula.find_elements(By.XPATH, './/span[contains(@class, "cli-title-metadata-item")]')
        
        # Extrae el texto de cada parte de la metadata
        metadata_texts = [element.text for element in metadata_elements]
        
        # Asegúrate de que metadata_texts tenga al menos 3 elementos
        año = metadata_texts[0] if len(metadata_texts) > 0 else ''
        duracion = metadata_texts[1] if len(metadata_texts) > 1 else ''
        clasificacion = metadata_texts[2] if len(metadata_texts) > 2 else 'Not Rated'
        
        # Escribe los datos en el archivo CSV
        writer.writerow([titulo, año, duracion, clasificacion])

# Cierra el navegador
driver.quit()