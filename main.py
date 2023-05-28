import pickle

import requests
import streamlit as st

st.markdown(
    """
    <style>
    body {
        background-color: #f2f2f2;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 10px;
    }
    .header{
    	font-size : 130 px;
        align-items : center ;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        display : flex;
        flex-wrap: wrap;
        justify-content: space-around;
        
    }
    .movie {
        margin-bottom: 20px;
        text-align: center;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-radius: 4px;
        overflow: hidden;
        transition: transform 0.3s ease-in-out;
        cursor: pointer;
    }
    .movie:hover {
        transform: translateY(-5px);
    }
    .movie.selected {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        transform: scale(1.1);
        
    }
    .movie:hover .movie-details {
        display: block;
        width: 100%;
        
        z-index: 21;
    }
    .movie img {
        width: 100%;
        height: auto;
        object-fit: cover;
    }
    .movie-details {
        width: 100%;
        height: auto;
        display: none;
        padding: 10px;
        background-color: #f5f5f5;
        font-size: 8px;
        z-index: -1;
    }
    .movie-title {
        font-weight: bold;
        margin-top: 5px;
        color: #333333;
        font-size: 12px;
    }
    .movie-similarity {
        font-size: 8px;
        color: #777777;
    }
    .movie-overview {
        margin-top: 7px;
        color: #555555;
        display: block;
        font-size: 10px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id
    )
    data = requests.get(url)
    data = data.json()
    poster_path = data["poster_path"]
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path, data


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_similarity = []
    recommended_movie_details = []
    for i in distances[1:16]:  # Updated to display 15 movies
        # fetch the movie poster and details
        movie_id = movies.iloc[i[0]].movie_id
        poster_path, movie_details = fetch_poster(movie_id)
        recommended_movie_posters.append(poster_path)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_similarity.append(i[1])
        recommended_movie_details.append(movie_details)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_similarity, recommended_movie_details


st.header(' :blue[Movie Recommender System]')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_similarity, recommended_movie_details = recommend(
        selected_movie)
    cols = st.columns(10)  # Updated with 10 columns
    for i in range(10):
        with cols[i]:
            selected_class = "selected" 
            st.markdown(
                "<div class='movie {}'>"
                "<img src='{}' alt='movie poster' width='500'>"
                "<div class='movie-details'>"
                "<h4 class='movie-title'>{}</h4>"
                "<p class='movie-similarity'>Similarity: {:.2f}</p>"
                "<p class='movie-overview'><b>Overview:</b> {}</p>"
                "</div>"
                "</div>".format(
                    selected_class,
                    recommended_movie_posters[i],
                    recommended_movie_names[i],
                    recommended_movie_similarity[i],
                    recommended_movie_details[i]['overview']
                ),
                unsafe_allow_html=True
            )
