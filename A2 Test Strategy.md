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

For spec 1, we need to implement the functionality of creating event in the calendar. The event should have its own id, name, attendees, date and location which can be online or physical at a venue, so the function **insert\_event** is created which will be explained more in detail in specification 2 **Event Organizer**. This event can be set up on past, future and present dates but only can delete the events on past dates, function **delete\_event** will make this work, which this is different from cancel an event, a cancelled event will stay as achieved that can be restored in future if needed, (don't think needed here) and also the function **check\_emailFormat** is used to check the correct format of email.

Event dates can only be yyyy-mm-dd (2022-02-22) format or dd-MON-yy (12-AUG-22), function **ensure\_date\_format** is used to check the format of starting date and ending date of event. As there are certain limitations to the Google Calendar API, we had to ensure that the date format is applicable, therefore if the input parameter fulfills the specified requirements of the date format, it will be converted into the form of yyyy-mm-dd otherwise an error will be raised. Then as the calendar takes in event dates in a date time format, we have to also ensure that the time is within the accepted format, which leads to us having a **ensure\_time\_format** function. This function just takes in an input of time and make sure it is in a %H:%M:%S (20:15:20) 24 hour time format, otherwise it will raise an error.

Event location can only be American, Australian or abbreviated street types, so **address\_check** is created to check the location of event(online/physical) and the format of location. In the specification it isn't really implicitly explained on how an address is checked, therefore we broke down the given examples of the address into certain patterns that we noticed which has a pattern of (Name, Street, Country). When no input is given in the parameter of the **address\_check** function, it will be assumed that the address is online.

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

In this test suite, we will have created all the necessary functions to ensure all the requirements in the specification is fulfilled.

***Testing method:*** 

Branch Coverage

***Tester:***

Jun Jie Chua, Guoyueyang Huang, Li Pin Loo

***Rationale:***

For this test suite, we have chosen to test it in a form of branch coverage. Firstly for the function used to ensure the address format, we have tested out all the branches that covers the function, to ensure that every decision of the program is exercised once. In here, we tested all branches that leads to a valid address and also all branches that leads to an invalid address.

Moving on, in the function used to ensure the valid date format and time format, branch coverage is also implemented as a testing technique, as similarly to the address format function, we have tested all possible branches that leads to a valid date and time format and also all decisions that leads to an invalid date and time format

### Testing

**Test 1: address_check Function**

**Description:**

This test suite is to test the function that checks the address to make sure that it is in the correct format.

**Provided Input with Expected and Actual Output.**
***Test Frame 1***


| Test Case No | Input | Expected Output | Actual Output |
| --- | --- | --- | --- |
| 1 | 'Mrs Smith, 546 Fake St., Clayton VIC 3400, AUSTRALIA'  | True | True |
| 2 | 'Mr Morrison 11 Banks Av WAGGA WAGGA WEST VIRGINIA 2650 US' | True | True |
| 3 | '' | False | False |
| 4 | 'online' | False | False |
| 5 | '52, jalan 1234A, KL' | ValueError() | ValueError() |
| 6 | '52KL' | ValueError() | ValueError() |
| 7 | 'Mrs Smith 546 Fake St. Clayton 3400 A' | ValueError() | ValueError() |

**Test 2: ensure_date_format Function**

**Description:**

This test suite is to test the function that checks the date to make sure that it is in the correct format.

**Provided Input with Expected and Actual Output.**

***Test Frame 1***

| Test Case No | Input (starting_date, ending_date) | Expected Output | Actual Output |
| --- | --- | --- | --- |
| 1 | ('2022-8-4', '2022-9-4')  | True | True |
| 2 | ('4-JAN-21', '4-OCT-22') | True | True |
| 3 | ('2022-9-4', '2022-8-4') | ValueError() | ValueError() |
| 4 | ('2022-9-4', '22-8-4') | ValueError() | ValueError() |
| 5 | ('2051-9-4', '2052-8-4') | ValueError() | ValueError() |
| 6 | ('22-9-4', '22-12-4') | ValueError() | ValueError() |
| 7 | ('2-9-19', '13-12-21') | ValueError() | ValueError() |

**Test 3: ensure_time_format Function**

**Description:**

This test suite is to test the function that checks the time to make sure that it is in the correct format.\

**Provided Input with Expected and Actual Output.**

***Test Frame 1***

| Test Case No | Input | Expected Output | Actual Output |
| --- | --- | --- | --- |
| 1 | '9:6:23'  | True | True |
| 2 | '15:55:3' | True | True |
| 3 | '23:66:8' | ValueError() | ValueError() |
| 4 | '25:12:69' | ValueError() | ValueError() |

## Test Suite 2: Creation of Events Organiser

***Description:***

Test suite 2 is created to test what the organizer of the event can do, such as move event to other attendees, update event details, etc.

***Testing method:*** 

Branch Coverage, condition coverage, statement coverage

***Tester:***

Jun Jie Chua, Guoyueyang Huang, Li Pin Loo

***Rationale:***

For this test suite, we have decided to use branch coverage, condition coverage and statement coverage to test the functions regarding to event organizers. 

First, check_emailFormat is tested with branch coverage and condition coverage. This is to ensure the user is using a correct email format when attempting to create, or modify an event. Here, we tested all branches that lead to a wrong email format and also branches that lead to a correct email format. 

Second, check_date function is tested with branch coverage, condition coverage and statement coverage. This allows us to cover all possible outcomes, as this function also contains ensure_time_format function, utilising what we have tested in test suite 1.

Third, check_details function is tested with branch coverage and condition coverage. This allows us to cover all possible outcomes.

Fourth, insert_event is tested with mocking. For insert_event function, we've tested with branch coverage and condition coverage also, to ensure all branches and possibilities are covered. Within insert_event function, it contains other check functions like ensure_time_format, address_check, check_attendees_limit, and more. These functions are also covered in other test suites, with their own respective test methods.

Fifth, delete_event is tested with mocking. Since we can't test delete_event with actual events, we tested such that it will raise TypeError. This is to ensure the function is executed as intended, and such branch is also covered as well. 

Sixth, move_event is tested with mocking. Similar to delete_event, since testing moving event to other user couldn't be tested, we decided to test its call count to ensure the function is executed. 

### Testing

**Test 1: check_emailFormat Function**

**Description:**

This test frame is to test check_emailFormat function, a function that checks if the email format is correct. 

**Provided Input with Expected and Actual Output.**

***Test Frame 1***

| Test Case No | Input | Expected Output | Actual Output |
| --- | --- | --- | --- |
| 1 | "kekw@gmail.com" | True | True |
| 2 | "primary" | ValueError() | ValueError() |
| 3 | "PEPEGA" | ValueError() | ValueError() |
| 4 | "PEPEGA@hjello" | ValueError() | ValueError() |
| 5 | "PEPEGA.weeeeeeeeeeeeee" | ValueError() | ValueError() |

**Test 2: check_date Function**

**Description:**

This test frame is to test check_date function, a function that allows events only from today and till 2050 can be modified. 

**Provided Input with Expected and Actual Output.**

***Test Frame 1***

| Test Case No | Input | Expected Output | Actual Output |
| --- | --- | --- | --- |
| 1 | "2024-09-22T00:00:00+08:00" | True | True |
| 2 | "2020-09-22T00:00:00+08:00" | ValueError() | ValueError() |
| 3 | "2051-01-01T00:00:00+08:00" | ValueError() | ValueError() |

**Test 3: check_details Function**

**Description:**

This test frame is to test check_details function, a function that allows event to be modified if the user is the organizer of the event.

**Provided Input with Expected and Actual Output.**

***Test Frame 1***

| Test Case No | Input (event organizer email, modifier email) | Expected Output | Actual Output |
| --- | --- | --- | --- |
| 1 | ("113@gmail.com", "113@gmail.com") | True | True |
| 2 | ("113@gmail.com","223@gmail.com") | ValueError() | ValueError() |

**Test 4: insert_event Function**

**Description:**

This test frame is to test insert_event function, a function that allows a user to create an event and become organizer of the event.

**Provided Input with Expected and Actual Output.**

***Test Frame 1***

| Test Case No | Input (multiple inputs) | Expected Output | Actual Output |
| --- | --- | --- | --- |
| 1 | start_date = "2022-09-25" <br> end_date = "2022-09-26" <br> start_time = "20:06:14" <br> end_time = "20:06:14" <br> id = '753951' <br> event_name = 'PEPEGA' <br> location = "" <br> calID = "123456@gmail.com" <br> attendees = ["23456@gmail.com"] | True (event resource id == id) | True (event resource id == id) |
| 2 | start_date = "" <br> end_date = "" <br> start_time = "20:06:14" <br> end_time = "20:06:14" <br> id = '753951' <br> event_name = 'PEPEGA' <br> location = "" <br> calID = "123456@gmail.com" <br> attendees = ["23456@gmail.com"] | ValueError() | ValueError() |
| 3 | start_date =  "2022-09-25" <br> end_date = "2022-09-26" <br> start_time = "20:06:14" <br> end_time = "20:06:14" <br> id = '1' <br> event_name = 'PEPEGA'<br> location = "" <br> calID = "123456@gmail.com" <br> attendees = ["23456@gmail.com"] | ValueError() | ValueError() |

**Test 5: delete_event Function**

**Description:**

This test frame is to test delete_event function, a function that allows the organizer of the event to delete the event

**Provided Input with Expected and Actual Output.**

***Test Frame 1***

| Test Case No | Input (multiple inputs) | Expected Output | Actual Output |
| --- | --- | --- | --- |
| 1 | calendarId = '123@gmail.com' <br> eventId = '753951' | ValueError() | ValueError() |

**Test 6: move_event Function**

**Description:**

This test frame is to test move_event function, a function that allows the original organizer of the event to move the organizer role to other user. Note, this only works with personal email (not monash email)

**Provided Input with Expected and Actual Output.**

***Test Frame 1***

| Test Case No | Input (multiple inputs) | Expected Output | Actual Output |
| --- | --- | --- | --- |
| 1 | calId = "123456789@gmail.com" <br> newCalID = "23456@gmail.com" <br> Id = '753951' | ValueError() | ValueError() |

## Test Suite 3: Creation of Attendees

***Description:***

In this test suite, we will have created all the necessary functions to ensure all the requirements in the specification is fulfilled.

***Testing method:*** 

Branch Coverage

***Tester:***

Jun Jie Chua, Guoyueyang Huang, Li Pin Loo

***Rationale:***

For this test suite, we have chosen to test it in a form of branch coverage. Firstly for the function used to ensure the number of attendees is within the limit, we have tested out all the branches that covers the function, to ensure that every decision of the program is exercised once. In here, we tested all branches that leads to a valid number of attendees and also all branches that leads to an invalid number of attendees.

**Testing**

**Test 1**

**Ensure Valid Number Of Attendees Function**

**Description:**

This test suite is to test the function that checks the number of attendees to make sure that it is in the correct amount. 

**Provided Input with Expected and Actual Output.**

***Test Frame 1***

| Test Case No | Input (multiple inputs) | Expected Output | Actual Output |
| --- | --- | --- | --- |
| 1 | attendees= ['john@gmail.com', 'hi@gmail.com'] = "2022-09-25" | True | True |
| 2 | attendees= ['john@gmail.com', 'hi@gmail.com', '1@gmail.com', '2@gmail.com', '3@gmail.com', '4@gmail.com', '5@gmail,com', '6@gmail.com', '7@gmail.com', '8@gmail.com', '9@gmail.com', '10@gmail.com', '13@gmail.com', '14@gmail.com', '15@gmail.com', '16@gmail.com', '17@gmail.com', '18@gmail.com', '19@gmail.com', '20@gmail.com', '12@gmail.com', '21@gmail.com' ] | ValueError() | ValueError() |

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
