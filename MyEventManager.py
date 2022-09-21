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


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
import datetime
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
def insert_event(api, starting_date, ending_date, id):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if (starting_date == '') or (ending_date == ''):
        raise ValueError("Start or end time must be a string.")
    
    if (len(id) < 5 or len(id) > 1024):
        raise ValueError("id must be between 5 to 1024 characters!")

    eventbody = {
                    "kind": "calendar#event",
                    "id": id,
                    "summary": 'test #2',
                    "description": 'idk why delete doesn''t work',
                    "start": {
                        "date": starting_date
                    },
                    "end": {
                        "date": ending_date
                    },
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

# function to check if the current event needed to be updated is valid today till 2050
def check_date(api, ownCalendarId, eventIdToBeChecked):
    event = api.events().get(calendarId=ownCalendarId, eventId=eventIdToBeChecked).execute()
    current_date = datetime.datetime.strptime(event['start']['date'],'%Y-%m-%d').date()
    today_date =  datetime.datetime.today().date()
    upper_bound = datetime.datetime(2050,12,31).date()
    if current_date >= today_date and current_date <= upper_bound:
        return event
    else:
        raise ValueError("Can only modify events that are present and max year 2050")

# haven't tested this cause i need someone to test for me
def move_event(api, originalId, newId, eventId):
    events_result = api.events().move(calendarId=originalId, eventId=eventId, destination=newId).execute()
    return events_result

# this is okay, it runs:
# if this event has no attendee attribute (aka, no attendee at first), it creates the attribute then add people inside
# else, just append at the back of the list
def add_attendee(api, ownId, eventId, attendeeEmail: str):
    event = check_date(api,ownId,eventId)
    newattendeee = {"email": attendeeEmail, "organiser": 'False'}
    if event.get('attendees') != None:
        event['attendees'].append(newattendeee)
    else:
        event['attendees'] = [newattendeee]
        # add one line that limits maxAttendee
    event = api.events().update(calendarId=ownId, eventId=event['id'], body=event).execute()
    return event
    

# this is okay, it runs:
# if this event has attendee attribute (aka, no attendee at first), it runs a linear search to find the attendee email
# if no email is found, raise error, else, remove 
# else, that means no attendee attribute, so no attendees at all, so raise another error
def remove_attendee(api, ownId, eventId, attendeeEmail: str):
    event = check_date(api,ownId,eventId)
    found = -1
    i = 0
    if event.get('attendees') != None:
        while i < len(event['attendees']):
            if event['attendees'][i]['email'] == attendeeEmail:
                found = i
                break
            i += 1
        if found == -1:
            raise ValueError("No attendees match the email")
        event['attendees'].remove(event['attendees'][found])
        event = api.events().update(calendarId=ownId, eventId=event['id'], body=event).execute()
        return event
    else: 
        raise ValueError("There are no attendees in the event!")


def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events = get_upcoming_events(api, time_now, 10)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    """this test case written in 20/09/2022"""
    # newlyAddedEvent = insert_event(api, datetime.date.today().strftime("%Y-%m-%d"), '2022-09-23','123789') # event without any attendees
    # # print(newlyAddedEvent.get('id'))
    # # print(newlyAddedEvent.get('attendees'))
    # # test add attendees
    # newlyAddedEvent = add_attendee(api, 'primary', newlyAddedEvent['id'],'lloo0007@student.monash.edu') # add new attendees
    # # remove attendees
    # newlyAddedEvent = remove_attendee(api, 'primary', newlyAddedEvent['id'],'lloo0007@student.monash.edu') # this should remove lloo0007
    # newlyAddedEvent = remove_attendee(api, 'primary', newlyAddedEvent['id'],'lloo0007@student.monash.edu') # this should prompt error cause event now shouldn't have anyone 



    """haven't tested move_event"""
    # newevent3 = move_event(api, 'primary','lloo0007@student.monash.edu','123456789')
    # print(newevent3)

    """test to modify event older than today"""
    # newevent3 = api.events().get(calendarId='primary', eventId='1234689').execute()
    # print(newevent3['start']['date'])
    # newevent3 = check_date(api, 'primary', '1234689')
    # print(newevent3)
    # newevent3 = add_attendee(api,'primary','1234689','lloo0007@student.monash.edu')
    # print(newevent3)
if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()