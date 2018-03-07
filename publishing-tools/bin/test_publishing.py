import unittest
import publishing
from datetime import datetime


class TestPublishing(unittest.TestCase):

    def test_closed_interval(self):
        interval = publishing.Interval(datetime(2018, 6, 1), datetime(2018, 8, 1))

        self.assertTrue(datetime(2018, 5, 13) not in interval)
        self.assertTrue(datetime(2018, 6, 17) in interval)
        self.assertTrue(datetime(2018, 7, 19) in interval)
        self.assertTrue(datetime(2018, 8, 19) not in interval)

    def test_right_open_interval(self):
        interval = publishing.Interval(datetime(2018, 6, 1), None)

        self.assertTrue(datetime(2018, 5, 13) not in interval)
        self.assertTrue(datetime(2018, 6, 13) in interval)
        self.assertTrue(datetime(2019, 7, 17) in interval)
        self.assertTrue(datetime(2020, 8, 19) in interval)

    def test_left_open_interval(self):
        interval = publishing.Interval(None, datetime(2018, 6, 1))

        self.assertTrue(datetime(2018, 5, 13) in interval)
        self.assertTrue(datetime(2018, 6, 13) not in interval)
        self.assertTrue(datetime(2019, 7, 17) not in interval)
        self.assertTrue(datetime(2020, 8, 19) not in interval)

    def test_make_intervals(self):
        # check simple open
        intervals = publishing.make_interval_list([
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
        ])

        self.assertEqual(intervals, [
            publishing.Interval(datetime(2018, 3, 5), None),
        ])

        # check simple open -> close
        intervals = publishing.make_interval_list([
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 3, 11), 'event': 'decommissioned'},
        ])

        self.assertEqual(intervals, [
            publishing.Interval(datetime(2018, 3, 5), datetime(2018, 3, 11)),
        ])

        # check multiple open -> close
        intervals = publishing.make_interval_list([
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 3, 11), 'event': 'decommissioned'},
            {'timestamp': datetime(2018, 4, 10), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 4, 15), 'event': 'decommissioned'},
            {'timestamp': datetime(2018, 7, 20), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 7, 21), 'event': 'retired'},
        ])

        self.assertEqual(intervals, [
            publishing.Interval(datetime(2018, 3, 5), datetime(2018, 3, 11)),
            publishing.Interval(datetime(2018, 4, 10), datetime(2018, 4, 15)),
            publishing.Interval(datetime(2018, 7, 20), datetime(2018, 7, 21)),
        ])

        # check proper start union
        intervals = publishing.make_interval_list([
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 3, 11), 'event': 'commissioned'},
        ])

        self.assertEqual(intervals, [
            publishing.Interval(datetime(2018, 3, 5), None),
        ])

        # check proper end union
        intervals = publishing.make_interval_list([
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 3, 11), 'event': 'decommissioned'},
            {'timestamp': datetime(2018, 3, 17), 'event': 'decommissioned'},
        ])

        self.assertEqual(intervals, [
            publishing.Interval(datetime(2018, 3, 5), datetime(2018, 3, 11)),
        ])


if __name__ == '__main__':
    unittest.main()
