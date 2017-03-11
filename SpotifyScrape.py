
import spotipy
sp = spotipy.Spotify()
from threading import Thread
import csv
import sys
csv.field_size_limit(sys.maxsize)
reload(sys)
sys.setdefaultencoding('utf-8')

#San Fermin: spotify:artist:7fSnislKgW9Mz0YIqWQmGt
#Ed Sheerhan: spotify:artist:6eUKZXaKkcviH0Ku9w2n3V


seed_artist_uris = {'spotify:artist:6eUKZXaKkcviH0Ku9w2n3V': False}
total_seen = 0
artist_table = {}
global_popularity = []


artists = {}
genres  = {}
artist_related = {}
artist_genre   = {}

popularity_minimum = 10

def process_id(id):
	seed_artist_uris[id] = True
	data = sp.artist_related_artists(id)
	related_artists_count = len(data['artists'])
	for related_artist in data['artists']:
		related_artist_i = 1
		name = related_artist['name']
		uri = related_artist['uri']
		popularity = related_artist['popularity']
		global_popularity.append(popularity)
		# Check against popularity minimum
		if popularity >= popularity_minimum:
			if uri not in artists:
				# Populate Artists Table
				ad = sp.artist(uri)
				genres_count = len(ad['genres'])
				artists[uri] = {'uri': uri, 'name': ad['name'], 'popularity': ad['popularity'], 'image_url': ad['images'][0]['url'], 'followers': ad['followers']['total'], 'type': ad['type'], 'genre_count': genres_count, 'related_artists_count': related_artists_count }
				# Populate Genres table
				genre_i = 1
				for g in ad['genres']:
					if g not in genres:
						genres[g] = genre_i
						genre_i += 1
					# Populate Genres<>Artists table
					artist_genre[uri + '_' + g] = {'uri': uri, 'genre_id': genres[g], 'genre_order': genre_i}
					genre_i += 1
		# Populat Artists<>Artists table
		artist_related[id + uri] = {'uri': id, 'related_uri': uri, 'related_order': related_artist_i}
		if(uri) not in seed_artist_uris:
			seed_artist_uris[uri] = False
		related_artist_i += 1

def process_id_range(id_range, store=None):
    if store is None:
        store = {}
    for id in id_range:
        store[id] = process_id(id)
    return store

def threaded_data_request(nthreads, id_range):
    store = {}
    threads = []
    for i in range(nthreads):
        ids = id_range[i::nthreads]
        t = Thread(target=process_id_range, args=(ids,store))
        threads.append(t)    
    # start the threads
    [ t.start() for t in threads ]
    # wait for the threads to finish
    [ t.join() for t in threads ]
    return store

def collect_keys_false(dictionary):
	new_list = []
	for k, v in dictionary.iteritems():
	    if v == False:
	    	new_list.append(k)
	return new_list

threaded_data_request(1, collect_keys_false(seed_artist_uris)[:20])

'''
import csv
import io
#f = io.open('artists.csv', 'wb', encoding='utf8')
with io.open('artists.csv', 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    for k, v in artists.items():
       writer.writerow([v['uri'],v['name'],v['popularity']])


def create_csv_from_dict(filename, dict_obj, key_list, headers=False):
	f = open(filename, 'wb')
	wr = csv.writer(f, quoting=csv.QUOTE_ALL)
	if (headers):
		wr.writerow([h for h in headers])
	else:
		wr.writerow([k for k in key_list])
	for d in dict_obj:
		wr.writerow([dict_obj[d][k] for k in key_list])
	f.close()

create_csv_from_dict('artists.csv', artists, ['popularity', 'name'])

class SpotifyScrape(threading.Thread):
    def __init__(self, threadID, name, counter, example_dictionary):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.example = example_dictionary

    def run(self):
        print "Starting " + self.name
        example_thread(self.name, example_dictionary)
        print "Exiting " + self.name
        sel

def example_thread(threadName, example):
	keys = example_dictionary.keys()
	global currentPosition
	while currentPosition < len(keys):
		for k in keys:
			#print(threadName, example_dictionary[keys[currentPosition]])
			print(currentPosition)
			currentPosition += 1
	if currentPosition == len(keys):
		exitFlag = 1

def iterate_on_dictionary(uri_dict):
	for uri in uri_dict.keys():
		data = sp.artist_related_artists(uri)
		for artist in data['artists']:
			name = artist['name']
			uri = artist['uri']
			if(uri) not in uri_dict:
				uri_dict[uri] = False
		uri_dict[uri] = True
		global total_seen
		total_seen = total_seen+1

def runthreads():
	global currentPosition
	currentPosition = 0
	thread1 = SpotifyScrape(1, "Thread1", 1, example_dictionary)
#	thread2 = SpotifyScrape(2, "Thread2", 1, example_dictionary)
	thread1.start()
#	thread2.start()
	if exitFlag:
		thread1.exit()

timeit.timeit(runthreads, number=100)

#iterate_on_dictionary(seed_artist_uris)
#print(len(seed_artist_uris), total_seen)

data = sp.artist_related_artists('spotify:artist:7fSnislKgW9Mz0YIqWQmGt') #SAN FERMIN
sp.artist_related_artists('spotify:artist:7fSnislKgW9Mz0YIqWQmGt')
'''