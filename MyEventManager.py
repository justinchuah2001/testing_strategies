# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.
# can send calendar event invitation to a student using the student.monash.edu email.
# The app doesn't support sending events to non student or private emails such as outlook, gmail etc
# students must have their own api key
# no test cases for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html
# Name: Li Pin
# Student ID: 31108555


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
import datetime
from multiprocessing.sharedctypes import Value
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_api():
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if (number_of_events <= 0):
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])

# test insert()
def insert_event(api, starting_date, ending_date, event_location, event_name, id):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if (starting_date == '') or (ending_date == ''):
        raise ValueError("Start or end time must be a string.")
    
    if (len(id) < 5 or len(id) > 1024):
        raise ValueError("id must be between 5 to 1024 characters!")

    starting_date, ending_date = ensure_date_format(starting_date, ending_date)
    address_check(event_location)


    

    eventbody = {
                    "kind": "calendar#event",
                    "id": id,
                    "summary": event_name,
                    "description": 'test add',
                    "location": event_location,
                    "start": {
                        "dateTime": starting_date
                    },
                    "end": {
                        "dateTime": ending_date
                    },
                    "attendees": [
                        {
                        "email": 'lloo0007@student.monash.edu',
                        "organizer": 'False',
                        }
                    ],
                    "guestsCanInviteOthers": 'False',
                    "guestsCanModify": 'False',
                    "guestsCanSeeOtherGuests": 'True',
                    "reminders": {
                        "useDefault": 'False',
                        "overrides": [
                            {'method': 'popup', 'minutes': 10}
                        ]
                    },
                    "eventType": 'default'
                }

    events_result = api.events().insert(calendarId='primary', body=eventbody).execute()
    return events_result

# haven't tested this cause i need someone to test for me
def move_event(api, originalId, newId, eventId):
    events_result = api.events().move(calendarId=originalId, eventId=eventId, destination=newId).execute()
    return events_result

# this is okay, it runs:
# if this event has no attendee attribute (aka, no attendee at first), it creates the attribute then add people inside
# else, just append at the back of the list
def add_attendee(api, ownId, eventId, attendeeEmail: str):
    event = api.events().get(calendarId=ownId, eventId=eventId).execute()
    newattendeee = {"email": attendeeEmail, "organiser": 'False'}
    if hasattr(event,'attendees'):
        event['attendees'].append(newattendeee)
    else:
        event['attendees'] = [newattendeee]
    event = api.events().update(calendarId=ownId, eventId=event['id'], body=event).execute()
    return event

# this is okay, it runs:
# if this event has attendee attribute (aka, no attendee at first), it runs a linear search to find the attendee email
# if no email is found, raise error, else, remove 
# else, that means no attendee attribute, so no attendees at all, so raise another error
def remove_attendee(api, ownId, eventId, attendeeEmail: str):
    event = api.events().get(calendarId=ownId, eventId=eventId).execute()
    found = 0
    i = 0
    if hasattr(event,'attendees'):
        while i < len(event['attendees']):
            if event['attendees'][i] == attendeeEmail:
                found = i
                break
            i += 1
        if found == 0:
            raise ValueError("No email is found!")
        event['attendees'].remove(event['attendees'][found])
        event = api.events().update(calendarId=ownId, eventId=event['id'], body=event).execute()
    else: 
        raise ValueError("There are no attendees in the event!")
    return event

def get_events(api, Id):
    event = api.events().get(calendarId='primary', eventId=Id).execute()
    return event['summary']

def delete_events(api,  Id):
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'
    event = api.events().get(calendarId='primary', eventId = Id).execute()
    if event.get('end').get('dateTime') > time_now:
        raise ValueError("Only past events can be deleted")
    else:
        api.events().delete(calendarId='primary', eventId=Id).execute()
    return

def ensure_date_format(start_date, end_date):
    start = start_date.split("T")
    end = end_date.split("T")
    try:
        start[0] != (datetime.datetime.strptime(start[0], '%Y-%b-%d'))
        start[0] = datetime.datetime.strptime(start[0], '%Y-%b-%d').strftime('%Y-%m-%d')
    except:
        try:
            start[0] != datetime.datetime.strptime(start[0], '%Y-%m-%d')
            start[0] = datetime.datetime.strptime(start[0], '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            raise ValueError("Wrong Date Format")

    try:
        end[0] != (datetime.datetime.strptime(end[0], '%Y-%b-%d'))
        end[0] = datetime.datetime.strptime(end[0], '%Y-%b-%d').strftime('%Y-%m-%d')
    except:
        try:
            end[0] != datetime.datetime.strptime(end[0], '%Y-%m-%d')
            end[0] = datetime.datetime.strptime(end[0], '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            raise ValueError("Wrong Date Format")
    return start[0] + "T" + start[1], end[0] + "T" + end[1]


def address_check(location):
    format = 0
    for i in range(len(location)):
        if format == 0:
            if str.isdigit(location[i]):
                format += 1
        elif format == 1:
            try:
                if location[i].isupper() and location[i+1].isupper():
                    format += 1
            except:
                
                raise ValueError("Incorrect Address Format")
        elif format == 2:
            if str.isdigit(location[i]):
                format += 1
    if format != 3:
        raise ValueError("Incorrect Address Format")
    return True


def main():
    # address = """Mrs Smith 123 Fake St. Clayton VIC 3400 AUSTRALIA"""
    # address_check(address)
    print(ensure_date_format('2022-SEP-20T20:06:14+08:00','2022-SEP-20T20:06:14+08:00'))
    api = get_calendar_api()
    # time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    # events = get_upcoming_events(api, time_now, 10)

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])
    

    newevent2 = insert_event(api,'2022-9-20T20:07:14+08:00','2022-9-20T20:07:14+08:00','Mrs Smith 546 Fake St. Clayton VIC 3400 AUSTRALIA', 'realevent', '1234testings')


    # delete_events(api, 'date12345')
    # print(newevent2.get('attendees'))
    # newevent3 = move_event(api, 'primary','lloo0007@student.monash.edu','123456789')
    # print(newevent3)
    # newevent3 = api.events().get(calendarId='primary', eventId='1234689').execute()
    # print(newevent3)
    # newevent3 = add_attendee(api,'primary','1234689','lloo0007@student.monash.edu')
    # print(newevent3)
    # newevent4 = add_attendee(api,'primary','1234689','ghua0010@student.monash.edu')
    # newevent4 = add_attendee(api,'primary','1234689','lloo0007@student.monash.edu')
    # print(newevent4.get('attendees'))
    # newevent5 = remove_attendee(api,'primary','1234689','ghua0010@student.monash.edu')
    # print(newevent5.get('attendees'))
if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()