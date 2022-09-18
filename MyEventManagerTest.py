import unittest
from unittest.mock import MagicMock, Mock, patch
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
    def test_insert_event(self):
        start_date = "2022-09-18"
        end_date = "2022-09-18"
        id = '123456789'

        mock_api = Mock()
        mock_api.id = MyEventManager.insert_event(mock_api, start_date, end_date, id) #i don't understand but ok
        args, kwargs = mock_api.events.return_value.insert.call_args_list[0]
        self.assertEqual(kwargs.get('body').get('id'), id)

def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)
main()