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
# Student ID: 31108555 aa


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
import datetime
import pickle
import os.path
import re
from subprocess import check_output
from tracemalloc import start
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from calendar import monthrange
import json
# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SCOPES = ['https://www.googleapis.com/auth/calendar']
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

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
def insert_event(api, calID, starting_date, ending_date, start_time, end_time, event_location, event_name, id, attendees = None):
    # checks the start end date format (yyyy-mm-dd || dd-MON-yy), id format, and time format (24hr)
    if (starting_date == '') or (ending_date == ''):
        raise ValueError("Start or end time must be a string.")
    if (len(id) < 5 or len(id) > 1024):
        raise ValueError("id must be between 5 to 1024 characters!")
    starting_date, ending_date = ensure_date_format(starting_date, ending_date)
    ensure_time_format(start_time, end_time)
    check_emailFormat(calID)

    # combine date and time together to become datetime format
    start = starting_date + "T" + start_time + "+08:00"
    end = ending_date + "T" + end_time + "+08:00"
    # check if address is either online or physical location
    flag = address_check(event_location)
    if not flag:
        event_location = 'online'
        
    # add roles to attendees, also check the attendees email format
    attendeesFormat = []
    for i in range (len(attendees)):
        check_emailFormat(attendees[i])
        create_reader(api, calID, attendees[i])
        attendeesFormat.append({"email": attendees[i]})

    eventbody = {
                    "kind": "calendar#event",
                    "id": id,
                    "summary": event_name,
                    "description": 'test add',
                    "location": event_location,
                    "start": {
                        "dateTime": start
                    },
                    "end": {
                        "dateTime": end
                    },
                    "attendees": attendeesFormat,
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

    events_result = api.events().insert(calendarId=calID, body=eventbody).execute()
    return events_result

# function to check if the current event needed to be updated is valid today till 2050
def check_date(api, ownCalendarId, eventIdToBeChecked):
    event = api.events().get(calendarId=ownCalendarId, eventId=eventIdToBeChecked).execute()
    current_date = datetime.datetime.strptime(event['start']['date'],'%Y-%m-%d')
    today_date =  datetime.datetime.today()
    upper_bound = datetime.datetime(2050,12,31)
    if current_date >= today_date and current_date <= upper_bound:
        return event
    else:
        raise ValueError("Can only modify events that are present and max year 2050")

def check_details(api, ownCalendarId, eventIdToBeChecked):
    event = api.events().get(calendarId=ownCalendarId, eventId=eventIdToBeChecked).execute()
    event_organiser_email = event['organizer']['email']
    if ownCalendarId == event_organiser_email:
        return event
    else:
        raise ValueError("Only organiser of the event can manage the event details!")

def check_emailFormat(email):
    # findAt = -1
    # i = 0
    # if email is None or email == '':
    #     raise ValueError("Email format is incorrect.")
    # while i < (len(email)):
    #     if email[i] == '@':
    #         findAt = i
    #         break
    #     i += 1
    # if findAt == -1 or findAt+1 == len(email):
    #     raise ValueError("Email format is incorrect.")
    # else:
    #     return True
        # pass the regular expression
    # and the string into the fullmatch() method
    if email == "primary":
        return True
    if(re.fullmatch(regex, email)):
        return True
    else:
        raise ValueError("Email format is incorrect.")
    

def update_event(api, ownId, eventId, newStartDate, newEndDate, newName, newStartTime, newEndTime, newLocation, newStatus, newAttendees):
    # check if the user requesting to modify the event is the organizer of the event
    # check whether the event to be modified is within modifiable range of date
    # check the calendarID of the current user
    event = check_details(api,ownId,eventId)
    event = check_date(api,ownId,eventId)
    check_emailFormat(ownId)
    # get current event details
    newEventSDatetime = event['start']['datetime']
    newEventEDatetime = event['end']['datetime']
    newEventLocation = event['location']
    newEventStatus = event['status']
    newEventName = event['summary']
    # if current event has attendees, get the current list, else, creates an empty list
    if event.get('attendees') != None:
        newEventAttendees = event['attendees']
    else: 
        newEventAttendees = []

    if newStartDate is not None and newEndDate is not None:
        if newStartDate == '' or newEndDate == '':
            raise ValueError("Start or end time must be a string.")
        starting_date, ending_date = ensure_date_format(starting_date, ending_date)
        ensure_time_format(newStartTime, newEndTime)
        start = starting_date + "T" + newStartTime + "+08:00"
        end = ending_date + "T" + newEndTime + "+08:00"
        newEventSDatetime = start
        newEventEDatetime = end
    if newName is not None:
        newEventName = newName
    if newLocation is not None:
        address_check(newLocation)
        newEventLocation = newLocation
    if newStatus is not None:
        newEventStatus = newStatus
    if newAttendees is not None:
        for i in range (len(newAttendees)):
            check_emailFormat(newAttendees[i])
            newEventAttendees.append({"email": newAttendees[i]})

    eventbody = {
                "kind": "calendar#event",
                "id": eventId,
                "summary": newEventName,
                "description": 'test add',
                "location": newEventLocation,
                "status": newEventStatus,
                "start": {
                    "dateTime": newEventEDatetime
                },
                "end": {
                    "dateTime": newEventSDatetime
                },
                "attendees": newEventAttendees,
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
    event = api.events().update(calendarId=ownId, eventId=event['id'], body=eventbody).execute()
    return event

# only works with personal email
def move_event(api, originalId, newId, eventId):
    # the authentication popped, choose the new calendar ID you wish to move to, NOT YOUR OWN CALENDAR
    events_result = api.events().move(calendarId=originalId, eventId=eventId, destination=newId).execute()
    return events_result

# this is okay, it runs:
# if this event has no attendee attribute (aka, no attendee at first), it creates the attribute then add people inside
# else, just append at the back of the list
def add_attendee(api, ownId, eventId, attendeeEmail: str):
    event = check_details(api,ownId,eventId)
    event = check_date(api,ownId,eventId)
    check_emailFormat(attendeeEmail)
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
    event = check_details(api,ownId,eventId)
    event = check_date(api,ownId,eventId)
    check_emailFormat(attendeeEmail)
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

def get_event(api, Id):
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

def ensure_date_format(start_date, end_date = None):
    try:
        datetime.datetime.strptime(start_date, '%Y-%b-%d')
        start_date = datetime.datetime.strptime(start_date, '%Y-%b-%d').strftime('%Y-%m-%d')
        
    except:
        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
            
        except:
            raise ValueError("Wrong Date Format")

    try:
        (datetime.datetime.strptime(end_date, '%Y-%b-%d'))
        end_date = datetime.datetime.strptime(end_date, '%Y-%b-%d').strftime('%Y-%m-%d')
    except:
        try:
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            raise ValueError("Wrong End Date Format")
    
    if int(start_date.split("-")[0]) > 2050:
        raise ValueError("Year can't be more than 2050")
    
    return start_date, end_date

def ensure_time_format(start_time, end_time = None):
    try:
        start_time == datetime.datetime.strptime(start_time, '%H:%M:%S')
    except:
        raise ValueError("Incorrect Start Time Format")
    try:
        end_time == datetime.datetime.strptime(end_time, '%H:%M:%S')
    except:
        raise ValueError("Incorrect End Time Format")

    return 


def address_check(location):
    if location.upper() == 'ONLINE' or location == '':
        return False
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

def create_reader(api, calendarId, user_email):
    rolebody = {
        "role": "reader",
        "scope": {
        "type": "user",
        "value": user_email,
        }
    }
    created_rule = api.acl().insert(calendarId=calendarId, body=rolebody).execute()
    return created_rule

def create_writer(api, calendarId, user_email):
    rolebody = {
        "role": "writer",
        "scope": {
        "type": "user",
        "value": user_email
        }
    }
    created_rule = api.acl().insert(calendarId=calendarId, body=rolebody).execute()
    return created_rule

def create_owner(api, calendarId, user_email):
    rolebody = {
        "role": "owner",
        "scope": {
        "type": "user",
        "value": user_email
        }
    }
    created_rule = api.acl().insert(calendarId=calendarId, body=rolebody).execute()
    return created_rule

def search_event(api, query):
    if query == None:
        return
    events_result = api.events().list(calendarId='primary', q = query, singleEvents=True, orderBy='startTime').execute()
    events_result = events_result.get('items', [])
    if not events_result:
        print("No such event")
        return
    for event in events_result:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    return

def get_events(api, starting_time, ending_time):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """

    events_result = api.events().list(calendarId='primary', timeMin=starting_time, timeMax=ending_time, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])

def print_events(api, start_time, end_time):
    events = get_events(api, start_time, end_time)
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    return
    
def export_event(api, starting_time, ending_time):
    items = get_events(api, starting_time, ending_time)
 
    with open("output.json", "w") as outfile:
        json.dump(items, outfile)
    return

def import_event(api):
    f = open('output.json')
    data = json.load(f)
    calID = 'primary'
    for i in data:
        startDateTime = i['start']['dateTime']
        endDateTime = i['end']['dateTime']
        event_location = i['location']
        event_name = i['summary']
        id = i['id']
        startDate = startDateTime.split("T")
        endDate = endDateTime.split("T")
        startTime = startDate[1].split("+")
        endTime = endDate[1].split("+")
        insert_event(api, calID, startDate[0], endDate[0], startTime[0], endTime[0], event_location, event_name, id)


def terminal_ui (api):
    inp = None
    while inp != "q":
        inp = input(
        """Please enter an input: 
Q = Quit
D = View by Day
M = View by Month
Y = View by Year
S = Search
Input: """)
        if inp == "s":
            query = input("What would you like to search: \n")
            search_event(api, query)
        if inp == "d":
            year = input("Enter the year: \n")
            month = input("Enter the month: \n")
            day = input ("Enter the day: \n")
            start_time = year + "-" + month + "-" + day + 'T00:00:00+08:00'
            end_time = year + "-" + month + "-" + day + 'T23:59:00+08:00'
            print_events(api, start_time, end_time)
            while inp != "c":
                inp = input("""Please enter another input
Q = Quit
I = Increase day by one
D = Decrease day by one
C = Change View/Change to Search
Input: """)
                if inp == "q":
                    return
                elif inp == "i":
                    day = str(int(day) + 1)
                    if int(day) > monthrange(int(year), int(month))[1]:
                        month = str(int(month) + 1)
                        day = '1'
                    start_time = year + "-" + month + "-" + day + 'T00:00:00+08:00'
                    end_time = year + "-" + month + "-" + day + 'T23:59:00+08:00'
                    print_events(api, start_time, end_time)
                elif inp == "d":
                    day = str(int(day) - 1)
                    start_time = year + "-" + month + "-" + day + 'T00:00:00+08:00'
                    end_time = year + "-" + month + "-" + day + 'T23:59:00+08:00'
                    print_events(api, start_time, end_time)
                else:
                    break
        if inp == "m":
            year = input("Enter the year: \n")
            month = input("Enter the month: \n")
            start_time = year + "-" + month + "-" + '1' + 'T00:00:00+08:00'
            end_time = year + "-" + month + "-" + str(monthrange(int(year), int(month))[1]) + 'T23:59:00+08:00'
            print_events(api, start_time, end_time)
            while inp != "c":
                inp = input("""Please enter another input
Q = Quit
I = Increase month by one
D = Decrease month by one
C = Change View
Input: """)
                if inp == "q":
                    return
                elif inp == "i":
                    month = str(int(month) + 1)
                    if int(month) > 12:
                        month = '1'
                        year = str(int(year) + 1)
                    start_time = year + "-" + month + "-" + '1' + 'T00:00:00+08:00'
                    end_time = year + "-" + month + "-" + str(monthrange(int(year), int(month))[1]) + 'T23:59:00+08:00'
                    print_events(api, start_time, end_time)
                elif inp == "d":
                    month = str(int(month) - 1)
                    if int(month) < 1:
                        month = '12'
                        year = str(int(year) - 1)
                    start_time = year + "-" + month + "-" + '1' + 'T00:00:00+08:00'
                    end_time = year + "-" + month + "-" + str(monthrange(int(year), int(month))[1]) + 'T23:59:00+08:00'
                    print_events(api, start_time, end_time)
                else:
                    break
        if inp == "y":
            year = input("Please input a year\n")
            start_time = year + "-" + '1' + "-" + '1' + 'T00:00:00+08:00'
            end_time = year + "-" + '12' + "-" + str(monthrange(int(year), 12)[1]) + 'T23:59:00+08:00'
            print_events(api, start_time, end_time)
            while inp != "c":
                inp = input("""Please enter another input
Q = Quit
I = Increase year by one
D = Decrease year by one
C = Change View/Change to Search
Input: """)
                if inp == "q":
                    return
                elif inp == "i":
                    year = str(int(year) + 1)
                    start_time = year + "-" + '1' + "-" + '1' + 'T00:00:00+08:00'
                    end_time = year + "-" + '12' + "-" + str(monthrange(int(year), 12)[1]) + 'T23:59:00+08:00'
                    print_events(api, start_time, end_time)
                elif inp == "d":
                    year = str(int(year) - 1)
                    start_time = year + "-" + '1' + "-" + '1' + 'T00:00:00+08:00'
                    end_time = year + "-" + '12' + "-" + str(monthrange(int(year), 12)[1]) + 'T23:59:00+08:00'
                    print_events(api, start_time, end_time)
    return


def main():
    # address = """Mrs Smith 123 Fake St. Clayton VIC 3400 AUSTRALIA"""
    # address_check(address)
    # print(ensure_date_format('2022-SEP-20T20:06:14+08:00','2022-SEP-20T20:06:14+08:00'))
    api = get_calendar_api()
    # time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # terminal_ui(api)
    # events = get_upcoming_events(api, '2022-9-20T00:00:10+08:00', 10)

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])
    # check_emailFormat("something@gmail.com")

    # newevent2 = insert_event(api,'2022-9-22','2022-9-22','00:07:14','23:50:00','Mrs Smith 546 Fake St. Clayton VIC 3400 AUSTRALIA', 'ddd', 'ddd123ddd')
    print(ensure_date_format('2022-SEP-20', '2022-SEP-20'))
    insert_event(api,'primary', '2022-9-23','2022-9-23','00:07:14','23:50:00','Mrs Smith 546 Fake St. Clayton VIC 3400 AUSTRALIA', 'test_reminder', 'ccc123ccc', ['lloo0007@student.monash.edu'])
    # export_event(api, '2022-9-21T00:00:10+08:00', '2022-9-23T00:00:10+08:00')
    # import_event(api)
    # user_interface(api, 2022, '2022-9-21T20:07:14+08:00', 10)
    # user_interface(api, time_now)
    # terminal_ui(api)
    # ensure_time_format('20:07:14')
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