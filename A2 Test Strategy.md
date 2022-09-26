# **FIT2107 Whitebox Testing**

**Team: 06**

**Members: Jun Jie Chua, Guoyueyang Huang, Li Pin Loo**

# Introduction:

In this assignment, we are going to employ various automated **BlackBox** and **Whitebox** with **unit testing** techniques (including **mocking**) to test and implement functional requirements from a specification document provided. Based on the provided specification, the ***MyEventManager-v2*** module should be used as a calendar and have functionalities on **event**, **event organiser**, **attendees**, **reminder** and **navigation**. The event inside this application should able to be an official meeting, an online meeting or a physical event at a venue. For each event, an event id, event name, event location, attendees and date is needed, all events can be deleted or cancelled. Therefore we need to create test suites for all the functionalities first in order to obey the **test driven development (TDD)** which tests are created (iteratively) before the software is fully developed and tracked all software development by repeatedly testing the software against all test cases. We have decided to split the testing into the following test suites: 

- The **first** test suite will be testing the creation of event.
- The **second** test suite will be testing on the creation of event organiser that the organiser can only create and update events at present and future dates.
- The **third** test suite will be testing the attendees details of the event.
- The **fourth** test suite will be testing the reminder of each event.
- The **fifth** test suite will be testing on the navigation of the calendar.
- The **sixth** test suite will be testing on the import and export of the event.

# Implementation:

## Spec 1: Event

For spec 1, we need to implement the functionality of creating event in the calendar. The event should have its own id, name, attendees, date and location which can be online or physical at a venue, so the function **insert\_event** is created. This event can be set up on past, future and present dates but only can delete the events on past dates, function **delete\_event** will make this work, which this is different from cancel an event, a cancelled event will stay as achieved that can be restored in future if needed, and also the function **check\_emailFormat** is used to check the correct format of email.  Also we need to check the date and location format in the function. Event dates can only be yyyy-mm-dd (2022-02-22) format or dd-MON-yy (12-AUG-22), function **ensure\_time\_format** is used to check the format of starting date and ending date of event. Event location can only be American, Australian or abbreviated street types, so **address\_check** is created to check the location of event(online/physical) and the format of location.

## Spec 2: Event Organiser

For spec 2, event organiser is responsible for creating an event(function **insert\_event**) and also can create event for others. Other than that, organiser also can update the event(function **update\_event**) at present and future but cannot exceed 2050 as mentioned in specification. Also, since only the owner(organiser) or the attendee who has the writer role of this event can delete, create, update or passing this event to someone else, so the **delete\_events**, **insert\_event**, **update\_event** and **move\_event** function is created which can be accessed by organiser or writer only.

## Spec 3: Attendees

For spec 3, attendee is the person who attends the event, so the role of attendee is reader as default. As the attendee will be notified when an event is created, change and cancellation, in the function body of **insert\_event** and **update\_event**, a piece of code of reminder will be added into the event body, and it will notify the attendee before the event.

Since the attendee can only view the events for a maximum of 5 years in past and next five years in future, this will be limit in function

Also for each event, there is a limit of 20 attendees, this will be limit in function 

## Spec 4: Reminders(Notifications)

For spec 4, reminders are part of the event, so a piece of code for sending event is included in the event body of **insert\_event** and **update\_event** in order to send the notification before the set time.

## Spec 5: Navigation

For spec 5,  the application should provide a navigation mechanism, which user can navigate through days, months and years to view the details of events. To achieve this, a function **terminal\_ui** is created for users to look through the events in the calendar and also be able to search for an event by using event name, date or keywords of the event.

## Spec 6: Import and Export

For spec 6, the application should support importing and exporting of events in JSON format and should compatible with Windows, Ubuntu and OSX operating systems, so function **export\_event** and **import\_event** is used to importing and exporting in this application.

# Test Suites:

## Test Suite 1: Creation of Events

***Description:***

***Testing method:*** 

***Tester:***

Jun Jie Chua, Guoyueyang Huang, Li Pin Loo

***Rationale:***

## Test Suite 2: Creation of Events Organiser

***Description:***

Test suite 2 is created to test what the organizer of the event can do, such as move event to other attendees, update event details, etc.

***Testing method:*** 

For this test suite, 

***Tester:***

Jun Jie Chua, Guoyueyang Huang, Li Pin Loo

***Rationale:***



## Test Suite 3: Creation of Attendees

***Description:***

***Testing method:*** 

***Tester:***

Jun Jie Chua, Guoyueyang Huang, Li Pin Loo

***Rationale:***

## Test Suite 4: Testing of Reminders(Notifications)

***Description:***

***Testing method:*** 

***Tester:***

Jun Jie Chua, Guoyueyang Huang, Li Pin Loo

***Rationale:***

## Test Suite 5: Testing of Navigation

***Description:***

***Testing method:*** 

***Tester:***

Jun Jie Chua, Guoyueyang Huang, Li Pin Loo

***Rationale:***

## Test Suite 6: Testing the import and export of event

***Description:***

***Testing method:*** 

***Tester:***

Jun Jie Chua, Guoyueyang Huang, Li Pin Loo

***Rationale:***