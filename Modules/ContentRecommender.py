from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from ast import literal_eval
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import Modules.Util as ut

def getIndexFromTitle(df: pd.DataFrame, title):
    if isinstance(title, str):
        titles = df[df['title'] == title]
        titles = pd.Series(titles.index, index=titles['title'])
        index = titles[0]
    else:
        index = title
    return index


def plotRecommender(df: pd.DataFrame, title: str):
    tfidf = TfidfVectorizer(stop_words='english')
    
    #Replace NaN with an empty string
    df['overview'] = df['overview'].fillna('')
    
    #Construct the required TF-IDF matrix by fitting and transforming the data
    vector_matrix = tfidf.fit_transform(df['overview'])

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(vector_matrix, vector_matrix)
    return getRecommendationsByTitle(df, title, cosine_sim)


def getRecommendationsByTitle(df: pd.DataFrame, title, cosine_sim, recommendationsNum=20, index=-1):

    if index < 0:
        index = getIndexFromTitle(df, title)
    print('Getting recommendations for index ' + str(index)+': ' + title)
    similarityScores = list(enumerate(cosine_sim[index]))

    recommendationsNum += 1
    similarityScores = sorted(similarityScores, key=lambda x: x[1], reverse=True)
    similarityScores = similarityScores[1:recommendationsNum]
    movieIndexes     = [i[0] for i in similarityScores]
    scores           = [i[1] for i in similarityScores]


    #result = df['title'].iloc[movieIndexes]
    #result = result.tolist()
    result = dict(zip(movieIndexes, scores))
    return result

def extractFeatures(df: pd.DataFrame):
    print('in extractFeatures')
    features = ['cast', 'crew', 'keywords', 'genres']
    for f in features:
        df[f] = df[f].apply(literal_eval)

def getDirector(crewList):
    for member in crewList:
        if member['job'] == 'Director':
            return member['name']
    return np.nan

def get_list(metadataList):
    if isinstance(metadataList, list):
        names = [i['name'] for i in metadataList]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names
    else:
        return metadataList

def removeSpaces(metadataList):
    if isinstance(metadataList, list):
        return [str.lower(i.replace(" ", "")) for i in metadataList]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(metadataList, str):
            return str.lower(metadataList.replace(" ", ""))
        else:
            return ''

def stirSoup(movieDataRow):
        return ' '.join(movieDataRow['keywords']) + ' ' + ' '.join(movieDataRow['cast']) + ' ' + movieDataRow['director'] + ' ' + ' '.join(movieDataRow['genres'])

def fullContentRecommender(df: pd.DataFrame):
    print('in fullContentRecommender')
    extractFeatures(df)
    df['director'] = df['crew'].apply(getDirector)
    features = ['cast', 'keywords', 'genres']

    for feature in features:
        df[feature] = df[feature].apply(get_list)

    features.append('director')
    for feature in features:
        df[feature] = df[feature].apply(removeSpaces)

    df['soup'] = df.apply(stirSoup, axis=1)


    print('before vectorizer')
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(df['soup'])
    contentCosineSim = cosine_similarity(count_matrix, count_matrix)
    ut.pickleObject(contentCosineSim, 'Output/Cosine_Sim.pkl')

    features.append('soup')
    df.drop(columns=features, inplace=True)

    print('after vectorizer')
    return contentCosineSim

