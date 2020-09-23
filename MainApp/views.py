from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from typing import List
from django.template import loader
from Modules.ContentRecommender import fullContentRecommender, getRecommendationsAsColumn, getRecommendationsByTitle
import Modules.Util as ut
#from Modules.EDA import *
movieData = pd.read_csv('Input/movies_metadata.csv')
#movieData = movieData.sample(frac=0.10, random_state=1)
movieData.sort_values(by='title', inplace=True)
movieData.reset_index(inplace=True, drop=True)

#movieData.to_csv('Input/movies_metadata.csv')
movie_list = list(movieData['title'])

movie_list.sort()
moviestoDisplay = 6
debug = True
generateDF = False
# Create your views here.
# def home_view(*args, **kwargs):
#     return HttpResponse('<h1>Hello World</h1>')

def home_view(request):
    # data = movieData
    # movieData.to_csv('Input/movies_metadata.csv')
    template = loader.get_template('index.html')
    if request.method == 'POST':
        chosenMovie = request.POST.get('selectedMovie', None)

        context = {
            'movie_list': movie_list,
            'recommended_moviesHTML': displayMovies(movieData, chosenMovie),
        }
        return HttpResponse(template.render(context, request))

    else:
        context = {
            'movie_list': movie_list,
            'recommended_moviesHTML': '',
        }
        return HttpResponse(template.render(context, request))

def stringToList(s: str):
    result = s[2:-2]
    result = result.split(',')
    result = [int(s) for s in result]
    return result

def displayMovies(df, selectedMovie: str):

    if generateDF:
        movieList = fullContentRecommender(df, selectedMovie, moviestoDisplay, skipProcessing=True)
    else:
        # movieList = ut.unpickleObject('Output/Cosine_Sim.pkl')
        # df = getRecommendationsAsColumn(df, movieList)
        movieList = df[df['title'] == selectedMovie]['similarMovies']
        movieList = movieList.iloc[0]
        movieList = stringToList(movieList)
        movieList = movieList[0:moviestoDisplay]



    #movies = df[df['title'].isin(movieList)]
    movies = df.iloc[movieList]
    movieHTML = ""
    movieCount = 1

    for index, row in movies.iterrows():
        movieHTML += processMovie(df, row, movieCount)
        movieCount+=1
    return movieHTML

def processMovie(df: pd.DataFrame, movie, movieCount):
    movieHTML = ''
    posterLink = movie['poster_path']
    baseUrl = 'https://image.tmdb.org/t/p/original/'
    fullUrl = baseUrl + posterLink
    movieHTML += '<img src= "' + fullUrl + '" width="33%" height= "480px">'

    print(movie['title'] + ' url: ' + fullUrl)
    if movieCount % 3 == 0:
        movieHTML+='<br>'
    return movieHTML


