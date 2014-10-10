import json
import requests
from pprint import pprint
import operator
import networkx as nx


class FBViz:
    def __init__(self, token):
        self.access_token = token
        self.access_str = 'access_token=' + self.access_token
        self.friends_likes = {}
        self.friends_music = {}
        self.friends_books = {}
        self.friends_sports = {}
        self.friends_movies = {}
        self.friend_dict = {}
        self.music_reco_from = ''
        self.movies_reco_from = ''
        self.books_reco_from = ''
        self.sport_reco_from = ''
        self.like_minded_friend = ''
        self.G = nx.MultiGraph()

    def get_user_friends_ids(self):
        raw_data = []
        url = 'https://graph.facebook.com/' + str(self.user_id) + '/friends?' + self.access_str
        print url
        r = requests.get(url)
        data = r.json()
        pprint(data)
        for friend in data['data']:
            self.friend_dict[friend['id']] = friend['name']


    def get_recommender(self, d):
        new_dict = {}
        for name, raw_list in d.items():
            new_dict[name] = len(raw_list)
        v = list(new_dict.values())
        k = list(new_dict.keys())
        return k[v.index(max(v))]


    def get_like_minded(self):
        max_similar_likes = 0
        like_minded_friend = ''
        for name, likes_list in self.friends_likes.items():
            num_similar_likes = len(list(set.intersection(set(self.user_likes), set(likes_list))))
            if num_similar_likes > max_similar_likes:
                max_similar_likes = num_similar_likes
                self.like_minded_friend = name


    def get_likes_by_id(self, id):
        count = 0
        raw_data = []
        url = 'https://graph.facebook.com/' + str(id) + '/likes?fields(id,name,category)&' + self.access_str
        print url
        while True:
            r = requests.get(url)
            pprint(r.json())
            raw_data.insert(count, r.json())
            try:
                next_url = raw_data[count]['paging']['next'].encode('utf-8')
            except:
                break
            count += 1
            url = next_url

        likes = []
        for dat in raw_data:
            pprint(dat)
            for like in dat['data']:
                likes.append(like['name'])

        return likes

    def get_interests_data(self, id):
        url = 'https://graph.facebook.com/' + str(
            id) + '/friends?fields=name,likes.fields(name,category),music.fields(name,category),movies.fields(name,category),books.fields(name,category),sports&' + self.access_str

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
                    for music in dat['music']['data']:
                        if music['category'] in ('Musician/band', 'Music'):
                            music_list.append(music['name'])
                    self.friends_music[name] = music_list
                except:
                    pass
                try:
                    for movie in dat['movies']['data']:
                        movie_list.append(movie['name'])
                    self.friends_movies[name] = movie_list
                except:
                    pass
                try:
                    for book in dat['books']['data']:
                        books_list.append(book['name'])
                    self.friends_books[name] = books_list
                except:
                    pass
                try:
                    for sport in dat['sports']:
                        sport_list.append(sport['name'])
                    self.friends_sports[name] = sport_list
                except:
                    pass

    def build_graph(self):
        self.node_list = [self.like_minded_friend, self.books_reco_from, self.movies_reco_from, self.music_reco_from,
                          self.sport_reco_from, 'Read a book? Ask me', 'Watch a movie? Ask me', 'Sing along with',
                          'Sports arena?', 'Similar tastes?']
        #self.node_list.append(self.friends_likes[self.like_minded_friend][:10])
        self.node_list.append(self.user_name)

        self.G.add_nodes_from(self.node_list)

        self.G.add_edge(self.user_name, 'Similar tastes?', color = 'purple')
        self.G.add_edge('Similar tastes?', self.like_minded_friend,color = 'purple' )

        self.G.add_edge(self.user_name, 'Read a book? Ask me', color = 'blue')
        self.G.add_edge('Read a book? Ask me', self.books_reco_from, color = 'blue')

        self.G.add_edge(self.user_name, 'Watch a movie? Ask me', color = 'green')
        self.G.add_edge('Watch a movie? Ask me', self.movies_reco_from, color = 'green')

        self.G.add_edge(self.user_name, 'Sing along with', color = 'yellow')
        self.G.add_edge('Sing along with', self.music_reco_from, color = 'yellow')

        self.G.add_edge(self.user_name, 'Sports arena?', color = 'orange')
        self.G.add_edge('Sports arena?', self.sport_reco_from, color = 'orange')

        self.G.add_edge(self.user_name, 'Pages you might like!', color = 'red')
        for node in self.friends_likes[self.like_minded_friend][:10]:
            self.G.add_edge('Pages you might like', node, color = 'red')


        nx.write_graphml(self.G, 'FBViz' + ".graphml")


if __name__ == '__main__':

    FB_obj = FBViz(
        'CAACEdEose0cBAPdJzxeeopF24ZB9DrBlubT6zxEh82FcdOzaK5fRliUdOnG26wc1ayZAAZARTZCt62pX3zAGRZCg4am1vznRXaeOWO7fl5aOOQNhY67RteBdnf6QV1qeF0n9fqMAxK8efRaOoAeC2MALva7kQNtIeOwzXAdaQK0W4ZCZCOOwZBTL6dIGLqv7bm34QUTxdON7F6WjGBk7MMv54ZBgtePjBXokZD')
    FB_obj.user_id = 834289639943985
    FB_obj.user_name = 'Supriya Anand'
    FB_obj.user_likes = FB_obj.get_likes_by_id(FB_obj.user_id)
    FB_obj.get_user_friends_ids()
    '''
        Collect connections data for books,music,movies and sports choices
    '''
    for id, name in FB_obj.friend_dict.items():
        likes = FB_obj.get_likes_by_id(id)
        FB_obj.friends_likes[name] = likes
    FB_obj.get_interests_data(FB_obj.user_id)

    '''
        Get recommenders for each category by highest number of pages followed in the relevant category
    '''
    FB_obj.music_reco_from = FB_obj.get_recommender(FB_obj.friends_music)
    FB_obj.movies_reco_from = FB_obj.get_recommender(FB_obj.friends_movies)
    FB_obj.books_reco_from = FB_obj.get_recommender(FB_obj.friends_books)
    FB_obj.sport_reco_from = FB_obj.get_recommender(FB_obj.friends_sports)

    '''
        Get possible pages to follow from like minded friends
    '''
    FB_obj.get_like_minded()
    FB_obj.build_graph()

