from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configura las opciones de Chrome
chrome_options = Options()
# Descomentar esta línea si quieres ver el navegador
chrome_options.add_argument("--headless")

# Ruta al archivo chromedriver.exe
service = Service('C:\\Users\\dario\\OneDrive\\Escritorio\\chromedriver-win64\\chromedriver.exe')

# Inicializa el driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL de IMDb (ejemplo)
url = 'https://www.imdb.com/chart/top'

# Abrir la página web
driver.get(url)

# Esperar a que los elementos estén disponibles
wait = WebDriverWait(driver, 10)
titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="titleColumn"]')))
ratings = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="ratingColumn imdbRating"]')))

# Crear listas para almacenar los datos
movie_titles = []
movie_ratings = []

print(f"Titles found: {len(titles)}")
print(f"Ratings found: {len(ratings)}")

# Iterar sobre los elementos y extraer los datos
for title, rating in zip(titles, ratings):
    movie_titles.append(title.text)
    movie_ratings.append(rating.text)

# Crear un DataFrame
data = {'Title': movie_titles, 'Rating': movie_ratings}
df = pd.DataFrame(data)

# Guardar los datos en un archivo CSV
df.to_csv('imdb_top_movies.csv', index=False)

# Cerrar el driver
driver.quit()