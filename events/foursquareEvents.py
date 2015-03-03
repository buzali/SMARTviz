
import foursquare
import sys
import logging
from _creds import *
import json
import logging


class Event(object):

    def __init__(self, name, location, url, photo):
        self.type = 'Generic'
        self.name = name
        self.location = location
        self.url = url
        self.photo = photo
    def __repr__(self):
        return "%s: %s" %(self.type, self.name)
    def __str__(self):
        return "%s: %s" %(self.type, self.name)
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class FoursquareEvent(Event):

    def __init__(self, obj):
        name = obj['name']
        location = "%s,%s" %(obj['location']['lat'],obj['location']['lng'])
        url = obj.get('shortUrl')
        photo = obj.get('photos')
        super(FoursquareEvent, self).__init__(name, location, url, photo) 
        self.type = 'Foursquare'

class FoursquareEventFetcher(object):
    @classmethod
    def fetch(cls, loc):
        loghandler = logging.StreamHandler(stream=sys.stdout)
        foursquare.log.addHandler(loghandler)
        foursquare.log.setLevel(logging.DEBUG)

        client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        #access_token = client.oauth.get_token('')
        client.set_access_token(ACCESS_TOKEN)
        # #lab coordinates
        # ll = '40.4428285,-79.9561175'
        # #bloomberg coordinates
        # ll = '40.761662,-73.96805'
        trending_venues = client.venues.trending(params={'ll': loc})['venues']
        venues =  [FoursquareEvent(venue) for venue in trending_venues]
        return json.dumps(venues,default=lambda o: o.__dict__)

# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Event):
#             return obj.to_json()

#         return json.JSONEncoder.default(self, obj)

# ll = '40.761662,-73.96805'
# #print json.dumps(FoursquareEventFetcher.fetch(ll),default=lambda o: o.__dict__)
