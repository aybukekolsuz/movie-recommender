import pandas as pd
import requests
import time

def load_movie_data(file_path):
    # Film verilerini yükle
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def preprocess_data(data):
    # Veriyi ön işleme tabi tut
    # Örneğin, eksik değerleri doldurma veya gereksiz sütunları kaldırma
    data = data.dropna()
    print(data.head())
    print(data.columns)
    return data

def get_movie_titles(data):
    # Film başlıklarını al
    return data['title'].tolist() if 'title' in data.columns else []

def fetch_imdb_data(title, api_key):
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        imdb_score = data.get("imdbRating", None)
        poster_url = data.get("Poster", None)
        return imdb_score, poster_url
    return None, None

def load_movielens_data(item_path, data_path, omdb_api_key):
    item_columns = ['movie_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL',
                    'unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy',
                    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                    'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    items = pd.read_csv(item_path, sep='|', encoding='latin-1', names=item_columns)
    genre_columns = item_columns[5:]
    items['genres'] = items[genre_columns].apply(lambda x: [genre for genre, val in x.items() if val == 1], axis=1)

    # Gerçek IMDb puanı ve poster url'si ekle
    imdb_scores = []
    poster_urls = []
    for title in items['title']:
        score, poster = fetch_imdb_data(title, omdb_api_key)
        imdb_scores.append(score)
        poster_urls.append(poster)
        time.sleep(0.2)  # API'yı yavaşlatmak için

    items['imdb_score'] = imdb_scores
    items['poster_url'] = poster_urls

    data_columns = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_csv(data_path, sep='\t', names=data_columns)

    merged = ratings.merge(items[['movie_id', 'title', 'genres', 'imdb_score', 'poster_url']], on='movie_id', how='left')
    merged['watched'] = 1
    return merged

