import pandas as pd

def getImdbScore(df: pd.DataFrame):
    v = df['vote_count']
    r = df['vote_average']
    m = df['vote_count'].quantile(0.90)
    c = df['vote_average'].mean()
    df['imdb_score'] = (v*r/(v+m)) + (m/(v+m)*c)
    return df