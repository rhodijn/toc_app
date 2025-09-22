#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


import requests

def api_request(url: str, endpoint: str, method: str, payload: dict) -> tuple:
    """
    perform an api request and return the answer
    """
    if method == 'get':
        pass
    elif method == 'post':
        req = requests.post(f"{url}{endpoint}", json=payload)
    elif method == 'put':
        pass
    return req

zahl_1 = int(input('gib eine zahl ein: '))
zahl_2 = int(input('gib noch eine zahl ein: '))
r = api_request('http://127.0.0.1:5000/api/', 'sub', 'post', {'a': zahl_1,'b': zahl_2})
json_res = r.json()
print(f"das ergebnis ist {json_res['result']}")