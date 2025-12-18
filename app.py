import streamlit as st
import pandas as pd
import pickle
import requests

# Function to fetch movie poster from API
def fetch_poster(movie_id):
    api_key = "d47ebc3110af351efd65f415240c01ef"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

    data = response.json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Recommendation function
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_posters = []

        for i in movie_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_posters

    except Exception as e:
        st.error(f"Error: {e}")
        return [], []


# Loading data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Website UI
st.title('🎬 Movie Recommendation System')

option = st.selectbox('Search for a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(option)

    if names:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.text(names[i])
                st.image(posters[i])
    else:
        st.warning("No similar movies found.")
