import streamlit as st
import pickle
import pandas as pd
import requests


# Now fetching the poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url).json()

    if 'poster_path' in data and data['poster_path'] is not None:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    list_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in list_movies:
        movie_id = movies.iloc[i[0]]['id']  # this will contain the movie id
        recommended_movies.append(movies.iloc[i[0]]['title'])
        # Fetching the poster
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies['title'].values

st.title('Movie Recommender System')
selected_movie = st.selectbox(
    'Type or select movie from drop down',
    movies_list)
if st.button('Recommend'):
    recommended_movies, recommended_movies_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movies_posters[1])

    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movies_posters[4])
