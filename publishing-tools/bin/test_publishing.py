import unittest
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
import publishing
from datetime import datetime


class TestPublishing(unittest.TestCase):

    def test_closed_interval(self):
        interval = publishing.Interval(datetime(2018, 6, 1), datetime(2018, 8, 1))

        self.assertNotIn(datetime(2018, 5, 13), interval)
        self.assertIn(datetime(2018, 6, 17), interval)
        self.assertIn(datetime(2018, 7, 19), interval)
        self.assertNotIn(datetime(2018, 8, 19), interval)

    def test_right_open_interval(self):
        interval = publishing.Interval(datetime(2018, 6, 1), None)

        self.assertNotIn(datetime(2018, 5, 13), interval)
        self.assertIn(datetime(2018, 6, 13), interval)
        self.assertIn(datetime(2019, 7, 17), interval)
        self.assertIn(datetime(2020, 8, 19), interval)

    def test_left_open_interval(self):
        interval = publishing.Interval(None, datetime(2018, 6, 1))

        self.assertIn(datetime(2018, 5, 13), interval)
        self.assertNotIn(datetime(2018, 6, 13), interval)
        self.assertNotIn(datetime(2019, 7, 17), interval)
        self.assertNotIn(datetime(2020, 8, 19), interval)

    def test_infinite_interval(self):
        interval = publishing.Interval(None, None)

        self.assertIn(datetime(1910, 5, 13), interval)
        self.assertIn(datetime(2018, 6, 13), interval)
        self.assertIn(datetime(2019, 7, 17), interval)
        self.assertIn(datetime(2200, 8, 19), interval)

    def test_make_intervals_empty(self):
        self.assertEqual(publishing.make_interval_list([]), [])

    def test_make_intervals_open(self):
        intervals = publishing.make_interval_list([
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 3, 11), 'event': 'decommissioned'},
            {'timestamp': datetime(2018, 4, 10), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 4, 15), 'event': 'decommissioned'},
            {'timestamp': datetime(2018, 7, 20), 'event': 'commissioned'},
        ])

        self.assertEqual(intervals, [
            publishing.Interval(datetime(2018, 3, 5), datetime(2018, 3, 11)),
            publishing.Interval(datetime(2018, 4, 10), datetime(2018, 4, 15)),
            publishing.Interval(datetime(2018, 7, 20), None),
        ])

    def test_make_intervals_closed(self):
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

    def test_make_intervals_open_union(self):
        intervals = publishing.make_interval_list([
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 3, 11), 'event': 'commissioned'},
        ])

        self.assertEqual(intervals, [
            publishing.Interval(datetime(2018, 3, 5), None),
        ])

    def test_make_intervals_closed_union(self):
        intervals = publishing.make_interval_list([
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 3, 11), 'event': 'decommissioned'},
            {'timestamp': datetime(2018, 3, 17), 'event': 'decommissioned'},
        ])

        self.assertEqual(intervals, [
            publishing.Interval(datetime(2018, 3, 5), datetime(2018, 3, 11)),
        ])

    def test_make_intervals_start_before_end(self):
        intervals = publishing.make_interval_list([
            {'timestamp': datetime(2018, 3, 1), 'event': 'decommissioned'},
            {'timestamp': datetime(2018, 3, 2), 'event': 'decommissioned'},
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 3, 17), 'event': 'decommissioned'},
        ])

        self.assertEqual(intervals, [
            publishing.Interval(datetime(2018, 3, 5), datetime(2018, 3, 17)),
        ])

    def test_make_intervals_unknown_event(self):
        intervals = publishing.make_interval_list([
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 3, 17), 'event': 'unknown'},
        ])

        self.assertEqual(intervals, [
            publishing.Interval(datetime(2018, 3, 5), None),
        ])

    def test_make_intervals_unordered(self):
        from itertools import permutations

        input_permutations = permutations([
            {'timestamp': datetime(2018, 3, 5), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 4, 10), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 7, 20), 'event': 'commissioned'},
            {'timestamp': datetime(2018, 3, 11), 'event': 'decommissioned'},
            {'timestamp': datetime(2018, 4, 15), 'event': 'decommissioned'},
            {'timestamp': datetime(2020, 1, 1), 'event': 'retired'},
        ])

        output_intervals = [
            publishing.Interval(datetime(2018, 3, 5), datetime(2018, 3, 11)),
            publishing.Interval(datetime(2018, 4, 10), datetime(2018, 4, 15)),
            publishing.Interval(datetime(2018, 7, 20), datetime(2020, 1, 1)),
        ]

        for p in input_permutations:
            self.assertEqual(publishing.make_interval_list(p), output_intervals)


if __name__ == '__main__':
    unittest.main()
