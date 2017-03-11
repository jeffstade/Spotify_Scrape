import spotipy
sp = spotipy.Spotify()
import threading
exitFlag = 0
import timeit

seed_artist_uris = {'spotify:artist:7fSnislKgW9Mz0YIqWQmGt':False}
total_seen = 0

example_dictionary = {}
for i in range(1,1000):
	example_dictionary[i] = i+1

currentPosition = 0

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

'''
data = sp.artist_related_artists('spotify:artist:7fSnislKgW9Mz0YIqWQmGt') #SAN FERMIN
sp.artist_related_artists('spotify:artist:7fSnislKgW9Mz0YIqWQmGt')
'''