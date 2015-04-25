from django.shortcuts import render
from django.http import HttpResponse
from event import *
import json, requests
from datetime import date
from utils import *
from firebase import firebase


def index(request, ll=None):
    if not ll:
        ll = '40.761662,-73.96805'

    #Get date from GET params
    date_str = request.GET.get("date")
    try:
        dd = get_datetz(date_str,ll)
    except Exception, e:
        return HttpResponse("error parsing date")
    foursquare = FoursquareEventFetcher.fetch(ll, dd)
    meetups = MeetupsEventFetcher.fetch(ll,dd)
    songkick = SongkickEventFetcher.fetch(ll, dd)
    eventbrite = EventbriteEventFetcher.fetch(ll,dd)
    all_events = [foursquare, meetups, songkick, eventbrite]
    json_all = json.dumps(all_events,default=lambda o: o.__dict__)
    return HttpResponse(json_all)

def fb_test(request):
    fb = firebase.FirebaseApplication('https://blinding-torch-1320.firebaseio.com/')
    new_user = 'asd'
    result = fb.post('/users', new_user)
    return HttpResponse(str(result))


def foursquare(request, ll=None):
    return HttpResponse(fetch(request, ll, FoursquareEventFetcher))

def meetups(request, ll=None):
   return HttpResponse(fetch(request, ll, MeetupsEventFetcher))

def songkick(request, ll=None):
    return HttpResponse(fetch(request, ll, SongkickEventFetcher))

def eventbrite(request, ll=None):
    return HttpResponse(fetch(request, ll, EventbriteEventFetcher))

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


def fetch(request, ll, fetcher):
    if not ll:
        ll = '40.761662,-73.96805'
    #Get date from GET params
    date_str = request.GET.get("date")
    try:
        dd = get_datetz(date_str,ll)
    except Exception, e:
        return HttpResponse("error parsing date")
    result = fetcher.fetch(ll,dd)
    json_all = json.dumps(result,default=lambda o: o.__dict__)
    return json_all



# ['preferredImage']['uri']

# ['title', 'officialUrl', 'shortDescription']

# ['showtimes']

# awtthn4hrz46u8utfkxsfm5k
# 6ba9xurnyeebzp9dx4kr6ds7
# f4e68drjqy93jk8djh9bsf8g
# khdmmearvwdhrskchcatf9vb