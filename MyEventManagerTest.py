from datetime import datetime
import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
# Add other imports here if needed
class MyEventManagerTest(unittest.TestCase):
    initialEvent = None
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
    def test_insert_event(self):
        start_date = "2022-09-25"
        end_date = "2022-09-26"
        start_time = "20:06:14"
        end_time = "20:06:14"
        id = '753951'
        event_name = 'PEPEGA'
        location = ""
        calID = "123456@gmail.com"
        attendees = ["23456@gmail.com"]

    def test_get_events(self):
        starting_time = '2022-9-20T00:00:10+08:00'
        ending_time = '2022-9-20T00:00:10+08:00'
        mock_api = MagicMock()
        events = MyEventManager.insert_event(mock_api, calID, start_date, end_date, start_time, end_time, location, event_name ,id, attendees) #i don't understand but ok
        self.assertEqual(mock_api.events.return_value.insert.return_value.execute.return_value.get.call_count, 0)
        args, kwargs = mock_api.events.return_value.insert.call_args_list[0] # this line to get the event body
        self.assertEqual(kwargs.get('body').get('id'), id)

    # after rewrite
    # def test_valid_check_date(self):
    #     todayDate = datetime.now().strftime()

    #     MyEventManager.check_date(todayDate)
    
    def test_check_details(self):
        calId = "113@gmail.com"

        mock_api = MagicMock()
        events = MyEventManager.check_details(mock_api, calId)
        self.assertEqual(mock_api.events.return_value.get.return_value.execute.return_value.get.call_count, 0)
        args, kwargs = mock_api.acl.return_value.get.call_args_list[0]
        self.assertEqual(kwargs.get("calendarId"), calId)

    def test_valid_email_format(self):
        email = "kekw@gmail.com"
        flag = MyEventManager.check_emailFormat(email)
        self.assertEqual(flag, True)

    def test_invalid_email_format(self):
        email = "kekw"
        with self.assertRaises(ValueError):
            MyEventManager.check_emailFormat(email)
    
    def test_valid_date_format(self):
        startdate = "2022-8-4"
        enddate = "2022-9-4"
        start, end = MyEventManager.ensure_date_format(startdate, enddate)
        self.assertEqual(end > start, True)

        startdate = "4-JAN-21"
        enddate = "4-OCT-22"
        start, end = MyEventManager.ensure_date_format(startdate, enddate)
        self.assertEqual(end > start, True)

    def test_invalid_date_format(self):
        startdate = "2022-9-4"
        enddate = "2022-8-4"
        with self.assertRaises(ValueError):
            MyEventManager.ensure_date_format(startdate, enddate)

    def test_valid_time_format(self):
        starttime = "9:6:23"
        endtime = "15:55:3"
        flag = MyEventManager.ensure_time_format(starttime, endtime)
        self.assertEqual(flag, True)

    def test_invalid_time_format(self):
        starttime = "23:66:8"
        endtime = "5:12:69"
        with self.assertRaises(ValueError):
            MyEventManager.ensure_date_format(starttime, endtime)

        starttime = "23:6:8"
        endtime = "5:12:9"
        with self.assertRaises(ValueError):
            MyEventManager.ensure_date_format(starttime, endtime)

    def test_valid_address_format(self):
        address = 'Mrs Smith, 546 Fake St., Clayton VIC 3400, AUSTRALIA'
        flag = MyEventManager.address_check(address)
        self.assertEqual(flag, True)

        address = 'Mr Morrison 11 Banks Av WAGGA WAGGA NSW 2650 AUSTRALIA'
        flag = MyEventManager.address_check(address)
        self.assertEqual(flag, True)

        address = ''
        flag = MyEventManager.address_check(address)
        self.assertEqual(flag, False)

    def test_invalid_address_format(self):
        address = '52, jalan 1234A, KL'
        with self.assertRaises(ValueError):
            MyEventManager.address_check(address)
    

def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)
main()