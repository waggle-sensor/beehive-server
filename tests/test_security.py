import unittest
import requests
import subprocess
import time


class TestSecurity(unittest.TestCase):

    # TODO can make more fine grain. just moved end-to-end into single test for now

    def test_sql_injection_registration(self):
        r = requests.get(f'http://localhost/api/registration/1')
        self.assertNotRegex(r.text, "waggle.registrations.*doesn't exist")

        msg = "'; DROP TABLE registrations; SELECT * FROM registrations WHERE id='"
        r = requests.get(f'http://localhost/api/registration/{msg}')

        r = requests.get(f'http://localhost/api/registration/1')
        self.assertNotRegex(r.text, "waggle.registrations.*doesn't exist")


if __name__ == '__main__':
    unittest.main()
