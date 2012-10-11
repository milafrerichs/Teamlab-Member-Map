import urllib
import json
import httplib

username = "YURUSERNAME"
password = "YOURPASSWORD"
url = "http://YOURPROJECT.teamlab.com/api/1.0/"
yahooKey = "YOURYAHOOKEY"
yahooUrl = "http://where.yahooapis.com/geocode"
def getToken():
	params = urllib.urlencode({'userName':username,'password':password})
	authenticationUrl = url+"authentication.json"
	tokenJsonFile = urllib.urlopen(authenticationUrl,params)
	tokenJson = tokenJsonFile.read()
	tokenObj = json.loads(tokenJson)
	return tokenObj['response']['token']

def getPeople(token):
	headers = {"Authorization": token}
	peopleUrl = "zentrumd64.teamlab.com"
	conn = httplib.HTTPConnection(peopleUrl)
	conn.request("GET", "/api/1.0/people.json", "", headers)
	response = conn.getresponse()
	peopleJson = response.read()
	conn.close()
	peopleObj = json.loads(peopleJson)
	return peopleObj["response"]

def parsePeople(people):
	peopleCities = []
	for person in people:
		if "location" in person:
			if person["location"] != "":
				peopleCities.append({"id":person["id"],"location":person["location"]})
	return peopleCities

def removeAndCountDuplicates(peopleCities):
	cities = {}
	for city in peopleCities:
		if city["location"] in cities:
		    cities[city["location"]] = cities[city["location"]]+1
		    peopleCities.remove(city)
		else:
		    cities[city["location"]] = 1
	for city in peopleCities:		
		if city["location"] in cities:
			city["mitglieder"] = cities[city["location"]]
		if "mitglieder" in city:
			city["mitglieder"] = cities[city["location"]]
		else:
			city["mitglieder"] = 1
			 
	return peopleCities

def geoCodePeople(peopleCities):
	peopleData = []
	for cities in peopleCities:
		cityDecode = cities["location"].encode('utf-8')
		city = cityDecode+",Germany"
		params = urllib.urlencode({'q':city,'locale':'de_DE','flags':'J','appid':yahooKey})
		latLngFile = urllib.urlopen(yahooUrl+"?%s" % params)
		latLngJson = latLngFile.read()
		latLngObj = json.loads(latLngJson)
		if "Results" in latLngObj["ResultSet"]:
			peopleData.append({"id":cities["id"],"city":cities["location"],"mitglieder":cities["mitglieder"],"location":{"lat":latLngObj["ResultSet"]["Results"][0]["latitude"],"lng":latLngObj["ResultSet"]["Results"][0]["longitude"]}})
	return peopleData	

token = getToken()
people = getPeople(token)	
peopleCities = parsePeople(people)
peopleCities = removeAndCountDuplicates(peopleCities)
peopleData = geoCodePeople(peopleCities)
f = open('js/data.json', 'w')
f.write(json.dumps(peopleData))
f.truncate()
f.close()