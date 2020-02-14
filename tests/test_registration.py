import requests
import subprocess
import time

nodeid = '0000000000000001'

# submit request for credentials
r = requests.post(f'http://localhost/api/registration?nodeid={nodeid}').json()
requestid = r['data']

# approve request
subprocess.check_output([
    'docker', 'exec', '-ti', 'beehive-mysql', 'mysql',
    '-u', 'waggle',
    '--password=waggle',
    '-D', 'waggle',
    '-e', f"update registrations set state='approved', response_date=NOW() where id='{requestid}';",
])

# print credentials
r = requests.get(f'http://localhost/api/registration/{requestid}')
print(r.text)
