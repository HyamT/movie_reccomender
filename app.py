from flask import Flask, render_template, request
from models.reccomender import get_content_recommendations
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route('/')  
def home():
    return render_template('home.html')

@app.route('/recommend', methods=['POST'])

def recommend():
    # Get user input from the form
    film_title = request.form['film_title']

    connection = sqlite3.connect('movies.db')
    movies_df = pd.read_sql_query("SELECT * FROM movies", connection)
    movies_df['genres_str'] = movies_df['genres'].str.replace('|', ' ')  # Pre-process genres
    # Generate recommendations
    try:
        recommendations = get_content_recommendations(film_title, movies_df)
        if not recommendations:
            return render_template('error.html', film_title=film_title)
        
        connection.close()
        return render_template('results.html', film_title=film_title, recommendations=recommendations, movies_df=movies_df)
    except ValueError as e:
        connection.close()
        return render_template('home.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
