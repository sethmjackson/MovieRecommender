
#creates dfs from file, prints relevent data
from Modules.EDA import *
import pandas as pd
import Modules.Util as ut
import Modules.Plots as plots
import pickle
from Modules.SimpleRecommender import getImdbScore
from Modules.ContentRecommender import getRecommendations, plotRecommender, fullContentRecommender

import django
## impute data
movieData = getImdbScore(movieData)
movieData.to_csv('Input/movies_metadata.csv')
#movieData.sort_values(by='imdb_score', ascending=False, inplace=True)
#title = 'The Dark Knight Rises'
title = 'The Godfather'
#plotRec = plotRecommender(movieData, title)
contentRec = fullContentRecommender(movieData, title)
print('')




