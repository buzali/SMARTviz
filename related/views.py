from django.shortcuts import render
from django.http import HttpResponse
from facebookTwitterInsta import *


def facebook(request,searchQuery):
    print "facebook"
    print searchQuery
    resp = searchOnFacebook(searchQuery)
    return HttpResponse(resp)

def twitter(request,searchQuery):
    print "twitter"
    twitter = setupTwitter()
    resp = searchOnTwitter(twitter,searchQuery)
    return HttpResponse(resp)

def instagram(request,searchQuery):
    print "instagram"
    resp = searchInsta2(searchQuery)
    return HttpResponse(resp)

def instaloco(request,lat,lng):
    print "instaloco"
    resp = searchInstagram(lat,lng)    
    return HttpResponse(resp)


def places(request,lat,lng,typey,searchTerm=""):
    print "places"
    resp = findPlaces(lat,lng,typey,searchTerm)
    return HttpResponse(resp)



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
             resp = searchOnTwitter(twitter,searchQuery)
        elif relatedName == "instagram":
             searchQuery = pathy[3]
             resp = searchInsta2(searchQuery)
        elif relatedName == "instaloco":
             lat =  pathy[3]
             lng =  pathy[4]
             print lat
             print lng
             resp = searchInstagram(lat,lng)    
        elif relatedName == "places":
             a= "asd" 
             lat =  pathy[3]
             lng =  pathy[4]
             typey = pathy[5]
             searchTerm = pathy[6]
             if not searchTerm:
                 searchTerm = ""
             resp = findPlaces(lat,lng,typey,searchTerm)


        
        return HttpResponse(resp)