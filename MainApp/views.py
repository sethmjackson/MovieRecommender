from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from typing import List
from django.template import loader

movieData = pd.read_csv('Input/movies_metadata.csv')
moviestoDisplay = 5
# Create your views here.
# def home_view(*args, **kwargs):
#     return HttpResponse('<h1>Hello World</h1>')
def home_view(request):
    movie_list = list(movieData['title'])
    template = loader.get_template('index.html')
    context = {
        'movie_list': movie_list,
    }
    return HttpResponse(template.render(context, request))



def displayMovies(df: pd.DataFrame, movieList: List[int]):
    movies = df[df['id'].isin(movieList)]
    movieHTML = ""
    baseUrl = 'https://image.tmdb.org/t/p/original/'

    for row in movies:
        posterLinks = row['poster_path']

    return movieHTML
