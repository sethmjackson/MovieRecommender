import pandas as pd
import Modules.Util as ut
## initialize data

def preprocessMovieData(df: pd.DataFrame):
    #df = df[df['id'].str.isnumeric() == True]
    df['id'] = df['id'].astype('int')
    print(df['title'].value_counts())

    ut.convertColumns(df.dropna(), ['revenue', 'budget'], int)
    df['profit'] = df['revenue'] - df['budget']
    df = df.merge(credits, on='id')
    df = df.merge(keywords, on='id')
    return df

movieData = pd.read_csv('Input/movies_metadata.csv')
movieData = movieData.drop(columns=['original_title', 'belongs_to_collection', 'homepage', 'spoken_languages'])
movieData['imdb_score'] = 0
movieData = movieData[['id', 'imdb_id', 'imdb_score', 'title',
                        'release_date', 'budget', 'revenue', 'runtime', 'vote_count', 'vote_average',
                        'popularity', 'status', 'adult',  'video', 'original_language',
                        'genres', 'production_companies', 'production_countries', 'overview', 'tagline', 'poster_path',
                      ]]

credits = pd.read_csv('Input/credits.csv')
credits['id'] = credits['id'].astype('int')

keywords = pd.read_csv('Input/keywords.csv')
keywords['id'] = keywords['id'].astype('int')

links = pd.read_csv('Input/links.csv')
linksSmall = pd.read_csv('Input/links_small.csv')
ratings = pd.read_csv('Input/ratings.csv')
ratings_small = pd.read_csv('Input/ratings_small.csv')

movieData = preprocessMovieData(movieData)

print('Finished EDA','\n')



def plotEDA():
    pass