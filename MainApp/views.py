from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from typing import List
from django.template import loader
from Modules.ContentRecommender import fullContentRecommender, getRecommendationsAsColumn, getRecommendationsByTitle
from Modules.SimpleRecommender import getImdbScore
import Modules.Util as ut
#from Modules.EDA import *
from Modules.DfManip import *
from Modules.Tmdb import getMovieInfo
import random

movieData = readDF()
#movieData = movieData.sample(frac=0.10, random_state=1)


#movieData.to_csv('Input/movies_metadata.csv')
movie_list = list(movieData['title'])
movie_list.sort()
moviestoDisplay = 6
generateDF = False

def home_view(request):
    template = loader.get_template('index.html')
    movieValue=""
    if request.method == 'POST':
        if 'selectMovie' in request.POST:
            chosenMovie = request.POST.get('selectedMovie', None)
            movieValue = chosenMovie
        else:
            chosenMovie = random.choice(movie_list)
            #movieValue = chosenMovie
            movieValue = chosenMovie
            print('movieValue: ' + movieValue)


        if chosenMovie in movie_list:
            context = {
                'movie_list': movie_list,
                'recommended_moviesHTML': displayMovies(movieData, chosenMovie),
                'movieValue': movieValue,
            }
        else:
            context = {
                'movie_list': movie_list,
                'recommended_moviesHTML': '<div class="infoDiv"> Error, invalid movie title selected. </div>',
                'movieValue': movieValue,
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


def displayMovies(df, selectedMovie: str):

    if generateDF:
        movieSimilarities = fullContentRecommender(df, selectedMovie, moviestoDisplay)
        getRecommendationsByTitle(df, selectedMovie, movieSimilarities)
        df = getRecommendationsAsColumn(df, movieSimilarities)
    else:
        #movieSimilarities = ut.unpickleObject('Output/Cosine_Sim.pkl')
        pass
    #getRecommendationsByTitle(df, 'Queerama', movieSimilarities)
    #df = getRecommendationsAsColumn(df, movieSimilarities)

    #df = getImdbScore(df)
    #df.to_csv('Input/movies_metadata.csv', index=False)
    movieList = df[df['title'] == selectedMovie]['similarMovies']
    movieList = movieList.iloc[0]
    if isinstance(movieList, str):
        movieList = stringToList(movieList)

    #movieList = movieList[0:moviestoDisplay]
    movies = df.iloc[movieList]
    #movies.sort_values(by = 'imdb_score')


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





# https://image.tmdb.org/t/p/w600_and_h900_bestv2/1P3ZyEq02wcTMd3iE4ebtLvncvH.jpg
#https://image.tmdb.org/t/p/w220_and_h330_face/1P3ZyEq02wcTMd3iE4ebtLvncvH.jpg
def processMovie(df: pd.DataFrame, movie, movieCount):
    movieHTML = ''
    posterLink, homepage = getMovieInfo(movie)
    if posterLink is None:
        return None




    baseUrl = 'https://image.tmdb.org/t/p/'
    #sizeUrl = 'original'
    sizeUrl = 'w500'

    fullUrl = baseUrl + sizeUrl + posterLink

    homepageExists = homepage != None and homepage != ""
    if homepageExists:
        movieHTML+= '<a href="' + homepage + '">'
    movieHTML += '<img src= "' + fullUrl + '" width="33%"  alt="' + movie['title'] + ' Poster Here">'

    if homepageExists:
        movieHTML += '</a>'

    print(movie['title'] + ' url: ' + fullUrl)
    if movieCount % 3 == 0:
        movieHTML+='<br>'
    return movieHTML

