import requests, json, tweepy, io, random
from urllib.request import urlopen
from credentials import *
from tweepy import Stream

#Search the API using title as a keyword
#Filter through results to display Turku City Library results only

def findbook(book):
	FINNA_API_SEARCH = 'https://api.finna.fi/v1/search'
	fields = ['title', 'buildings']
	filters = ['building:1/Vaski/1/']
	params = {'filter[]': filters,'lookfor':book, 'type':'Title','lng':'en-gb','field[]':fields}
	req = requests.get(FINNA_API_SEARCH, params=params)
	response = req.json()
	resultcount = response['resultCount']
	if(resultcount == 0):
		answer = "Your tweet didn't match any result in the Finna Library database"
	else:
		records = response['records']
		final_result = False
		for item in records:
			if(item['title'].lower() != book.lower()):
				answer = "This book is unavailable"
			if(item['title'].lower() == book.lower()):
				result = item['buildings']
				for dic in result:
					for key in dic:
						if(dic[key] == 'Turku City Library'):
							answer = "This book is available at Turku City Library"
							final_result = True
			break
		if final_result == False:
			answer = "Unfortunately, this book is currently unavailable"
	return answer 


#AWS Lambda function handler invoking your script goes here
#...

#Respond to tweets
mentions = api.mentions_timeline()
for mention in mentions:
	mention_tweet = mention.text
	updated_tweet = mention_tweet.split()
	updated_tweet.pop(0) #Get rid of the @username
	title_tweet = ' '.join(updated_tweet) #Convert back to string
	user = mention.author.screen_name
	reply = "@%s " % (user) + findbook(title_tweet)
	print(reply)
	mention = api.update_status(reply, mention.id)