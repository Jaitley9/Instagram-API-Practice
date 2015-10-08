import requests
import json

def yourFans(userID, accessTokenID):
	"""
	in:
		userID - The Instagram user_id found from the API
		accessTokenID - Generated from authentication process. Used for access control on Instagram's end. 
	out:
		likers - A list of all usernames which liked every single picture in user feed
	"""
	userMediaRecent = requests.get("https://api.instagram.com/v1/users/" + userID +"/media/recent?access_token=" + accessTokenID).json()
	fans = {}
	while(userMediaRecent['pagination']):
		fans = makeFansDict(fans, userMediaRecent)
		userMediaRecent = requests.get(userMediaRecent['pagination']['next_url']).json()

	#Run it one last time because once you hit the last page, userMediaRecent['pagination'] will be false
	return makeFansDict(fans, userMediaRecent)

def makeFansDict(fans, userMediaRecent):
	"""
	in:
		fans - Dictionary in which the keys are the usernames of the  
	"""
	for i in range(0 , len(userMediaRecent['data'])):
		likes = requests.get("https://api.instagram.com/v1/media/" + userMediaRecent['data'][i]['id'] + "/likes/?access_token=" + accessTokenID).json()
		
		for j in range(0 , len(likes['data'])):
			userName  = likes['data'][j]['username']
			
			if(userName in fans):
				fans[userName] += 1
			else:
				fans[userName] = 1

	return fans

def yourLikes(userID, accessTokenID):
	userMediaLiked = requests.get("https://api.instagram.com/v1/users/" + userID +"/media/liked?access_token=" + accessTokenID).json()
	likes = {}
	
	while(userMediaLiked['pagination']):
		
		likes = makeLikesDict(likes, userMediaLiked)
		userMediaLiked = requests.get(userMediaLiked['pagination']['next_url']).json()
	
	#Run it one last time because once you hit the last page, userMediaLiked['pagination'] will be false
	return makeLikesDict(likes, userMediaLiked)

def makeLikesDict(likes, userMediaLiked):
	for i in range(0 , len(userMediaLiked['data'])):
		
		userName  = userMediaLiked['data'][i]['user']['username']
		
		if(userName in likes):
			likes[userName] += 1
		else:
			likes[userName] = 1

	return likes



#accessTokenID = null
#gotta get your own accesstoken
accessTokenID = "835826709.be662d5.2208942e2bce465a80eda436ca9e60a4"
#https://api.instagram.com/v1/users/self/media/liked?access_token=835826709.be662d5.2208942e2bce465a80eda436ca9e60a4

userID = "self"

#fans = yourFans(userID, accessTokenID)
liked = yourLikes(userID, accessTokenID)
#orderedFansList = sorted(fans, key = fans.get, reverse = True)
orderedLikedList  = sorted(liked, key = liked.get, reverse = True)
#Thanks to this http://stackoverflow.com/a/3418035 for sorting dict via value

likesList = open("userLikers.txt", 'w')
for idol in orderedLikedList:
	likesList.write(idol + ": " + repr(liked[idol]) + '\n')
	print(idol + ":" + repr(liked[idol]))
	

	

