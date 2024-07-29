from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException

# Configura las opciones de Chrome
chrome_options = Options()
# Descomentar esta línea si quieres ver el navegador
# chrome_options.add_argument("--headless")

# Ruta al archivo chromedriver.exe
service = Service('D:\\chromedriver-win64\\chromedriver.exe')  # Asegúrate de que esta ruta sea correcta

# Inicializa el driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL de IMDb (ejemplo)
url = 'https://www.imdb.com/chart/top'

# Abrir la página web
driver.get(url)

# Esperar a que los elementos estén disponibles
wait = WebDriverWait(driver, 60)  # Aumenta el tiempo de espera a 60 segundos

try:
    # Usar XPaths basados en la imagen
    titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="lister-item-content"]/h3[@class="lister-item-header"]/a')))
    print(f"Títulos encontrados: {len(titles)}")

    years = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="lister-item-content"]/h3[@class="lister-item-header"]/span[@class="lister-item-year"]')))
    print(f"Años encontrados: {len(years)}")

    durations = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="lister-item-content"]/p[@class="text-muted"]/span[@class="runtime"]')))
    print(f"Duraciones encontradas: {len(durations)}")

    # Crear listas para almacenar los datos
    movie_titles = []
    movie_years = []
    movie_durations = []

    # Iterar sobre los elementos y extraer los datos
    for title, year, duration in zip(titles, years, durations):
        movie_titles.append(title.text)
        movie_years.append(year.text)
        movie_durations.append(duration.text)

    # Crear un DataFrame
    data = {'Title': movie_titles, 'Year': movie_years, 'Duration': movie_durations}
    df = pd.DataFrame(data)

    # Guardar los datos en un archivo CSV
    df.to_csv('imdb_top_movies.csv', index=False)

    print("Datos guardados en 'imdb_top_movies.csv'")

except TimeoutException as e:
    print("TimeoutException: No se pudieron encontrar los elementos en la página web.")
    print(e)

# Cerrar el driver
driver.quit()