import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text  import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

df_movies = pd.read_csv('movies_imdb.csv') 
df_movies.head()
df_movies = df_movies.rename(columns={'Unnamed: 0': 'movie_id' })

#function to create the new df for the nlp calculating
def import_features(df_movies):
    dataset = df_movies.copy()
    for i in range(0,df_movies.shape[0]):
        dataset['Tags'] = dataset['Movie Name']+' '+ dataset['Genres']+' '+dataset['Director']+' '+ dataset['Description']
    return dataset


dataset = import_features(df_movies)
dataset['Tags'] = dataset['Tags'].fillna('')
# dataset['Tags']

#NLP 
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(dataset['Tags'])
cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)

#make a series with all the keyword 
indices = pd.Series(dataset.index, index = dataset['Movie Name']).drop_duplicates()
# indices
# indices['The Dark Knight']


#FUNCTION THAT BRING RECCOMEND WITH MOVIE NAME - case sensitive
def get_reccommendation_other_movies(title,cosine_sim = cosine_sim):
    '''
        this function return df with movies by similarity froem selected movie
    '''
    try:
        #title.casefold()
        idx = indices[title]
        sim_scores = enumerate(cosine_sim[idx])
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        sim_index = [i[0] for i in sim_scores]
        #print(dataset[['Movie Name','Photo URL']].iloc[sim_index])
        return(dataset[['Movie Name','Photo URL']].iloc[sim_index])
    except KeyError:
        #print(f"Movie '{title}' not found in the dataset.")
        return(f"Movie '{title}' not found in the dataset.")

# u = get_reccommendation_other_movies('The Dark Knight')
# print(u)        

def recommend_by_genre(pref_genres,df=df_movies):
    '''
    this function return df with movies by selected genre
    '''
    df_genre = df.copy()
    df_genre['Genres'] = df_genre['Genres'].fillna('')
    condition_genres = df_genre['Genres'].str.contains(pref_genres,case=False)
    user_movies = df_genre[condition_genres]
    if user_movies.empty:
        return('No Movies For this Genre\s')
    else:
        random_movies = user_movies.sample(min(10, user_movies.shape[0]))
        return(random_movies[['Movie Name','Photo URL']])

# ac = 'action'
# res = recommend_by_genre(ac)
# print(res)

def recommend_by_director(pref_director,df = df_movies):
    '''
    this function return df with movies by selected director
    '''
    df_director = df.copy()
    df_director['Director'] = df_director['Director'].fillna('')
    condition_director = df_director['Director'].str.contains(pref_director,case=False)
    user_movies = df_director[condition_director]
    if user_movies.empty:
        return('No Movies For this Director')
    else:
        return(user_movies[['Movie Name','Photo URL']])



def recommend_by_duration(duration_range=None,df=df_movies):
    '''
        this function return df with movies by selected duration
    '''
    if duration_range and duration_range[0] > duration_range[1]:
        print("Invalid duration range. The start duration cannot be greater than the end duration.")
        return
    
    condition_duration = df['Duration (Min)'].between(duration_range[0], duration_range[1]) if duration_range else False
    user_movies = df[condition_duration]
    if user_movies.empty:
        return('No Movies For This Duration')
    else:
        return(user_movies[['Movie Name','Photo URL']])


def load_image_from_url(url):
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    return ImageTk.PhotoImage(img)


#image_url = 'https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_UX140_CR0,0,140,209_AL_.jpg'











# # Example usage:
# user_input_genres = None
# user_input_director = 'christopher nolan'
# duration_range_input = None  
# recommend_movies_by_preferences(user_genres=user_input_genres, user_director=user_input_director, duration_range=duration_range_input)