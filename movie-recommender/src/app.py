from flask import Flask, render_template, request
from models.recommender import MovieRecommender

app = Flask(__name__)
recommender = MovieRecommender()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    recommendations = recommender.get_recommendations(user_input)
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)