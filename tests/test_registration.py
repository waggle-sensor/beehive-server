import unittest
import requests
import subprocess
import time


class TestRegistration(unittest.TestCase):

    # TODO can make more fine grain. just moved end-to-end into single test for now

    def test_full(self):
        nodeid = '0000000000000001'

        # submit request for credentials
        r = requests.post(
            f'http://localhost/api/registration?nodeid={nodeid}').json()
        requestid = r['data']

        # approve request
        # TODO replace with what will become approval api
        subprocess.check_output([
            'docker', 'exec', '-ti', 'beehive-mysql', 'mysql',
            '-u', 'waggle',
            '--password=waggle',
            '-D', 'waggle',
            '-e', f"update registrations set state='approved', response_date=NOW() where id='{requestid}';",
        ])

        # print credentials
        r = requests.get(f'http://localhost/api/registration/{requestid}')
        self.assertIn('RSA PRIVATE KEY', r.text)
        self.assertIn('CERTIFICATE', r.text)
        self.assertIn('PORT', r.text)
        self.assertIn('ssh-rsa', r.text)


if __name__ == '__main__':
    unittest.main()
