from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def normalise_title(title: str) -> str:
    """
    Normalize a movie title by removing the year, handling 'The' at the start,
    and converting to lowercase.

    Args:
        title (str): The original movie title.

    Returns:
        str: The normalized title.
    """
    title = title.split('(')[0].strip()  # Remove year
    if title.lower().startswith("the "):
        title = f"{title[4:].strip()}, The"  # Move 'The' to the end
    return title.lower()  # Convert to lowercase

def find_movie_by_title(user_input: str, movies_df: pd.DataFrame) -> int:
    """
    Find the movie index based on a user input that is case-insensitive 
    and ignores the year in the title.

    Args:
        user_input (str): The user's movie title input.
        movies_df (pd.DataFrame): The DataFrame containing movie titles.

    Returns:
        int: The index of the matched movie.
    """
    # Normalize user input
    normalized_input = normalise_title(user_input)

    # Normalize all movie titles in the DataFrame
    movies_df['normalized_title'] = movies_df['title'].apply(normalise_title)

    # Search for the movie
    matches = movies_df[movies_df['normalized_title'] == normalized_input]
    if matches.empty:
        return ''
    
    return matches.index[0]

def get_content_recommendations(film_title: str, movies_df: pd.DataFrame) -> list:
    """
    Generate content-based movie recommendations using cosine similarity.

    Args:
        film_title (str): The title of the movie to base recommendations on.
        movies_df (pd.DataFrame): DataFrame containing movie details.

    Returns:
        list: A sorted list of similar movies with their similarity scores.
    """
    try:
        # Find the movie index using flexible matching
        movie_index = find_movie_by_title(film_title, movies_df)
        if movie_index == '':
            return []

        # Calculate similarity
        vectorizer = CountVectorizer()
        genre_matrix = vectorizer.fit_transform(movies_df['genres_str'])
        similarity = cosine_similarity(genre_matrix)

        # Sort by similarity
        similar_movies = list(enumerate(similarity[movie_index]))
        similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
        return similar_movies[1:6]  # Skip the first movie (itself)
    
    except Exception as e:
        print(f"Error in content-based recommendations: {e}")
        return []
