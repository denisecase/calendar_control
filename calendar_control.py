import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import csv

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'

"""
# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/google-apps/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.
"""
# enter semester start as integers
startyear = 2019
startmonth = 1
startday = 14

wks_in_sem = 16
color_id = 8

email_invite = "dcase@nwmissouri.edu"
name_invite = "Denise Case (NWMSU)"

csvfile = 'one.csv'

showcolors = False
addRepeating = False
addIndividual = True

                                    
sem_start =  datetime.date(startyear, startmonth, startday)                        

def get_credentials():
    """
    # Gets valid user credentials from storage.
    # If nothing has been stored, or if the stored credentials are invalid,
    # the OAuth2 flow is completed to obtain the new credentials.
    # 
    #  Returns:
    #  Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print( 'Storing credentials to ' + credential_path)
    return credentials

def main():
    """
    Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service object and outputs a list of the next
    5 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    """
    # test access by getting current events 
    """
    print ('Getting the upcoming 5 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print ('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print ( start + "   " + event['summary'] )
        
    colors = service.colors().get().execute()
   
    if showcolors:
        # Print available calendarListEntry colors for reference.
        for id, color in colors['calendar'].items(): #python 3
            print ('colorId: %s' % id)
            print ('  Background: %s' % color['background'])
            print ('  Foreground: %s' % color['foreground'])
            
        # Print available event colors for reference.
        for id, color in colors['event'].items():
            print ('colorId: %s' % id)
            print ('  Background: %s' % color['background'])
            print ('  Foreground: %s' % color['foreground'])    
    
    if addRepeating:
        # add recurring events	
        for i in range(1, wks_in_sem+1):
        #for i in range(wks_in_sem, wks_in_sem+1):
            weekstr = 'Week ' + str(i)
            print (weekstr)
            
            mon = sem_start + datetime.timedelta(weeks=i-1)
            print ('mon =' + str(mon))
            
            monstr = mon.strftime("%Y-%m-%d").lstrip("0")
            print ('monstr =' + monstr)
            
            rec_event = {
            'summary': weekstr,
            'location': 'NWMissouri State',
            'start': {
            'date': monstr,
            'timeZone': 'America/Chicago'
            },
            'end': {
            'date': monstr,
            'timeZone': 'America/Chicago'
            },
            'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=5',
            ],
            'reminders': {
            'useDefault': False,
            'overrides': [],
            },
            "attendees": [
                {
                "email": email_invite,
                "displayName": name_invite
                }
            ],
            'colorId': str(color_id),
            }

            recurring_event  = service.events().insert(calendarId='primary', body=rec_event).execute()
            print (recurring_event ['id'])
    
    if addIndividual:
        # add individual events from csv file
        f = open(csvfile, 'r')
        print f

        for line in csv.reader(f):
            print line

            title, y, m, d = line
            print (title)
            
            mon = datetime.date(int(y), int(m), int(d))  
            print ('mon =' + str(mon))
            
            monstr = mon.strftime("%Y-%m-%d").lstrip("0")
            print ('monstr =' + monstr)
            
            rec_event = {
            'summary': title,
            'location': 'NWMissouri State',
            'start': {
            'date': monstr,
            'timeZone': 'America/Chicago'
            },
            'end': {
            'date': monstr,
            'timeZone': 'America/Chicago'
            },
            'reminders': {
            'useDefault': False,
            'overrides': [],
            },
            "attendees": [
                {
                "email": "dcase@nwmissouri.edu",
                "displayName": "Denise Case (NWMSU)"
                }
            ],
            'colorId': str(color_id),
            }

            ind_event  = service.events().insert(calendarId='primary', body=rec_event).execute()
            print (ind_event ['id'])

if __name__ == '__main__':
    main()
       
    