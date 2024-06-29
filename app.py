import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    try:
        response = requests.get("https://api.themoviedb.org/3/movie/{78}?api_key=4df2402698a306d84976f1a6539071e1&language=en-US")

            # Timeout set to 10 seconds

        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        print(data)
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(poster_url)

    return recommended_movies, recommended_movies_posters


# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app UI
st.header('Movie Recommender System')
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    if names and posters:
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.text("A cat")
                st.image("https://static.streamlit.io/examples/cat.jpg")


