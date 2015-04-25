
import foursquare
import sys
import logging
from _creds import *
import json
import logging
from eventbrite import Eventbrite
from meetup import Meetup
from datetime import date, datetime, timedelta
from songkick import Songkick
from dateutil.tz import *
import dateutil
import time, pytz

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
        photo = obj.get('photos')
        super(FoursquareEvent, self).__init__(name, lat,lng, url, photo)
        self.type = 'Foursquare'
        self.address = '\n'.join(obj['location']['formattedAddress'])
        self.description = self.address

class FoursquareEventFetcher(object):
    @classmethod
    def fetch(cls, loc, dd=None):
        if dd:
            utc_now = datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.utc)
            #If dd in future, return empty
            if dd > utc_now:
                return []
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
    def fetch(cls, loc, dd=None):
        lat = loc.split(',')[0]
        lng = loc.split(',')[1]
        eventbrite = Eventbrite(EVENTBRITE_TOKEN)
        # #lab coordinates
        # ll = '40.4428285,-79.9561175'
        # #bloomberg coordinates
        # ll = '40.761662,-73.96805'
        datef = '%Y-%m-%dT%H:%M:%SZ'

        #If no date, get today's in utc
        if not dd:
            est = pytz.timezone("US/Eastern")
            now = datetime.now()
            dd = est.localize(datetime(now.year, now.month, now.day, 0,0))

        if not dd.tzinfo:
            print "ERROR- Missing timezone"
            return []
        today_utc = dd.astimezone(tzutc())
        print today_utc.strftime(datef)
        print (today_utc + timedelta(1)).strftime(datef)

        data = {'location.latitude':lat,
                'location.longitude': lng,
                 'location.within': '10km',
                 'start_date.range_start':today_utc.strftime(datef),
                 'start_date.range_end':(today_utc + timedelta(1)).strftime(datef),
                 }

        events_api = eventbrite.event_search(**data)
        
        events_dict = []
        if events_api.get('events'):   
            events_dict = [{'lat': e['venue']['latitude'],
            'lng': e['venue']['longitude'],
            'name': e['name']['text'],
            'description': e.get('description'),
            'url': e['url'],
            'start': datetime.strptime(e['start']['local'], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d %H:%m"),
            'end': datetime.strptime(e['end']['local'], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d %H:%m"),
            } for e in events_api['events'] if e.get('venue')]
        else:
            #if error print api output
            print events_api
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

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    epoch = epoch.replace(tzinfo=pytz.utc)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return int(unix_time(dt) * 1000.0)

class MeetupsEventFetcher(object):
    @classmethod
    def fetch(cls, loc, dd=None):
        lat = loc.split(',')[0]
        lng = loc.split(',')[1]
        meet = Meetup(MEETUPS_KEY)
        # #lab coordinates
        # ll = '40.4428285,-79.9561175'
        # #bloomberg coordinates
        # ll = '40.761662,-73.96805'

        #If no date, get today's in utc
        if not dd:
            est = pytz.timezone("US/Eastern")
            now = datetime.now()
            dd = est.localize(datetime(now.year, now.month, now.day, 0,0))

        if not dd.tzinfo:
            print "ERROR- Missing timezone"
            return []

        day_utc = dd.astimezone(tzutc())
        day_ms = unix_time_millis(day_utc)
        print day_ms
        next_ms = unix_time_millis(day_utc+timedelta(1))
        print next_ms

        data = {
        'lat':lat,
        'lon':lng,
        'radius': '8',
        'time':'{0},{1}'.format(repr(day_ms),repr(next_ms)),
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
    def fetch(cls, loc, dd=None):
        if not dd:
            dd=datetime.today()
        #dd=datetime(dd.year, dd.month, dd.day, 0,0,0 , tzinfo=dd.tzinfo)
        #dd_utc = dd.astimezone(pytz.utc)
        lat = loc.split(',')[0]
        lng = loc.split(',')[1]
        sk = Songkick('vYtwu69WMoO13X3H')
        loc = '{0},{1}'.format(lat,lng)
        events_query = sk.events.query(location='geo:' + loc, per_page=10, min_date=dd.date(), max_date= dd.date())
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
