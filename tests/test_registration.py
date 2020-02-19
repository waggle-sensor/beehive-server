import unittest
import requests
import subprocess
import time


class TestRegistration(unittest.TestCase):

    # TODO can make more fine grain. just moved end-to-end into single test for now
    def test_check_node_id_length(self):
        resp = requests.post(
            f'http://localhost/api/registration?nodeid=123456789').json()
        self.assertIn('error', resp)

        resp = requests.post(
            f'http://localhost/api/registration?nodeid=123456789123456789').json()
        self.assertIn('error', resp)

    def test_check_node_id_hex(self):
        resp = requests.post(
            f'http://localhost/api/registration?nodeid=0123456789abcdez').json()
        self.assertIn('error', resp)

    def test_full(self):
        nodeid = '0000000000000001'

        # start request for credentials
        r = requests.post(f'http://localhost/api/registration?nodeid={nodeid}')
        self.assertEqual(r.status_code, 200,
                         msg=f'invalid status code for response {r.text}')
        resp = r.json()
        self.assertIn('data', resp)
        requestid = resp['data']

        # approve request - TODO replace with what will become approval api
        subprocess.check_output([
            'docker', 'exec', '-ti', 'beehive-mysql', 'mysql',
            '-u', 'waggle',
            '--password=waggle',
            '-D', 'waggle',
            '-e', f"update registrations set state='approved', response_date=NOW() where id='{requestid}';",
        ])

        # check credentials
        r = requests.get(f'http://localhost/api/registration/{requestid}')
        self.assertEqual(r.status_code, 200,
                         msg=f'invalid status code for response {r.text}')
        self.assertIn('RSA PRIVATE KEY', r.text)
        self.assertIn('CERTIFICATE', r.text)
        self.assertIn('PORT', r.text)
        self.assertIn('ssh-rsa', r.text)

        # basic check that user exists in rabbitmq
        output = subprocess.check_output([
            'docker', 'exec', '-i', 'beehive-rabbitmq',
            'rabbitmqctl', 'list_user_permissions', f'node-{nodeid}',
        ]).decode()

        self.assertIn(f'to-node-{nodeid}', output)
        self.assertIn(f'messages', output)
        self.assertIn(f'data-pipeline-in', output)


if __name__ == '__main__':
    unittest.main()
