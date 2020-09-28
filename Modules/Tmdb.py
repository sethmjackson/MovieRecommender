import tmdbsimple as tmdb
from requests import HTTPError

tmdb.API_KEY = '11fead3601fd0a158c49a4d12ebdce88'

def getMovieInfo(movie):
    try:
        m = tmdb.Movies(movie['id'])
        info = m.info()
        #find = tmdb.Find(movie['id'])
        #json = find.info(external_id=movie['imdb_id'],  external_source = 'imdb_id')
        #homepage = info['homepage']

        title = info['title'].lower().replace(' ', '-')
        homepage = 'https://www.themoviedb.org/movie/' + str(info['id']) + '-' + title
        posterPath = info['poster_path']

        if posterPath == None:
            print(movie['title'])
        return posterPath, homepage
    except HTTPError:
        return None, None
# https://api.themoviedb.org/3/find/tt0372784?api_key=11fead3601fd0a158c49a4d12ebdce88&language=en-US&external_source=imdb_id