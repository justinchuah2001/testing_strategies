from datetime import datetime
from json import JSONDecodeError
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock, patch, call
import MyEventManager
# Add other imports here if needed
class MyEventManagerTest(unittest.TestCase):
    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = MyEventManager.get_upcoming_events(mock_api, time, num_events)
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    # Add more test cases here
    # This test tests number of upcoming events.
    def test_insert_valid_event(self):
        start_date = "2022-09-25"
        end_date = "2022-09-26"
        start_time = "20:06:14"
        end_time = "20:06:14"
        id = '753951'
        event_name = 'PEPEGA'
        location = ""
        calID = "123456@gmail.com"
        attendees = ["23456@gmail.com"]

        mock_api = MagicMock()
        events = MyEventManager.insert_event(mock_api, calID, start_date, end_date, start_time, end_time, location, event_name ,id, attendees) #i don't understand but ok
        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.return_value.get.call_count, 0)
        args, kwargs = mock_api.events.return_value.insert.call_args_list[0] # this line to get the event body
        self.assertEqual(kwargs.get('body').get('id'), id)
    
    def test_print_events(self):
        mock_api = MagicMock()
        MyEventManager.print_events(mock_api, '2022-09-25T00:07:14+08:00', '2022-09-26T23:50:00+08:00')
        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.return_value.get.call_count, 0)
        
    def test_insert_invalid_event(self):
        start_date = ""
        end_date = ""
        start_time = "20:06:14"
        end_time = "20:06:14"
        id = '753951'
        event_name = 'PEPEGA'
        location = ""
        calID = "123456@gmail.com"
        attendees = ["23456@gmail.com"]

        mock_api = MagicMock()
        with self.assertRaises(ValueError):
            events = MyEventManager.insert_event(mock_api, calID, start_date, end_date, start_time, end_time, location, event_name ,id, attendees) #i don't understand but ok

        start_date = "2022-09-25"
        end_date = "2022-09-26"
        id = '1'
        mock_api = MagicMock()
        with self.assertRaises(ValueError):
            events = MyEventManager.insert_event(mock_api, calID, start_date, end_date, start_time, end_time, location, event_name ,id, attendees) #i don't understand but ok


    def test_search_event(self):
        query = 'parallel'
        mock_api = MagicMock()
        events = MyEventManager.search_event(mock_api, query) #i don't understand but ok
        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.return_value.get.call_count, 0)
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs.get('q'), query)

        query = ''
        mock_api2 = MagicMock()
        events = MyEventManager.search_event(mock_api2, query) #i don't understand but ok
        args, kwargs2 = mock_api2.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs2.get('q'), '')

        query = None
        mock_api3 = MagicMock()
        events = MyEventManager.search_event(mock_api3, query) #i don't understand but ok
        kwargs3 = mock_api3.events.return_value.list.call_args_list
        self.assertEqual(kwargs3, [])

    def test_get_events(self):
        starting_time = '2022-9-20T00:00:10+8:00'
        ending_time = '2022-9-20T00:00:10+8:00'
        mock_api = MagicMock()
        events = MyEventManager.get_events(mock_api, starting_time, ending_time) #i don't understand but ok
        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.return_value.get.call_count, 0)
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs.get('timeMin'), starting_time)
        self.assertEqual(kwargs.get('timeMax'), ending_time)

    def test_delete_event(self):
        calId = '123@gmail.com'
        Id = '753951'
        mock_api = MagicMock()
        with self.assertRaises(TypeError):
            MyEventManager.delete_events(mock_api, calId, Id) 
        self.assertEqual(mock_api.events.return_value.get.return_value.execute.return_value.get.call_count,1)


    def test_export_events(self):
        starting_time = '2022-9-20T00:00:10+8:00'
        ending_time = '2022-9-20T00:00:10+8:00'
        mock_api = MagicMock()
        with self.assertRaises(TypeError):
            MyEventManager.export_event(mock_api, starting_time, ending_time) 
        
    def test_import_events(self):
        calId = "123@gmail.com"
        mock_api = MagicMock()
        MyEventManager.import_event(mock_api, calId)
        self.assertEqual(mock_api.events.return_value.get.return_value.execute.return_value.get.call_count,0)

    def test_print_events(self):
        mock_api = MagicMock()
        MyEventManager.print_events(mock_api,"2022-09-25T00:07:14+08:00","2022-09-26T23:50:00+08:00")
        self.assertEqual(mock_api.events.return_value.get.return_value.execute.return_value.get.call_count,0)

    def test_move_event(self):
        Id = '753951'
        mock_api = MagicMock()
        # move the eventmock_api = MagicMock()
        calId = "123456789@gmail.com"
        newCalID = "23456@gmail.com"
        event = MyEventManager.move_event(mock_api,calId,newCalID,Id)
        self.assertEqual(mock_api.events.return_value.move.return_value.execute.return_value.get.call_count, 0)

    def test_create_owner(self):
        mock_api = MagicMock()
        calId = "123456789@gmail.com"
        userEmail = "lmao@gmail.com"
        events = MyEventManager.create_owner(mock_api,calId,userEmail)
        self.assertEqual(mock_api.acl.return_value.insert.return_value.execute.return_value.get.call_count, 0)
        args, kwargs = mock_api.acl.return_value.insert.call_args_list[0] # this line to get the event body
        self.assertEqual(kwargs.get('body').get('role'), "owner")
        self.assertEqual(kwargs.get('body').get('scope').get('value'), userEmail)

    def test_create_reader(self):
        mock_api = MagicMock()
        calId = "123456789@gmail.com"
        userEmail = "lmao@gmail.com"
        events = MyEventManager.create_reader(mock_api,calId,userEmail)
        self.assertEqual(mock_api.acl.return_value.insert.return_value.execute.return_value.get.call_count, 0)
        args, kwargs = mock_api.acl.return_value.insert.call_args_list[0] # this line to get the event body
        self.assertEqual(kwargs.get('body').get('role'), "reader")
        self.assertEqual(kwargs.get('body').get('scope').get('value'), userEmail)

    def test_create_writer(self):
        mock_api = MagicMock()
        calId = "123456789@gmail.com"
        userEmail = "lmao@gmail.com"
        events = MyEventManager.create_writer(mock_api,calId,userEmail)
        self.assertEqual(mock_api.acl.return_value.insert.return_value.execute.return_value.get.call_count, 0)
        args, kwargs = mock_api.acl.return_value.insert.call_args_list[0] # this line to get the event body
        self.assertEqual(kwargs.get('body').get('role'), "writer")
        self.assertEqual(kwargs.get('body').get('scope').get('value'), userEmail)
    

        
    """ Coverage starts here """
    def test_get_upcoming_events_invalid_number(self):
        num_events = -1
        time = "2020-08-03T00:00:00.000000Z"
        mock_api = Mock()
        with self.assertRaises(ValueError):
            events = MyEventManager.get_upcoming_events(mock_api, time, num_events)
    # modifying date within modifiable date range (in between past created date and upper bound)
    # Condition coverage + branch coverage + statement coverage
    def test_valid_check_date(self):
        todayDate = "2024-09-22T00:00:00+08:00"
        self.assertEqual(MyEventManager.check_date(todayDate), True)
    
    # modifying date < today's date 
    # modifying date > upper bound's date 
    # Condition coverage + branch coverage + statement coverage
    def test_invalid_check_date(self):
        todayDate = "2020-09-22T00:00:00+08:00"
        with self.assertRaises(ValueError):
            self.assertEqual(MyEventManager.check_date(todayDate))
        todayDate = "2051-01-01T00:00:00+08:00"
        with self.assertRaises(ValueError):
            self.assertEqual(MyEventManager.check_date(todayDate))
    
    # calId = calendarId retrived from event
    # Condition coverage + branch coverage
    def test_check_valid_details(self):
        calId = "113@gmail.com"
        mock_api = MagicMock()
        self.assertEqual(MyEventManager.check_details(calId, calId), True)

    # calId != calendarId retrived from event
    # only happens when non-organiser attempting to modify an event
    # credentials won't match cause only organiser email is allowed to pass the test in order to modify event
    # Condition coverage + branch coverage
    def test_check_invalid_details(self):
        calId = "113@gmail.com"
        otherId = "223@gmail.com"
        mock_api = MagicMock()
        with self.assertRaises(ValueError): 
            events = MyEventManager.check_details(calId, otherId)

    # email format is valid
    # Condition coverage
    def test_valid_email_format1(self):
        email = "kekw@gmail.com"
        flag = MyEventManager.check_emailFormat(email)
        self.assertEqual(flag, True)
        email = "primary"
        flag = MyEventManager.check_emailFormat(email)
        self.assertEqual(flag, True)

    # email format is invalid 
    # Condition coverage
    def test_invalid_email_format(self):
        email = "PEPEGA"
        with self.assertRaises(ValueError):
            MyEventManager.check_emailFormat(email)
        email = "PEPEGA@hjello"
        with self.assertRaises(ValueError):
            MyEventManager.check_emailFormat(email)
        email = "PEPEGA.weeeeeeeeeeeeee"
        with self.assertRaises(ValueError):
            MyEventManager.check_emailFormat(email)
    
    # date format is valid
    # Condition coverage
    def test_valid_date_format(self):
        startdate = "2022-8-4"
        enddate = "2022-9-4"
        start, end = MyEventManager.ensure_date_format(startdate, enddate)
        self.assertEqual(end > start, True)
        startdate = "4-JAN-21"
        enddate = "4-OCT-22"
        start, end = MyEventManager.ensure_date_format(startdate, enddate)
        self.assertEqual(end > start, True)

    # date is invalid
    # Condition coverage
    def test_invalid_date_format(self):
        # start date > end date
        startdate = "2022-9-4"
        enddate = "2022-8-4"
        with self.assertRaises(ValueError):
            MyEventManager.ensure_date_format(startdate, enddate)
        startdate = "2022-9-4"
        enddate = "22-8-4"
        with self.assertRaises(ValueError):
            MyEventManager.ensure_date_format(startdate, enddate)
        startdate = "2051-9-4"
        enddate = "2052-8-4"
        with self.assertRaises(ValueError):
            MyEventManager.ensure_date_format(startdate, enddate)
        # yy-mm-dd invalid
        startdate = "22-9-4"
        enddate = "22-12-4"
        with self.assertRaises(ValueError):
            MyEventManager.ensure_date_format(startdate, enddate)
        # dd-mm-yy invalid
        startdate = "2-9-19"
        enddate = "13-12-21"
        with self.assertRaises(ValueError):
            MyEventManager.ensure_date_format(startdate, enddate)
    
    # time format is valid
    # Branch coverage
    def test_valid_time_format(self):
        starttime = "9:6:23"
        endtime = "15:55:3"
        flag = MyEventManager.ensure_time_format(starttime)
        self.assertEqual(flag, True)
        flag = MyEventManager.ensure_time_format(endtime)
        self.assertEqual(flag, True)

    # time format is invalid 
    # Branch coverage
    def test_invalid_time_format(self):
        starttime = "23:66:8"
        endtime = "25:12:69"
        with self.assertRaises(ValueError):
            MyEventManager.ensure_time_format(starttime)
        with self.assertRaises(ValueError):
            MyEventManager.ensure_time_format(endtime)

    # address format is valid
    # Condition coverage + Branch coverage 
    def test_valid_address_format(self):
        address = 'Mrs Smith, 546 Fake St., Clayton VIC 3400, AUSTRALIA'
        flag = MyEventManager.address_check(address)
        self.assertEqual(flag, True)
        address = 'Mr Morrison 11 Banks Av WAGGA WAGGA WEST VIRGINIA 2650 US'
        flag = MyEventManager.address_check(address)
        self.assertEqual(flag, True)
        address = ''
        flag = MyEventManager.address_check(address)
        self.assertEqual(flag, False)
        address = 'online'
        flag = MyEventManager.address_check(address)
        self.assertEqual(flag, False)

    # address format is invalid
    # Condition coverage + Branch coverage 
    def test_invalid_address_format(self):
        address = '52, jalan 1234A, KL'
        with self.assertRaises(ValueError):
            MyEventManager.address_check(address)
        address = '52KL'
        with self.assertRaises(ValueError):
            MyEventManager.address_check(address)
        address = 'Mrs Smith 546 Fake St. Clayton 3400 A'
        with self.assertRaises(ValueError):
            MyEventManager.address_check(address)
    
    # maxAttendee is valid
    # Condition coverage
    def test_attendees_limit(self):
        attendees = ['john@gmail.com', 'hi@gmail.com']
        guest = MyEventManager.check_attendee_limit(attendees)
        self.assertEqual(len(guest)<=20, True)
    
    # maxAttendee is invalid
    # Condition coverage
    def test_invalid_attendees_limit(self):
        attendees = ['john@gmail.com', 'hi@gmail.com', '1@gmail.com', '2@gmail.com', '3@gmail.com', '4@gmail.com', '5@gmail,com', '6@gmail.com'
        '7@gmail.com', '8@gmail.com', '9@gmail.com', '10@gmail.com', '13@gmail.com', '14@gmail.com', '15@gmail.com', '16@gmail.com', '17@gmail.com', 
        '18@gmail.com', '19@gmail.com', '20@gmail.com', '12@gmail.com', '21@gmail.com']
        with self.assertRaises(ValueError):
            MyEventManager.check_attendee_limit(attendees)

def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)
main()