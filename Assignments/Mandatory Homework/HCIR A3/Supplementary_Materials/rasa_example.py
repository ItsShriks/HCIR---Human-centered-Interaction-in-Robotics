import requests
import json
headers = {'content-type': 'application/json'}
message=''
defineUser = False
user = 'testuser'
while True:
    if not defineUser and user is None :
        user = input()
        defineUser=True
    message=input("you: ")

    payload = {'user':str(user),'message':str(message)}
    r = requests.post('http://localhost:5005/webhooks/rest/webhook', json=payload, headers=headers)
    print(json.loads(r.text))

