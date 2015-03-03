from django.shortcuts import render
from django.http import HttpResponse
from foursquareEvents import *
import json


def index(request, ll=None):
    if not ll:
    	ll = '40.761662,-73.96805'
    foursquare = FoursquareEventFetcher.fetch(ll)
    return HttpResponse(resp)