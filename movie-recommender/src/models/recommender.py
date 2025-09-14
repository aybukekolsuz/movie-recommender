import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class Recommender:
    def __init__(self, data):
        self.data = data
        self.model = None
        self.user_profiles = {}

    def preprocess_data(self):
        # Türleri birleştirip yeni bir sütun oluşturuyoruz
        self.data['genres_str'] = self.data['genres'].apply(lambda x: ' '.join(x))
        # Türleri vektörleştiriyoruz
        self.vectorizer = CountVectorizer()
        self.genre_matrix = self.vectorizer.fit_transform(self.data['genres_str'])
        print(self.data['genres'].head())
        print(type(self.data['genres'].iloc[0]))

    def train_model(self):
        # Kullanıcı profillerini oluşturuyoruz (örnek: izlenen filmlerin tür ortalaması)
        for user_id, group in self.data.groupby('user_id'):
            watched = group[group['watched'] == 1]
            if not watched.empty:
                user_profile = watched['genres_str'].str.cat(sep=' ')
                self.user_profiles[user_id] = self.vectorizer.transform([user_profile])
            else:
                self.user_profiles[user_id] = None

    def recommend(self, user_id, num_recommendations=5):
        # Kullanıcıya özel öneri
        if user_id not in self.user_profiles or self.user_profiles[user_id] is None:
            return []
        similarities = cosine_similarity(self.user_profiles[user_id], self.genre_matrix).flatten()
        watched_ids = set(self.data[self.data['user_id'] == user_id]['movie_id'])
        recommendations = [
            self.data.iloc[i]['title']
            for i in similarities.argsort()[::-1]
            if self.data.iloc[i]['movie_id'] not in watched_ids
        ]
        return recommendations[:num_recommendations]

    def evaluate_model(self):
        # Basit bir doğruluk metriği: önerilen filmlerden kaçı sonradan izlenmiş
        total = 0
        correct = 0
        for user_id in self.data['user_id'].unique():
            recs = self.recommend(user_id)
            future_watched = set(self.data[(self.data['user_id'] == user_id) & (self.data['future_watched'] == 1)]['movie_id'])
            correct += len(set(recs) & future_watched)
            total += len(recs)
        return correct / total if total > 0 else 0

    def recommend_by_genre(self, genre, num_recommendations=5):
        # Seçilen türe sahip filmleri filtrele
        filtered = self.data[self.data['genres'].apply(lambda x: genre.lower() in [g.lower() for g in x])]
        # IMDb puanına göre sırala (örnek: 'imdb_score' sütunu varsa)
        filtered = filtered.sort_values(by='imdb_score', ascending=False)
        # En yüksek puanlı filmleri seç
        return filtered.head(num_recommendations)[['title', 'imdb_score', 'poster_url']].to_dict('records')