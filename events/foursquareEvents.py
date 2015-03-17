
import foursquare
import sys
import logging
from _creds import *
import json
import logging
from eventbrite import Eventbrite
from meetup import Meetup
from datetime import date, datetime
from songkick import Songkick
import time

class Event(object):

    def __init__(self, name, lat, lng, url, photo):
        self.type = 'Generic'
        self.name = name
        self.latitude = lat
        self.longitude = lng
        self.url = url
        self.photo = photo
    def __repr__(self):
        return u"{0}: {1}".format(self.type, self.name)
    def __unicode__(self):
        return u"{0}: {1}".format(self.type, self.name)
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class FoursquareEvent(Event):

    def __init__(self, obj):
        name = obj['name']
        lat = obj['location']['lat']
        lng = obj['location']['lng']
        url = obj.get('url')
        print url
        photo = obj.get('photos')
        super(FoursquareEvent, self).__init__(name, lat,lng, url, photo) 
        self.type = 'Foursquare'
        self.address = '\n'.join(obj['location']['formattedAddress'])
        self.description = self.address

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
        return venues
        # return json.dumps(venues,default=lambda o: o.__dict__)

class EventbriteEvent(Event):

    def __init__(self, obj):
        super(EventbriteEvent, self).__init__(obj.get('name'), obj.get('lat'), obj.get('lng'), obj.get('url'), None) 
        self.type = 'Eventbrite'
        self.description = "{0} - {1}".format(obj['start'], obj['end'])


class EventbriteEventFetcher(object):
    @classmethod
    def fetch(cls, loc):
        lat = loc.split(',')[0]
        lng = loc.split(',')[1]
        eventbrite = Eventbrite(EVENTBRITE_TOKEN)
        # #lab coordinates
        # ll = '40.4428285,-79.9561175'
        # #bloomberg coordinates
        # ll = '40.761662,-73.96805'
        data = {'location.latitude':lat,
                'location.longitude': lng,
                 'location.within': '10km',
                 'start_date.keyword':'today'}

        events_api = eventbrite.event_search(**data)

        events_dict = [{'lat': e['venue']['latitude'],
        'lng': e['venue']['longitude'],
        'name': e['name']['text'],
        'description': e.get('description'),
        'url': e['url'],
        'start': datetime.strptime(e['start']['local'], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d %H:%m"),
        'end': datetime.strptime(e['end']['local'], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d %H:%m"),
        } for e in events_api['events'] if e.get('venue')]
        events = [EventbriteEvent(e) for e in events_dict]
        return events

class MeetupsEvent(Event):

    def __init__(self, obj):
        name = obj['name']
        lat=lng = None
        lat = obj['venue']['lat']
        lng = obj['venue']['lon']
        self.address = u"{0}, {1}".format(obj['venue']['address_1'],obj['venue']['city'])
        self.description = self.address
        url = obj.get('event_url')
        photo = obj.get('photo_url')
        super(MeetupsEvent, self).__init__(name, lat, lng, url, photo) 
        # self.description = obj.get('description')
        self.time = obj.get('time')

        self.type = 'Meetups'

class MeetupsEventFetcher(object):
    @classmethod
    def fetch(cls, loc):
        lat = loc.split(',')[0]
        lng = loc.split(',')[1]
        meet = Meetup(MEETUPS_KEY)
        # #lab coordinates
        # ll = '40.4428285,-79.9561175'
        # #bloomberg coordinates
        # ll = '40.761662,-73.96805'
        data = {
        'lat':lat,
        'lon':lng,
        'radius': '8',
        'time':'0d,1d',
        'only':'event_url,name,photo_url,distance,description,venue,time,why,simple_html_description',
        }
        meetups = meet._fetch('/2/open_events', **data)
        
        events_json = meetups['results']
        events =  [MeetupsEvent(event) for event in events_json if event.get('venue')]
        return events
        # return json.dumps(events,default=lambda o: o.__dict__)

class SongkickEvent(Event):

    def __init__(self, obj):
        super(SongkickEvent, self).__init__(obj.get('name','').split('at')[0], obj.get('lat'), obj.get('lng'), obj.get('url'), None) 
        self.type = 'Songkick'
        self.venue = obj['venue']
        time_str = ''
        if obj.get('time'):
            time_str = time.strftime('%H:%M', obj.get('time'))
            venueLoc_str = obj.get('name','').split('at')[1].split('(')[0].strip()
        else:
            venueLoc_str = obj.get('name')
        self.description = u"{0} - {1}".format(venueLoc_str, time_str)

class SongkickEventFetcher(object):
    @classmethod
    def fetch(cls, loc):
        lat = loc.split(',')[0]
        lng = loc.split(',')[1]
        sk = Songkick('vYtwu69WMoO13X3H')
        loc = '{0},{1}'.format(lat,lng)
        events_query = sk.events.query(location='geo:' + loc, per_page=10, min_date=date.today(), max_date=date.today())
        try:
            events_dict = [{'lat': str(event.location.latitude),
                'lng':event.location.longitude,
                'name': event.display_name,
                'url': event.uri,
                'venue': event.venue.display_name,
                'time': event.event_start.time
                } for event in events_query]
            
            events = [SongkickEvent(e) for e in events_dict]
        except Exception, e:
            raise e
            
        return events
        # return json.dumps(events,default=lambda o: o.__dict__)






# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Event):
#             return obj.to_json()

#         return json.JSONEncoder.default(self, obj)

