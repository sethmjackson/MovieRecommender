# MovieRecommender
A classic problem people have is finding a good movie to watch without doing a lot of research. To overcome this problem, recommender systems based on Machine Learning or Deep Learning are used to find movies that users are most likely to enjoy. There are 2 main types of recommender systems: Content Filtering (finds similarities between movies by their data), and Collaborative Filtering (finds similar movies by ratings and other data from users). This project uses Django to create a web application that allows the user to choose a movie and uses Content Filtering to recommend movies that are most similar to the one chosen by the user.

## Content Filtering
Content Filtering is performed on [The Movies Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset), which contains metadata for over 45,000 movies. The main idea behind Content Filtering is that if a user likes a movie, then they will probably like other movies that are similar to it. Movie similarity is determined by the following metadata: Cast, Director, Keywords, and Genre. The metadata is text based, so some basic natural language processing is required before it can compare movies.

Processing the data involves the following steps:

1. Removing stop words such as the, and, or, etc. They add no relevant information, so they are not useful for most types of analysis.
2. Finding the director of the movie from the cast so the director has their own category.
3. Removing spaces between words. This is done so that names and other multiple word terms like "Johnny Depp" and "Johnny Galecki" are not treated the same.
4. Creating a metadata soup by appending each processed category to each other.

After the data is processed, Scikit-learn's CountVectorizer function is used to compute the similarity between movies by their metadata soup. Essentially, it takes the words in the soup and converts them into word vectors. Then, it performs a Cosine Similarity algorithm to compute the angle between word vectors. The smaller the angle between vectors, the more similar they are. The CountVectorizer creates a matrix with similarity scores for each pair of movies. For each movie, the scores were sorted to find the 10 most similar movies, which were added as a column to the dataframe, so they would not need to be calculated at runtime.

## Django Application
![application screenshot](https://github.com/sethmjackson/MovieRecommender/blob/master/Output/Application%20Image.png)

Python has many libraries for creating a web application. Django is the most popular, thus it was chosen for this project. The app starts with a textbox where the user types a movie title. The textfield has autocomplete to make finding the desired movie quick and easy. Users can also select a random movie to find recommendations by clicking the "Surprise Me" button. Once the desired movie is selected, the "Get Selected Movies" button will get the 6 most similar movies, download their posters, and clicking on a poster will take the user to that movies' TMDB Page. The similarity scores and IMDB scores for each recommended movie are also displayed.

## TMDB
The Movie Database, also known as [TMDB](https://www.themoviedb.org/), is a database that contains detailed information on over 500,000 movies. The Movies dataframe has links to the movie posters in it, but the vast majority of them are outdated and no longer work. In order to find the poster links, the tmdbsimple library, which acts as a Python wrapper for the TMDB API was used. The ID of the movie is all that it takes to obtain that movie's updated information. The TMDB website has a simple structure to its URLs, therefore getting the link to each movie's page involves taking the base site link and adding the id of the movie, a dash, and the movie title.

## Web Deployment
[Heroku](https://www.heroku.com/) is a service that allows web applications from many languages to be deployed to a server for free. Heroku supports Django, and has Github integration, consequently each push onto the associated Github project will recompile the app and deploy it within minutes. There are some extra steps that need to be taken so that the Heroku server can install and run the libraries used in the application, but once it worked, it performed really well. A link to the Heroku server hosting the application can be found [here](https://django-movie-recommender.herokuapp.com/).

## Conclusion
It is difficult to determine the effectiveness of a recommendation system, especially without data from active users. To find some measure to evaluate, I plotted some data related to the similarity scores.

![Score Range](https://github.com/sethmjackson/MovieRecommender/blob/master/Output/Histograms/ScoreRange.png)
![Score Averages](https://github.com/sethmjackson/MovieRecommender/blob/master/Output/Histograms/ScoreAverages.png)
What these plots reveal is that the average of the similarity scores for each movie's recommendations is normally distributed, with most movies having scores between 0.3 and 0.5. The Ranges between the highest and lowest similarity scores is not normally distributed. Most values are between 0.1 and 0.2, but there are a surprising number of movies with a score range between 0.4 and 0.6. This seems to indicate that there are some movies that have recommendations that don't fit very well. There are 20 recommendations stored per movie, so perhaps after some point, the recommended movies are a poor fit.

## Future Work
If given more time, I would include Collaborative Filtering in my recommender, which would include obtaining reviews and other user generated data by using the millions of reviews in the movies dataset to find similarities between users that make it more effective at recommending movies.

Another option is to avoid using The Movies Dataset altogether and having my app use the TMDB database itself as the source of its data. This would allow the recommender to increase the number of movies by an order of magnitude.

Finally, I would add additional features to the application to allow the user to restrict the types of movies that can be randomly selected by rating, year, foreign/domestic, etc. 
