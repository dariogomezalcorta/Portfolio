import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_imdb_top_movies():
    url = 'https://www.imdb.com/chart/top/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    movies = []
    
    # Encuentra todos los elementos que contienen la información de las películas
    rows = soup.select('tbody.lister-list tr')
    
    for row in rows:
        title_column = row.find('td', class_='titleColumn')
        if title_column:
            title = title_column.a.text
            year = title_column.span.text.strip('()')
            rating_column = row.find('td', class_='imdbRating')
            rating = rating_column.strong.text if rating_column else 'N/A'
            movie_url = 'https://www.imdb.com' + title_column.a['href']
            
            # Obtener el género de cada película
            movie_response = requests.get(movie_url)
            movie_soup = BeautifulSoup(movie_response.content, 'html.parser')
            genre_tag = movie_soup.find('span', class_='sc-16ede01-2 iPpjzv')
            genre = genre_tag.text if genre_tag else 'N/A'
            
            movies.append({'title': title, 'year': year, 'rating': rating, 'genre': genre})

    return pd.DataFrame(movies)

df = scrape_imdb_top_movies()
df.to_csv('imdb_top_movies.csv', index=False)
print(df.head())