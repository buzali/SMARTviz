from django.shortcuts import render
from django.http import HttpResponse
from facebookTwitterInsta import *

def index(request):
    if request.method == 'GET':
        twitter = setupTwitter()
        q = request.GET.get('q')
        if not q:
            q = "The Porch Pittsburgh"
        resp = searchOnTwitter(twitter,q)
        return HttpResponse(resp)