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
service = Service(r'C:\Users\dario\OneDrive\Escritorio\chromedriver-win64\chromedriver.exe')  # Asegúrate de que esta ruta sea correcta

# Inicializa el driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL de IMDb (ejemplo)
url = 'https://www.imdb.com/chart/top'

# Abrir la página web
driver.get(url)

# Esperar a que los elementos estén disponibles
wait = WebDriverWait(driver, 60)  # Aumenta el tiempo de espera a 60 segundos

try:
    # Usar XPaths basados en la estructura actual de la página
    titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="titleColumn"]/a')))
    print(f"Títulos encontrados: {len(titles)}")

    years = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="titleColumn"]/span[@class="secondaryInfo"]')))
    print(f"Años encontrados: {len(years)}")

    ratings = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="ratingColumn imdbRating"]/strong')))
    print(f"Calificaciones encontradas: {len(ratings)}")

    # Crear listas para almacenar los datos
    movie_titles = []
    movie_years = []
    movie_ratings = []

    # Iterar sobre los elementos y extraer los datos
    for title, year, rating in zip(titles, years, ratings):
        movie_titles.append(title.text)
        movie_years.append(year.text.strip('()'))
        movie_ratings.append(rating.text)

    # Crear un DataFrame
    data = {'Title': movie_titles, 'Year': movie_years, 'Rating': movie_ratings}
    df = pd.DataFrame(data)

    # Guardar los datos en un archivo CSV
    df.to_csv('imdb_top_movies.csv', index=False)

    print("Datos guardados en 'imdb_top_movies.csv'")

except TimeoutException as e:
    print("TimeoutException: No se pudieron encontrar los elementos en la página web.")
    print(e)

# Cerrar el driver
driver.quit()