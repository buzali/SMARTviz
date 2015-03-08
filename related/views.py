from django.shortcuts import render
from django.http import HttpResponse
from facebookTwitterInsta import *

def index(request,ll=None):
    if request.method == 'GET':
    	namepath = request.path
    	print "aspp"
    	print request.GET.get('q')
        pathy = namepath.split("/")
        print "mouse"
        print pathy[2] 
        relatedName = pathy[2]
        if relatedName == "facebook":
             searchQuery = pathy[3]
             resp = searchOnFacebook(searchQuery)
        elif relatedName == "twitter":
             twitter = setupTwitter()
             searchQuery = pathy[3]
             #q = request.GET.get('q')
             if not searchQuery:
                 searchQuery = "The Porch Pittsburgh"
             resp = searchOnTwitter(twitter,q)
        elif relatedName == "instagram":
             a= "asd"
        elif relatedName == "places":
             a= "asd" 


        
        return HttpResponse(resp)