import json
import requests
from pprint import pprint

access_token = 'CAACEdEose0cBANSRdUQQs2qAICytY2rc4EYnK79AvTjX82PI2gLZC1eVR0kMIppGaKE5GjKSTGOFceHzoCYNBf3j1VjstgfeCmGJ85ZBFogsPfeSZB5CtALInYaZBxtQNsOTp5YcjYKTh72ZC9boBg2bgwd2rdaNPLrsWzTpShmn99J3UEl5uscTxFBynwWP0c3XG0t9OZChSaGReVNA3nZBgZAjgj2UFgMZD'

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

url = 'https://graph.facebook.com/me/friends?fields=name,likes.fields(name,category),music.fields(name,category),movies.fields(name,category)' + access_str

r = requests.get(url)
raw_data = []
count = 0

while True:
    r = requests.get(url)
    raw_data.insert(count, r.json())
    pprint(raw_data[count])
    try:
        next_url = raw_data[count]['paging']['next'].encode('utf-8')
    except:
        break
    count += 1
    url = next_url

pprint(raw_data)

for dat in raw_data[0]['data']:
    pprint(dat)
    likes_list = []
    likes_cat_list = []
    name = dat['name']
    try:
        for like in dat['likes']['data']:
            likes_list.append(like['name'])
            likes_cat_list.append(like['category'])
        print name
        print likes_list
    except:
        pass
'''
        for like in dat['data']:
                print 'id ' + like['id']
                friends_likes.append(like['name'])
                friends_likes_cat.append(like['category'])
'''
