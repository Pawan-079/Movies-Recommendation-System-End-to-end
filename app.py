import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = "8e41a8b0db301ec5d1612e6eb9c6df92"  # Replace with your actual API key

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US")
    data = response.json()
    if 'poster_path' in data:
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    else:
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index
    if len(movie_index) == 0:
        return [], []

    movie_index = movie_index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_posters.append(poster_url)

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movies Recommender System')

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    for i in range(min(len(names), 6)):
        st.subheader(names[i])
        st.image(posters[i] if i < len(posters) else "https://via.placeholder.com/500x750.png?text=No+Poster+Available")