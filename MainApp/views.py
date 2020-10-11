from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from typing import List
from django.template import loader
from Modules.ContentRecommender import fullContentRecommender, getRecommendationsByTitle
import Modules.Util as ut
from Modules.DfManip import *
from Modules.Tmdb import getMovieInfo
import random
import numpy as np

generateDF = False
generateCosineSims = False
if generateDF:
    movieData = processMovieData(generateCosineSims)
else:
    movieData = readDF()

#print(movieData['adult'].value_counts())
movieData = movieData[movieData['adult'] == False]
#print(movieData['adult'].value_counts())
movie_list = processTitles(movieData)
moviestoDisplay = 6


def home_view(request):
    template = loader.get_template('index.html')
    chosenMovie = ''
    if request.method == 'POST':
        if 'selectMovie' in request.POST:
            chosenMovie = request.POST.get('selectedMovie', None)
        else:
            chosenMovie = random.choice(movie_list)

        print('chosenMovie: ' + chosenMovie)

        if chosenMovie in movie_list:
            context = {
                'movie_list': movie_list,
                'recommended_moviesHTML': displayMovies(movieData, chosenMovie),
                'movieValue': chosenMovie,
            }
        else:
            context = {
                'movie_list': movie_list,
                'recommended_moviesHTML': '<span class="infoDiv" style="background-color: rgba(255, 0, 0, 0.6)"> The selected movie could not be found.</div>',
                'movieValue': chosenMovie,
            }

        return HttpResponse(template.render(context, request))

    else:
        context = {
            'movie_list': movie_list,
            'recommended_moviesHTML': '',
            'movieValue': "",
        }
        return HttpResponse(template.render(context, request))

def stringToList(s: str):
    result = s[1:-1]
    result = result.split(',')
    result = [int(s) for s in result]
    return result

def stringToDict(s: str):
    result = s[1:-1]
    result = result.split(',')

    result = {int(s.split(':')[0]): float(s.split(':')[1]) for s in result}
    return result

def displayMovies(df, selectedMovie: str):
    selectedMovie = selectedMovie[0:-7]
    movieList = df[df['title'] == selectedMovie]['similarMovies']
    movieList = movieList.iloc[0]
    movieList = stringToDict(movieList)

    #movieList = movieList[0:moviestoDisplay]
    #movies = df.loc[df['tmdb_id'].isin( list(movieList.keys()))]
    movies = df.iloc[list(movieList.keys())]
    movies = movies.sort_values(by='imdb_score', ascending=False)
    totalMovieHTML = ""
    movieCount = 1

    for index, row in movies.iterrows():
        if movieCount > moviestoDisplay:
            break

        currentMovieHTML = processMovie(df, row, movieCount)

        if currentMovieHTML is None:
            continue
        totalMovieHTML += currentMovieHTML
        movieCount += 1
    return totalMovieHTML

def processMovie(df: pd.DataFrame, movie, movieCount):
    movieHTML = ''
    posterLink, homepage = getMovieInfo(movie)
    if posterLink is None:
        return None

    baseUrl = 'https://image.tmdb.org/t/p/'
    #sizeUrl = 'original'
    #sizeUrl = 'w500'
    sizeUrl = 'w780'

    fullUrl = baseUrl + sizeUrl + posterLink

    homepageExists = homepage != None and homepage != ""
    if homepageExists:
        movieHTML+= '<a href="' + homepage + '">'
    movieHTML += '<img src= "' + fullUrl + '" width="33%" height="70%" alt="' + movie['title'] + ' Poster Here">'

    if homepageExists:
        movieHTML += '</a>'

    print(movie['title'] + ' url: ' + fullUrl)
    if movieCount % 3 == 0:
        movieHTML+='<br>'
    return movieHTML

