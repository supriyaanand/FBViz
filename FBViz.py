import json
import requests
from pprint import pprint

access_token = 'CAACEdEose0cBAG5ceGyZCaoNJYqdrGi64LmVv1rlmRfkqrOHkwJocZActqnZBzapLzYEuaKJ6Ein5Gxaes2UlkAFkgXIV0iv2NZC7MSp3rwiLB0ZC3LE4rARQVZA0zDor3kJvycQ6FHAIWStpAlJRWwltghblARqG4UDsPuvdcS5bGlffHCiOpJNc6GLN44IxyqX0XTZAoKZBFzPVZBuYRowNiKLTjw3P9nEZD'

access_str = '&access_token=' + access_token
# r = requests.get('https://graph.facebook.com/me/friends?fields=name,id,likes.fields(id,name,category)'+access_str)
'''
count = 0
raw_data = []
url = 'https://graph.facebook.com/me/likes?fields(id,name,category)' + access_str
while True:
    r = requests.get(url)
    raw_data.insert(count, r.json())
    try:
        next_url = raw_data[count]['paging']['next'].encode('utf-8')
    except:
        break
    count += 1
    url = next_url

my_likes_cats = []
my_likes = []
for dat in raw_data:
    #pprint(dat)
    for like in dat['data']:
        my_likes.append(like['name'])
        my_likes_cats.append(like['category'])

print my_likes_cats
print my_likes
'''
friends_likes = {}
friends_music = {}
friends_books = {}
friends_sports = {}
friends_movies = {}

url = 'https://graph.facebook.com/me/friends?fields=name,likes.fields(name,category),music.fields(name,category),movies.fields(name,category),books.fields(name,category),sports' + access_str

r = requests.get(url)
raw_data = []
count = 0

while True:
    r = requests.get(url)
    raw_data.insert(count, r.json())
    try:
        next_url = raw_data[count]['paging']['next'].encode('utf-8')
    except:
        break
    count += 1
    url = next_url


for info in raw_data:
    for dat in info['data']:
        likes_list = []
        likes_cat_list = []
        music_list = []
        movie_list = []
        books_list = []
        sport_list = []
        name = dat['name']
        try:
            for like in dat['likes']['data']:
                likes_list.append(like['name'])
                likes_cat_list.append(like['category'])
            friends_likes[name] = likes_list
        except:
            pass
        try:
            for music in dat['music']['data']:
                if music['category'] in ('Musician/band','Music'):
                    music_list.append(music['name'])
            friends_music[name] = music_list
        except:
            pass
        try:
            for movie in dat['movies']['data']:
                movie_list.append(movie['name'])
            friends_movies[name] = movie_list
        except:
            pass
        try:
            for book in dat['books']['data']:
                books_list.append(book['name'])
            friends_books[name] = books_list
        except:
            pass
        try:
            for sport in dat['sports']:
                sport_list.append(sport['name'])
            friends_sports[name] = sport_list
        except:
            pass

print "likes\n"
print friends_likes
print 'movies\n'
print friends_movies
print 'music\n'
print friends_music
print 'books\n'
print friends_books
print 'sports\n'
print friends_sports


