import random
import json
import requests
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
from preprocess import *
from streamlit_text_rating.st_text_rater import st_text_rater
import streamlit as st
from streamlit_star_rating import st_star_rating
import ast


# FOR LOCATION
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L 

data_ = pd.read_csv(
    'C:/Users/yukti/OneDrive/Desktop/Emotion-Detection-from-Text-using-Neural-Netwroks-main/tmdb_5000_movies.csv')
df12_ = pd.DataFrame(data_)
# print(data_)
data_['production_countries'] = data_['production_countries'].apply(convert)
c = []
for i in data_['production_countries']:
    for j in i:
        if j not in c:
            c.append(j)

# print(c)

st.sidebar.subheader("What's on top of your mind!!")


def user_input():
    text = st.sidebar.text_input('Write your thought! ')

    return text



input = user_input()



# st.write(input)
encoder = pickle.load(open('encoder.pkl', 'rb'))
cv = pickle.load(open('CountVectorizer.pkl', 'rb'))


model = tf.keras.models.load_model('my_model.h5')
input = preprocess(input)

array = cv.transform([input]).toarray()

pred = model.predict(array)
a = np.argmax(pred, axis=1)
prediction = encoder.inverse_transform(a)[0]
print(prediction)

mood = ""
if input == '':
    st.write('')
else:
    mood = prediction

st.header('Movie Recommender System')

# st.subheader("Recommendation on the basis of content")


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=208a5adae34de4dc409b5c6950954ff7&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie, selected_location):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances:
        # fetch the movie poster
        if len(recommended_movie_names)>=5 and len(recommended_movie_posters)>=5:
            break
        if(i[0]<len(data_)):
            if(selected_location in data_.iloc[i[0]].production_countries):
                movie_id = movies.iloc[i[0]].movie_id
                recommended_movie_posters.append(fetch_poster(movie_id))
                recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

def countries():
    c = []
    for i in movies["production_countries"]:
        for j in i:
            if j not in c:
                c.append(j)

def feedback():
    label = "User Rating"
    stars = st_star_rating(label, 5,defaultValue=0, size=20)


movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(
    open('C:/Users/yukti/OneDrive/Desktop/Emotion-Detection-from-Text-using-Neural-Netwroks-main/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_location = st.selectbox("Select your location",c )
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie, selected_location)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if(len(recommended_movie_names)>0 and len(recommended_movie_posters)>0):
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        else:
            print("NO RECOMMENDATIONS")
    with col2:
        if(len(recommended_movie_names)>1 and len(recommended_movie_posters)>1):
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
    with col3:
        if(len(recommended_movie_names)>2 and len(recommended_movie_posters)>2):
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
    with col4:
        if(len(recommended_movie_names)>3 and len(recommended_movie_posters)>3):
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
    with col5:
        if(len(recommended_movie_names)>4 and len(recommended_movie_posters)>4):
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])

    feedback()






st.subheader("Recommendation on the basis of mood")

data = pd.read_csv(
    'C:/Users/yukti/OneDrive/Desktop/Emotion-Detection-from-Text-using-Neural-Netwroks-main/tmdb_5000_movies.csv')
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
df = df.melt(id_vars=["vote_average",  "title", "id"], value_vars=df.columns[1:],
             value_name="name")[["vote_average", "title", "id", "name"]].dropna()


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
    top_movies1 = sorted_data['title'].iloc[:15].tolist()
    top_movies_id1 = sorted_data['id'].iloc[:15].tolist()
    top_movies = random.sample(top_movies1, 5)
    top_movies_id = [id for val, id in zip(
        top_movies1, top_movies_id1) if val in top_movies]
    for i in top_movies_id:
        recommended_movie_posters.append(fetch_poster(i))
    return top_movies, recommended_movie_posters


# col1, col2, col3, col4, col5 = st.columns(5)

# with col1:
#     button1 = st.button("Happy Mood😃")

# with col2:
#     button2 = st.button('Sad Mood😞')

# with col3:
#     button3 = st.button('Chill Mood🤩')

# with col4:
#     button4 = st.button('Adventurous Mood🎬')
# with col5:
#     button5 = st.button('Romantic Mood😍')


mood1 = ""
if mood == "joy":
    mood1 = "Drama"
    st.button("It seems you are Happy!!😃")
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
    feedback()

elif mood == "sadness":
    mood1 = "War"
    st.button("It seems you are sad!!😃")
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
    feedback()
elif mood == "surprised":
    mood1 = "Comedy"
    st.button("It seems you are surprised!!😃")
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
    feedback()
elif mood == "fear":
    mood1 = "Action"
    st.button("It seems you are fear!!😃")
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
    feedback()
elif mood == "love":
    mood1 = "Romance"
    st.button("It seems you are love!!😃")
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
    feedback()
elif mood == "anger":
    mood1 = "Romance"
    st.button("It seems you are angry!!😃")
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
    feedback()
