from django.shortcuts import render
from django.http import HttpResponse
from foursquareEvents import *
import json


def index(request, ll=None):
    if not ll:
    	ll = '40.761662,-73.96805'
    foursquare = FoursquareEventFetcher.fetch(ll)
    meetups = MeetupsEventFetcher.fetch(ll)
    all_events = []
    all_events = foursquare + meetups
    json_all = json.dumps(all_events,default=lambda o: o.__dict__)
    return HttpResponse(json_all)