import requests
import json

def getLikers(userID, accessTokenID):
	"""
	in:
		userID - The Instagram user_id found from the API
		accessTokenID - Generated from authentication process. Used for access control on Instagram's end. 
	out:
		likers - A list of all usernames which liked every single picture in user feed
	
	Use the Instagram API to get a list of all the usernames that liked each post.
	Will count the number of times a user shows up in the list for total likes by user.
	"""
	
	#GET JSON data for the first 33(max) pictures for the user
	userMediaData = requests.get("https://api.instagram.com/v1/users/" + userID +"/media/recent?access_token=" + accessTokenID + "&count=33").json()
	likers = []

	while(True):
		for i in range(1 , len(userMediaData['data'])):
			#This request.json() function starts indexing at 1 for some reason
			#Getting JSON data for all likes on each picture
			likes = requests.get("https://api.instagram.com/v1/media/" + userMediaData['data'][i]['id'] + "/likes/?access_token=" + accessTokenID).json()
			
			#Putting usernames of every single like on all pictures into likers.
			for j in range(1 , len(likes['data'])):
				likers.append(likes['data'][j]['username'])

		#Go to the next 33 posts. Instagram API makes it easy to tell when you've exhausted everything		
		if(userMediaData['pagination']):
			userMediaData = requests.get(userMediaData['pagination']['next_url']).json()
		else:
			return sorted(likers)

def genFans(likers):
	"""
	in:
		likers - List of usernames
	out: 
		fans - Dictionary of usernames and number of likes as values
	
	Generate a dictionary and increase count for each time they show up in the list.
	"""

	fans = {}

	for userName in likers:
		if(userName not in fans):
			fans[userName] = 0
		fans[userName] += 1

	return fans

#accessTokenID = "" You'll need to generate your own
userID = "self"

likers = getLikers(userID, accessTokenID)
fans = genFans(likers)
orderedFansList = sorted(fans, key = fans.get, reverse = True)
#Thanks to this http://stackoverflow.com/a/3418035 for sorting dict via value

for fan in orderedFansList:
	print(fan + ":" + repr(fans[fan]))
	

	

