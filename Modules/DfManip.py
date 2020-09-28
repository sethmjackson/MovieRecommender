import pandas as pd

def readDF(fileName = 'Input/movies_metadata.csv'):
    return pd.read_csv(fileName)

def compressDF(df: pd.DataFrame):
    df.drop(columns=['budget', 'revenue', 'runtime', 'vote_count', 'vote_average', 'popularity',
                     'status', 'adult', 'video', 'original_language', 'production_companies', 'production_countries',
                     'overview', 'tagline', 'poster_path', 'crew'], inplace=True)

def saveDF(df: pd.DataFrame):
    df.to_csv('Input/movies_metadata.csv', index=False)