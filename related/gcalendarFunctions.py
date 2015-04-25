import httplib2
import sys
import time
import datetime
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets


def firstAuthenticatation():

    scope = 'https://www.googleapis.com/auth/calendar'
    flow = flow_from_clientsecrets('client_secret.json', scope=scope)

    storage = Storage('credentials.dat')
    credentials = storage.get()

    class fakeargparse(object):  # fake argparse.Namespace
        noauth_local_webserver = True
        logging_level = "ERROR"
    flags = fakeargparse()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, flags)




def createACalendar(myUserId):
    import os
    print(os.getcwd() + "\n")
    scope = 'https://www.googleapis.com/auth/calendar'
    flow = flow_from_clientsecrets('related/client_secret.json', scope=scope)

    storage = Storage('credentials.dat')
    credentials = storage.get()

    class fakeargparse(object):  # fake argparse.Namespace
        noauth_local_webserver = True
        logging_level = "ERROR"
    flags = fakeargparse()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, flags)

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)

    calendar = { 'summary': 'What to do!', 'timeZone': 'America/New_York' }
    userId = myUserId
    created_calendar = service.calendars().insert(body=calendar).execute()
    import psycopg2
    con = psycopg2.connect("postgres://stidzrltcswslr:dF-4xn841hPh9MRRTzLpbWNgAf@ec2-23-23-81-189.compute-1.amazonaws.com:5432/d7bs3h94l5spv1");
    cur = con.cursor()
     
    cur.execute("insert into calendarDetails(userId,calendarId) values(%s, %s)",(userId,created_calendar['id']))
    con.commit()
    cur.close()
    con.close()    
    
    rule = { 'scope': { 'type': 'default', 'value': '',},'role': 'reader' }
    created_rule = service.acl().insert(calendarId=created_calendar['id'], body=rule).execute()

    #print created_rule['id']

    print created_calendar['id']
    return created_calendar['id']


def createAnEvent(desc,startDate,endDate,location,myCalendarId):

    scope = 'https://www.googleapis.com/auth/calendar'
    flow = flow_from_clientsecrets('client_secret.json', scope=scope)
    storage = Storage('credentials.dat')
    credentials = storage.get()
    class fakeargparse(object):  # fake argparse.Namespace
        noauth_local_webserver = True
        logging_level = "ERROR"
    flags = fakeargparse()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, flags)

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)

    event = { 'summary': 'Appointment','sendNotifications':True,
 
 'location': 'Somewhere',
  'start': {
    'dateTime': '2015-04-24T10:00:00.000-07:00'
  },
  'end': {
    'dateTime': '2015-04-24T10:25:00.000-07:00'
  },
 
}

    #myCalendarId = rg64sccbfcg3mue8j7dhd1vnl4@group.calendar.google.com
    created_event = service.events().insert(calendarId=myCalendarId, body=event).execute()

    print created_event['id']
    return created_event['id']


def deleteAnEvent(eventId,calendarId):
    scope = 'https://www.googleapis.com/auth/calendar'
    flow = flow_from_clientsecrets('client_secret.json', scope=scope)
    storage = Storage('credentials.dat')
    credentials = storage.get()
    class fakeargparse(object):  # fake argparse.Namespace
        noauth_local_webserver = True
        logging_level = "ERROR"
    flags = fakeargparse()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, flags)

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)
    service.events().delete(calendarId='rg64sccbfcg3mue8j7dhd1vnl4@group.calendar.google.com', eventId='d3hlf8k2n1dv30m4q02l84gcnc').execute()
    return True
    
    
    




