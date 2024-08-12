import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Especifica la ruta al ejecutable de ChromeDriver
service = Service(r'C:/Users/dario/OneDrive/Escritorio/chromedriver-win64/chromedriver.exe')

# Inicializa el driver de Chrome
driver = webdriver.Chrome(service=service)
driver.get('https://www.imdb.com/chart/top/')

# Espera a que la página cargue y todas las películas sean visibles
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '//li[@class="ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent"]'))
)

# Desplázate hacia abajo para cargar todas las películas
scroll_pause_time = 2  # Tiempo de espera entre cada scroll
screen_height = driver.execute_script("return window.innerHeight")

for i in range(10):  # Intenta hacer scroll 10 veces o hasta que se carguen todas las películas
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

# Obtén todas las películas después de haber hecho scroll
peliculas = driver.find_elements(By.XPATH, '//li[@class="ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent"]')

# Asegúrate de que todas las películas estén cargadas
assert len(peliculas) >= 250, "No se cargaron todas las películas, intenta incrementar el número de scrolls."

# Abre un archivo CSV para escribir
with open('peliculas_imdb.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Titulo', 'Año', 'Duracion', 'Clasificación', 'Puntaje', 'Resumen', 'Director', 'Actores', 'URL Imagen'])

    for pelicula in peliculas:
        try:
            # Extrae el título de la película
            titulo = pelicula.find_element(By.XPATH, './/h3[@class="ipc-title__text"]').text

            # Extrae los elementos de metadata (año, duración, clasificación)
            metadata_elements = pelicula.find_elements(By.XPATH, './/span[contains(@class, "cli-title-metadata-item")]')
            metadata_texts = [element.text for element in metadata_elements]

            año = metadata_texts[0] if len(metadata_texts) > 0 else ''
            duracion = metadata_texts[1] if len(metadata_texts) > 1 else ''
            clasificacion = metadata_texts[2] if len(metadata_texts) > 2 else 'Not Rated'

            # Extrae el puntaje
            puntaje = pelicula.find_element(By.XPATH, './/span[@class="ipc-rating-star--rating"]').text

            # Verifica si existe el botón de información
            info_buttons = pelicula.find_elements(By.XPATH, './/button[@class="ipc-icon-button cli-info-icon ipc-icon-button--base ipc-icon-button--onAccent2"]')
            if info_buttons:
                # Haz clic en el botón para mostrar más información
                info_button = info_buttons[0]
                driver.execute_script("arguments[0].click();", info_button)

                # Espera hasta que se cargue la ventana emergente
                ventana_emergente = WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "ipc-promptable-base__panel")]'))
                )

                # Introduce un retraso para asegurar que toda la información se cargue
                time.sleep(2)

                # Extrae el resumen de la película
                resumen = ventana_emergente.find_element(By.XPATH, './/div[contains(@class, "sc-d3701649-2 cTFzHt")]').text

                # Obtén el director dentro de la ventana emergente
                director_elements = ventana_emergente.find_elements(
                    By.XPATH, './/a[contains(@href, "/name/") and not(contains(@href, "?ref_=chttp_tt_pd"))]'
                )
                director = director_elements[0].text if director_elements else 'N/A'

                # Extrae los actores
                actores_elements = ventana_emergente.find_elements(By.XPATH, './/li[@class="ipc-inline-list__item"]')
                actores = ', '.join([actor.text for actor in actores_elements])

                # Extrae el URL de la imagen
                url_imagen = pelicula.find_element(By.XPATH, './/img[@class="ipc-image"]').get_attribute('src')

                # Escribe los datos en el archivo CSV
                writer.writerow([titulo, año, duracion, clasificacion, puntaje, resumen, director, actores, url_imagen])

                # Cierra la ventana emergente
                close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, './/button[@aria-label="Cerrar mensaje"]'))
                )
                driver.execute_script("arguments[0].click();", close_button)

                # Introduce un retraso adicional para asegurar que la ventana se cierre completamente
                time.sleep(1)

            else:
                # Si no hay botón de información, maneja el registro sin la ventana emergente
                writer.writerow([titulo, año, duracion, clasificacion, puntaje, '', '', '', ''])

        except Exception as e:
            print(f"Error al procesar la película: {titulo if 'titulo' in locals() else 'Desconocido'}. Detalle del error: {str(e)}")

# Cierra el navegador
driver.quit()