from django.shortcuts import render
from django.http import HttpResponse
from foursquareEvents import *
import json, requests
from datetime import date


def index(request, ll=None):
    if not ll:
        ll = '40.761662,-73.96805'
    foursquare = FoursquareEventFetcher.fetch(ll)
    meetups = MeetupsEventFetcher.fetch(ll)
    songkick = SongkickEventFetcher.fetch(ll)
    eventbrite = EventbriteEventFetcher.fetch(ll)
    all_events = [foursquare, meetups, songkick, eventbrite]
    json_all = json.dumps(all_events,default=lambda o: o.__dict__)
    return HttpResponse(json_all)

def foursquare(request, ll=None):
    if not ll:
        ll = '40.761662,-73.96805'
    foursquare = FoursquareEventFetcher.fetch(ll)
    json_all = json.dumps(foursquare,default=lambda o: o.__dict__)
    return HttpResponse(json_all)

def meetups(request, ll=None):
    if not ll:
        ll = '40.761662,-73.96805'
    meetups = MeetupsEventFetcher.fetch(ll)
    json_all = json.dumps(meetups,default=lambda o: o.__dict__)
    return HttpResponse(json_all)

def songkick(request, ll=None):
    if not ll:
        ll = '40.761662,-73.96805'
    songkick = SongkickEventFetcher.fetch(ll)
    json_all = json.dumps(songkick,default=lambda o: o.__dict__)
    return HttpResponse(json_all)

def eventbrite(request, ll=None):
    if not ll:
        ll = '40.761662,-73.96805'
    eventbrite = EventbriteEventFetcher.fetch(ll)
    json_all = json.dumps(eventbrite,default=lambda o: o.__dict__)
    return HttpResponse(json_all)

def showtimes(request, ll=None):
    if not ll:
        ll = '40.761662,-73.96805'
    lat = ll.split(',')[0]
    lng = ll.split(',')[1]
    tms_url = "http://data.tmsapi.com/v1.1/movies/showings"
    data = {
        'api_key': 'awtthn4hrz46u8utfkxsfm5k',
        'startDate': date.today().isoformat(),
        'lat': lat,
        'lng':lng,
        'api_key': 'awtthn4hrz46u8utfkxsfm5k',
    }
    r = requests.get(tms_url, params=data)
    if (r.text):
        return HttpResponse(r.json())
    return HttpResponse('')


# ['preferredImage']['uri']

# ['title', 'officialUrl', 'shortDescription']

# ['showtimes']

# awtthn4hrz46u8utfkxsfm5k
# 6ba9xurnyeebzp9dx4kr6ds7
# f4e68drjqy93jk8djh9bsf8g
# khdmmearvwdhrskchcatf9vb