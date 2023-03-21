import streamlit as st
import requests
import json
import pandas as pd
import pickle

st.header('Movie Recommender System')

st.subheader("Recommendation on the basis of content")
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=208a5adae34de4dc409b5c6950954ff7&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


movies = pickle.load(open('D:ir/movie_list.pkl','rb'))
similarity = pickle.load(open('D:/ir/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])





st.subheader("Recommendation on the basis of mood")

# Load the movie titles and genres dataset
data = pd.read_csv(
    'D:/ir/tmdb_5000_movies.csv')
df12 = pd.DataFrame(data)
data1 = data.loc[:, 'genres']

for i in range(len(data1)):
    string = data1[i]
    list_of_dicts = json.loads(string)
    data1[i] = list_of_dicts

df = pd.DataFrame(data1)
genres_list = data["genres"].apply(lambda x: [y["name"] for y in x]).explode()
# genres_list.unique()
df["genres"] = df["genres"].apply(lambda x: [y.get("name") for y in x])
df1 = pd.DataFrame(df["genres"].values.tolist())
df1.columns = ["name_{}".format(x) for x in range(len(df1.columns))]
df12['genres'] = df['genres']

df1 = pd.concat([df12[["id"]], df1], axis=1)
df1 = pd.concat([df12[["title"]], df1], axis=1)

df = pd.concat([df12[["vote_average"]], df1], axis=1)
df = df.melt(id_vars=["vote_average",  "title" , "id"], value_vars=df.columns[1:],
             value_name="name")[["vote_average","title","id", "name"]].dropna()


def suggest_movie(genre, mood):
    recommended_movie_posters = []
    # Filter the movies by genre and mood
    genre_data = df[df['name'] == genre]
    # print(genre_data)
    mood_data = genre_data[genre_data['name'] == mood]
    # print(mood_data)
    # Sort the movies by rating in descending order
    sorted_data = mood_data.sort_values('vote_average', ascending=False)
    # print(sorted_data['title'].loc[:10])
    # Return the top 10 movie titles
    # print(sorted_data['title'])
    top_movies = sorted_data['title'].iloc[:5].tolist()
    top_movies_id = sorted_data['id'].iloc[:5].tolist()
    for i in top_movies_id:
        recommended_movie_posters.append(fetch_poster(i))
    return top_movies, recommended_movie_posters


mood = ""


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    button1 = st.button("Happy Mood😃")

with col2:
    button2 = st.button('Sad Mood😞')

with col3:
    button3 = st.button('Chill Mood🤩')

with col4:
    button4 = st.button('Adventurous Mood🎬')
with col5:
    button5 = st.button('Romantic Mood😍')

if button1:
    mood = "happy"
if button2:
    mood = "sad"
if button3:
    mood = "chill"
if button4:
    mood = "adventurous"
if button5:
    mood = "romantic"

suggest_movie("Happy Mood", "happy")
mood1 = ""
if mood == "happy":
    mood1 = "Drama"
    romantic_movies, romantic_movies_posters = suggest_movie(mood1, mood1)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(romantic_movies[0])
        st.image(romantic_movies_posters[0])
    with col2:
        st.text(romantic_movies[1])
        st.image(romantic_movies_posters[1])

    with col3:
        st.text(romantic_movies[2])
        st.image(romantic_movies_posters[2])
    with col4:
        st.text(romantic_movies[3])
        st.image(romantic_movies_posters[3])
    with col5:
        st.text(romantic_movies[4])
        st.image(romantic_movies_posters[4])
elif mood == "sad":
    mood1 = "War"
    romantic_movies, romantic_movies_posters = suggest_movie(mood1, mood1)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(romantic_movies[0])
        st.image(romantic_movies_posters[0])
    with col2:
        st.text(romantic_movies[1])
        st.image(romantic_movies_posters[1])

    with col3:
        st.text(romantic_movies[2])
        st.image(romantic_movies_posters[2])
    with col4:
        st.text(romantic_movies[3])
        st.image(romantic_movies_posters[3])
    with col5:
        st.text(romantic_movies[4])
        st.image(romantic_movies_posters[4])
elif mood == "chill":
    mood1 = "Comedy"
    romantic_movies, romantic_movies_posters = suggest_movie(mood1, mood1)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(romantic_movies[0])
        st.image(romantic_movies_posters[0])
    with col2:
        st.text(romantic_movies[1])
        st.image(romantic_movies_posters[1])

    with col3:
        st.text(romantic_movies[2])
        st.image(romantic_movies_posters[2])
    with col4:
        st.text(romantic_movies[3])
        st.image(romantic_movies_posters[3])
    with col5:
        st.text(romantic_movies[4])
        st.image(romantic_movies_posters[4])
elif mood == "adventurous":
    mood1 = "Action"
    romantic_movies, romantic_movies_posters = suggest_movie(mood1, mood1)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(romantic_movies[0])
        st.image(romantic_movies_posters[0])
    with col2:
        st.text(romantic_movies[1])
        st.image(romantic_movies_posters[1])

    with col3:
        st.text(romantic_movies[2])
        st.image(romantic_movies_posters[2])
    with col4:
        st.text(romantic_movies[3])
        st.image(romantic_movies_posters[3])
    with col5:
        st.text(romantic_movies[4])
        st.image(romantic_movies_posters[4])
elif mood == "romantic":
    mood1 = "Romance"
    romantic_movies, romantic_movies_posters = suggest_movie(mood1, mood1)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(romantic_movies[0])
        st.image(romantic_movies_posters[0])
    with col2:
        st.text(romantic_movies[1])
        st.image(romantic_movies_posters[1])

    with col3:
        st.text(romantic_movies[2])
        st.image(romantic_movies_posters[2])
    with col4:
        st.text(romantic_movies[3])
        st.image(romantic_movies_posters[3])
    with col5:
        st.text(romantic_movies[4])
        st.image(romantic_movies_posters[4])

