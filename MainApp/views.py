from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from typing import List
from django.template import loader
from Modules.ContentRecommender import fullContentRecommender, getRecommendationsAsColumn, getRecommendationsByTitle
import Modules.Util as ut
#from Modules.EDA import *
movieData = pd.read_csv('Input/movies_metadata.csv')
movie_list = list(movieData['title'])
movie_list.sort()
moviestoDisplay = 10
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



def displayMovies(df, selectedMovie: str):

    if generateDF:
        movieList = fullContentRecommender(df, selectedMovie, moviestoDisplay)
    else:
        movieList = ut.unpickleObject('Output/Cosine_Sim.pkl')
        #getRecommendationsAsColumn(df, movieList)
        getRecommendationsByTitle(df, 'Heat', movieList)

    #heat
    movies = df[df['title'].isin(movieList)]
    movieHTML = ""
    baseUrl = 'https://image.tmdb.org/t/p/original/'
    movieCount = 1

    for movie in movies:
        movieHTML += processMovie(df, movie, movieCount)
        movieCount+=1
    return movieHTML

def processMovie(df: pd.DataFrame, movie, movieCount):
    movieHTML = ''
    posterLink = movie['poster_path']
    movieHTML += '<img src= "' + posterLink + '" width="33%"'


    if movieCount % 3 == 0:
        movieHTML+='<br>'


