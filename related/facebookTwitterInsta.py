from twython import Twython
import urllib3
import sys
import json
import facebook
import urllib2
from instagram.client import InstagramAPI


def setupTwitter():
       APP_KEY = 'aVKRHSK6yJFBWORwT1wIr2BsY'
       APP_SECRET = 'fzopk8RfTyDL09PrRtqj1JmrB8KtZORmLsr5jEiuEihku9jH2o'
       OAUTH_TOKEN = '1905291752-1unojpGy8h5Sc02kDbFa3vQpxp7lVkKZ4du4BKD'
       OAUTH_TOKEN_SECRET = 'XjESafpNrnYQoOYlXRsKZJLVY89k3AZYNUmxu2FvMkPCt'
       client_args = { 'verify': False }
       twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET,client_args=client_args) 
       #print twitter
       return twitter

 
def getKey(row,fieldName1 , fieldName2 , fieldName3 ):
     try:
       
       #value = row["entities"]["media"]
       #return value

      
       if fieldName3:
            value = row[fieldName1][fieldName2][fieldName3]
       elif fieldName2:
            value = row[fieldName1][fieldName2]
       else:    
            value = row[fieldName1]

       return value
     except KeyError :
          print "Key Error"
          return None

def searchOnTwitter(twitter,searchQuery):
       urllib3.disable_warnings()
       a = twitter.search(q=searchQuery,count=100,result_type="recent")  
       coinnn =0
       jsonArray = []

       for row in a["statuses"]:

          for key, value in row.iteritems():
             af = ""
             data = {}
          try:
             tweetID = row["id"]
             userId = row["user"]["id"]
             screen_name = row["user"]["screen_name"]
             profileImage = row["user"]["profile_image_url"]
             url = "http://twitter.com/" + str(userId) + "/status/" + str(tweetID)
             description = row["text"]
             media = getKey(row,"entities","media",None)
             imageUrl = ""
             if media:
                 imageUrl = getKey(media[0],"media_url_https",None,None)
                 print imageUrl
             #imageUrl = getKey(media[0],"media_url_https")
             print url  
             #print media
             data['title'] = screen_name
             data['titleImage'] = profileImage
             data['description'] = description
             data['type'] = 'twitter'
             data['link'] = url
             data['photo'] = imageUrl
             jsonArray.append(data)

          except:
             print sys.exc_info()[0]             
          coinnn = coinnn + 1
       #print a
       #a = twitter.search(q="@Benton",count=100)
       #print a
       a = ""
       jsss = json.dumps(jsonArray, separators=(',',':'))
       #print jsss
       return jsss

def searchOnFacebook(searchQuery):
    jsonArray = []

    graph = facebook.GraphAPI("CAACEdEose0cBAIIf9HI516AOiqoKdiOCyAqMWnshcaGh5xaUQjmOgi124z2lX7AaCuujY5h3SfTNXUZA2DMot6VqrtrJYyZC9y2NUfL5pXd3JuKYB3ZCFB75vFI8ZCOupFZAZAuM3bsFJZBQuabXDA3aobi087jePQsI70jhSZCZArMxQ8mSXGHezy5fyDkesfFpqzGkxfXgFD104M3eKgS7VP91yiGp6rYWNXgWDZAZBxSWwZDZD")
    response = graph.request('search', args={'q': searchQuery, 'type': 'event'})
    datay = response["data"]
    data = {}
    coubt = 0
    for row in datay:
        
        try:
              eventName = getKey(row,"name",None,None)
              eventId = getKey(row,"id",None,None)
              eventDetails =   graph.request(eventId)  
              #print eventDetails
              data['title'] = eventName
              #data['titleImage'] = profileImage
              data['description'] = eventDetails["description"]
              data['type'] = 'facebook'
              data['link'] = "http://www.facebook.com/events/" + str(eventId)
              data['startTime'] = getKey(eventDetails,"start_time",None,None) 
              data['endTime'] = getKey(eventDetails,"end_time",None,None) 
              
              data['photo'] = ""
              jsonArray.append(data)
        except:
             print sys.exc_info()[0]    
    jsss = json.dumps(jsonArray, separators=(',',':'))
    #print jsss
    return jsss   

def searchInstagram(lat,lng):
     jsonArray = []

     api = InstagramAPI(client_id='69ae00c802504e0599277ed72265e221', client_secret='7a8bc6124d694a71b482593078999774')
     #media = api.media_search(lat="40.858844",lng="80")
     media = api.media_search(lat=lat,lng=lng)
     for row in media:
        data = {}
        data['title'] = row.location.name
        #data['titleImage'] = profileImage
        data['description'] = row.caption.text
        data['type'] = 'instagram'
        data['link'] = row.link
              
        data['photo'] = row.images["standard_resolution"].url
        jsonArray.append(data)
    
     jsss = json.dumps(jsonArray, separators=(',',':'))
     #print jsss
     return jsss 



def searchInsta2(searchQuery):
     jsonArray = []
     api = InstagramAPI(client_id='69ae00c802504e0599277ed72265e221', client_secret='7a8bc6124d694a71b482593078999774')
     media = api.tag_recent_media(tag_name=searchQuery)
     media = media[0]
     for row in media:
        print row
        data = {}
        data['title'] = row.caption.text
        #data['titleImage'] = profileImage
        data['description'] = row.caption.text
        data['type'] = 'instagram'
        data['link'] = row.link
              
        data['photo'] = row.images["standard_resolution"].url
        jsonArray.append(data)
    
     jsss = json.dumps(jsonArray, separators=(',',':'))
     #print jsss
     return jsss


def findPlaces(lat,longy,type,searchTerm):
      jsonArray = []
      strReq = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(lat)+","+ str(longy)  +"&radius=500&types="+type+"&name="+searchTerm  +"&key=AIzaSyB8vY8sGIn0Dgo2yL0ZV73FF7dUcHRoihY"
      places = urllib2.urlopen(strReq)
      arr = places.read()
      results = json.loads(arr)
      actualResults = results["results"]
      jsss = ""
      for row in actualResults:
          data = {}
          name = row["name"]
          lat = row["geometry"]["location"]["lat"]
          longy = row["geometry"]["location"]["lng"]
          openNow = getKey(row,"opening_hours","open_now",None)
          stry = str(name) + " " + str(lat) + " " + str(longy) + " " + str(openNow)
          #print stry
          data['name'] = name
          #data['titleImage'] = profileImage
          data['lat'] = lat
          data['lng'] = longy
          data['type'] = 'places'
          data['openNow'] = openNow
          jsonArray.append(data)
    
          jsss = json.dumps(jsonArray, separators=(',',':'))

      print jsss
      return jsss

     

#twitter = setupTwitter()
#searchOnTwitter(twitter,"The Porch Pittsburgh")
#searchOnFacebook("Soup Pittsburgh")
#searchInsta2()
#findPlaces(-33.8670522,151.1957362,"food","cruise")

