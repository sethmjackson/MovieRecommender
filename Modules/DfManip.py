import pandas as pd
import Modules.Util as ut
from matplotlib import pyplot as plt
from Modules.ContentRecommender import fullContentRecommender, getRecommendationsByTitle
import matplotlib as mpl
import matplotlib.ticker as mtick

def readDF(fileName = 'Output/movies_metadata.csv'):
    df = pd.read_csv(fileName)
    nullRecommendations = ut.getRowsNum(df[df['similarMovies'] == -1])
    print('Null Movie Recommendations: ' + str(nullRecommendations))

    if nullRecommendations > 0:
        time, cosineSim = ut.getExecutionTime(lambda: ut.unpickleObject('Output/Cosine_Sim.pkl'))
        ut.getExecutionTime(lambda: getRecommendationsAsColumn(df, cosineSim))
    return df

def compressDF(df: pd.DataFrame):
    columns = ['budget', 'revenue', 'runtime', 'vote_count', 'vote_average', 'popularity',
                     'status', 'original_language', 'production_companies', 'production_countries',
                     'overview', 'tagline', 'poster_path', 'crew', 'keywords', 'video', 'cast', 'keywords',
                'original_title', 'belongs_to_collection', 'homepage', 'spoken_languages'
               ]
    ut.dropIfExists(df, columns, inplace=True)

def saveDF(df: pd.DataFrame):
    df.to_csv('Output/movies_metadata.csv', index=False)

def addImdbScore(df: pd.DataFrame):
    v = df['vote_count']
    r = df['vote_average']
    m = df['vote_count'].quantile(0.90)
    c = df['vote_average'].mean()
    df['imdb_score'] = (v*r/(v+m)) + (m/(v+m)*c)
    return df

def processMovieData(generateCosineSim: bool):

    ## open dataframe
    df = pd.read_csv('Input/movies_metadata (original).csv')
    df = addImdbScore(df)
    ## drop movies without release date
    df = df.apply(lambda x: x if isinstance(x['release_date'],str) else None, axis=1)
    df.dropna(how='all', inplace=True)

    df['tmdb_id'] = df.index
    df = df.sort_values(by='imdb_score', ascending=False)
    df.reset_index(inplace=True, drop=True)

    df['release_year'] = df['release_date'].apply(lambda date: date[0:4])

    df = df[['tmdb_id', 'id', 'imdb_id', 'imdb_score', 'title',
             'release_date', 'release_year', 'adult', 'genres'
           ]]

    ## merge credits and keywords into movieData
    credits = pd.read_csv('Input/credits.csv')
    credits['id'] = credits['id'].astype('int')
    keywords = pd.read_csv('Input/keywords.csv')
    keywords['id'] = keywords['id'].astype('int')

    df = df[df['id'].str.isnumeric() == True]
    df['id'] = df['id'].astype('int')
    df = df.merge(credits, on='id')
    df = df.merge(keywords, on='id')
    df = df[df.apply(lambda x: isinstance(x['title'], str), axis=1)]
    df['similarMovies'] = -1

## Add column of recommended movies
    if generateCosineSim:
        time, cosineSim = ut.getExecutionTime(lambda: fullContentRecommender(df))
    else:
        time, cosineSim = ut.getExecutionTime(lambda: ut.unpickleObject('Output/Cosine_Sim.pkl'))
    compressDF(df)
    ut.getExecutionTime(lambda: getRecommendationsAsColumn(df, cosineSim))
    return df

def processTitles(df: pd.DataFrame):
    return list(df.apply(lambda row: row['title'] + ' ('+str(row['release_year'])+')', axis=1))

def getRecommendationsAsColumn(df: pd.DataFrame, cosine_sim, recommendationsNum=20):

    #df['similarMovies'] = df.apply(lambda row: getRecommendationsByTitle(df, row['title'], cosine_sim, recommendationsNum), axis=1)
    for index, row in df.iterrows():
        if row['similarMovies'] != -1:
            continue
        recommendations = getRecommendationsByTitle(df, row['title'], cosine_sim, recommendationsNum, index)
        df.loc[index, 'similarMovies'] = str(recommendations)
        if index % 100 == 0:
            saveDF(df)
            print('last index saved is: ', str(index))
    saveDF(df)

def plotSimilarityScores(df: pd.DataFrame):
    movieList = df['similarMovies']
    movieList = movieList.apply(lambda x: ut.stringToDict(x))
    df['scoreRange'] = movieList.apply(lambda x: max(x.values()) - min(x.values()))
    df['scoreAverage'] = movieList.apply(lambda x: sum(x.values()) / len(x.values()))

    histDir = 'Output/Histograms/'
    scatterDir = 'Output/Scatterplots/'
    barDir = 'Output/Barplots/'

    histParams = {'kind': 'hist', 'legend': False, 'bins': 50}
    barParams = {'kind': 'bar', 'legend': False}
    figParams = {'x': 7, 'y': 7}

    plt.rc('font', size=40)
    plt.rc('axes', labelsize=60)
    plt.rc('axes', titlesize=60)
    xTickMult = lambda: ut.multiplyRange(plt.xticks()[0], 0.5)
    xTickMultLS = lambda: ut.multiplyLinSpace(plt.xticks()[0], 2)
    yTickFormat = lambda: plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
    xTickFormatPercent = lambda: plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    xTickFormatCommas = lambda: plt.gca().xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    xTickFormatDollars = lambda x=0: plt.gca().xaxis.set_major_formatter(
    mpl.ticker.StrMethodFormatter('${x:,.' + str(x) + 'f}'))
    # setTickIn = lambda: plt.gca().tick_params(axis='x', direction='in')
    trimTicks = lambda: plt.xticks()[0:-1]
    histParams = {'kind': 'hist', 'legend': False, 'bins': 100}

    ut.plotDF(df[['scoreRange']], histParams,
           {
            'grid': None,
            'xlabel': 'Range Between Highest and Lowest Similarity Scores',
            'title': 'Histogram of Similarity Score Ranges',
            'savefig': histDir + 'ScoreRange.png'})

    ut.plotDF(df[['scoreAverage']], histParams,
           {
            'grid': None,
            'xlabel': 'Average Similarity Scores',
            'title': 'Histogram of Similarity Score Averages',
            'savefig': histDir + 'ScoreAverages.png'})

    print('finished plotting')




