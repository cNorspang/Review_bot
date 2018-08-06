#! python3

# Imports
import praw
import Config
import time
import imdb
from rotten_tomatoes_client import RottenTomatoesClient
import requests
import APILeaning

key = APILeaning.key
host = APILeaning.Host

ia = imdb.IMDb()

subreddits = 'WikipediaBotTest'
# Making the bot login to reddit


def bot_login():
    r = praw.Reddit(username=Config.username,
                    password=Config.password,
                    client_id=Config.client_id,
                    client_secret=Config.client_secret,
                    user_agent="NolleDK's test review bot")
    return r

# Main functions


def Review_bot(r):
    print('Seaching for comments with !Review')

    for comment in r.subreddit(subreddits).comments(limit=25):
        reviewComments = open(r'C:\Users\root\Desktop\Projects\Review Bot\Review_comments.txt', 'r')
        if comment.body.startswith('!Review') and comment.id not in reviewComments.read():
            reviewComments.close()
            movie_request = str(comment.body)
            movie_request = movie_request.replace('!Review ', '')
            movie_request = movie_request.replace('!review ', '')
            # -------------------------------------------------IMDb---------------------------------------------------------- #
            imdb_search = ia.search_movie(movie_request)
            imdb_result = imdb_search[0]
            ia.update(imdb_result)
            imdb_rating = imdb_result['rating']
            print('The IMDb Rating of ' + str(imdb_result) + ' is: ' + str(imdb_rating))
            # -------------------------------------------------IMDb---------------------------------------------------------- #
            # ---------------------------------------------Metacritics------------------------------------------------------- #
            movie_request = str(imdb_result).replace(' ', '-')
            movie_request = movie_request.lower()
            print(movie_request)
            Metascore = requests.get("https://api-marcalencc-metacritic-v1.p.mashape.com/movie/" + movie_request,
              headers={
                "X-Mashape-Key": key,
                "X-Mashape-Host": host
              }
            )

            Metascore = Metascore.json()
            Metascore = Metascore[0]

            movie = movie_request.capitalize()
            movie = movie_request.replace('-', ' ')
            Metacritic_Score = Metascore['Rating']['CriticRating']
            print('The Metacritic score for ' + movie + ' is: ' + str(Metacritic_Score))
            # ------------------------------------------------Metacritic----------------------------------------------------- #
            # ---------------------------------------------Rotten Tomatoes--------------------------------------------------- #
            result = RottenTomatoesClient.search(term=str(imdb_result), limit=1)
            RTscore = result['movies'][0]['meterScore']
            print('The Rotten Tomatoes score for' + str(imdb_result) + ' is: ' + str(RTscore))
            # ---------------------------------------------Rotten Tomtates--------------------------------------------------- #
            imdb_rating = imdb_rating * 10
            average = (imdb_rating + Metacritic_Score + RTscore)/3
            # -------------------------------------------------Reply--------------------------------------------------------- #
            replystring = '''
The IMDb rating for {0} is: {1}/100

The Metacritc rating for {0} is: {2}/100

The Rotten Tomatoes rating for {0} is: {3}/100

The Average rating for {0} is: {4}/100
            '''.format(str(imdb_result), str(int(imdb_rating)), str(int(Metacritic_Score)), str(int(RTscore)), str(int(average)))
            comment.reply(replystring)
            # -------------------------------------------------Reply--------------------------------------------------------- #
            print('Comment Id is ' + comment.id)
            print('Noting Comment Id')
            Review_Comments = open(r'C:\Users\root\Desktop\Projects\Review Bot\Review_comments.txt', 'a')
            Review_Comments.write(comment.id)
            Review_Comments.write('\n')
            Review_Comments.close()

            time.sleep(10)


r = bot_login()

while True:
    Review_bot(r)
