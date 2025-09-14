from flask import Flask, render_template, request
from utils.data_loader import load_movielens_data
from models.recommender import Recommender

app = Flask(__name__)

# Veri dosya yolunu belirt
item_path = "data/u.item"
data_path = "data/u.data"
omdb_api_key = "b4d14332"

# Veriyi yükle ve ön işle
data = load_movielens_data(item_path, data_path, omdb_api_key)
if data is not None:
    recommender = Recommender(data)
    recommender.preprocess_data()
    recommender.train_model()
else:
    print("Veri yüklenemedi.")

@app.route('/')
def home():
    return render_template('index.html', recommendations=None)

@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form.get('genre')
    try:
        recommended_titles = recommender.recommend_by_genre(genre)
    except Exception as e:
        recommended_titles = [f"Hata: {e}"]
    return render_template('index.html', recommendations=recommended_titles)

if __name__ == '__main__':
    app.run(debug=True)