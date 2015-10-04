import requests
import json

def getLikers(userID, accessTokenID):
	"""
	in:
		userID - The Instagram user_id found from the API
		accessTokenID - Generated from authentication process. Used for access control on Instagram's end. 
	out:
		likers - A list of all usernames which liked every single picture in user feed
	"""
	userMediaData = requests.get("https://api.instagram.com/v1/users/" + userID +"/media/recent?access_token=" + accessTokenID).json()
	fans = {}
	while(userMediaData['pagination']):
		fans = getFans(fans, userMediaData)
		userMediaData = requests.get(userMediaData['pagination']['next_url']).json()

	#Run it one last time because once you hit the last page, userMediaData['pagination'] will be false
	return getFans(fans, userMediaData)

def getFans(fans, userMediaData):
	"""
	in:
		fans - Dictionary in which the keys are the usernames of the  
	"""
	for i in range(0 , len(userMediaData['data'])):
		likes = requests.get("https://api.instagram.com/v1/media/" + userMediaData['data'][i]['id'] + "/likes/?access_token=" + accessTokenID).json()
		
		for j in range(0 , len(likes['data'])):
			userName  = likes['data'][j]['username']
			
			if(userName in fans):
				fans[userName] += 1
			else:
				fans[userName] = 1

	return fans

accessTokenID = null
#gotta get your own accesstoken
userID = "self"

fans = getLikers(userID, accessTokenID)
orderedFansList = sorted(fans, key = fans.get, reverse = True)
#Thanks to this http://stackoverflow.com/a/3418035 for sorting dict via value

likesList = open("userLikers.txt", 'w')
for fan in orderedFansList:
	likesList.write(fan + ": " + repr(fans[fan]) + '\n')
	print(fan + ":" + repr(fans[fan]))
	

	

